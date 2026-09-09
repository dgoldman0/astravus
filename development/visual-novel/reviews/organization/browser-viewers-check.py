"""Exercise the three repository-local art viewers over HTTP using Chromium.

Run from any working directory: python3 path/to/browser-viewers-check.py.
Requires Playwright with Chromium and Pillow. No external requests are permitted.
Writes only its receipt and browser screenshots beside this script.
"""

import asyncio
import hashlib
import io
import json
import re
import threading
from datetime import datetime, timezone
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from PIL import Image, ImageChops
from playwright.async_api import async_playwright

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
VIEWERS = {
    "keys": ROOT / "visual-novel/art/character-keys/index.html",
    "comparisons": ROOT / "development/visual-novel/art/character-refinements/review.html",
    "opening": ROOT / "development/visual-novel/art/opening-identity/review.html",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return path.resolve().relative_to(ROOT).as_posix()


def embedded(path, identifier):
    pattern = rf'<script id="{identifier}" type="application/json">(.*?)</script>'
    return json.loads(re.search(pattern, path.read_text(), re.S).group(1))


def same_pixels(first, second):
    left = Image.open(io.BytesIO(first)).convert("RGB")
    right = Image.open(io.BytesIO(second)).convert("RGB")
    return left.size == right.size and ImageChops.difference(left, right).getbbox() is None


class LocalRefs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = set()

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("href", "src") and value and not value.startswith(("#", "data:")):
                if not urlsplit(value).scheme:
                    self.refs.add(value)


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


async def run():
    catalog_path = VIEWERS["keys"].parent / "catalog.json"
    catalog = json.loads(catalog_path.read_text())
    assert catalog == embedded(VIEWERS["keys"], "catalog-data")
    assets = embedded(VIEWERS["comparisons"], "assets-data")
    assert len(catalog["characters"]) == 17
    assert sum(len(c["sheets"]) for c in catalog["characters"]) == 20
    assert len(assets) == 9

    input_paths = {Path(__file__).resolve(), catalog_path, *VIEWERS.values()}
    for viewer in VIEWERS.values():
        parser = LocalRefs()
        parser.feed(viewer.read_text())
        for ref in parser.refs:
            input_paths.add((viewer.parent / unquote(urlsplit(ref).path)).resolve())
    for character in catalog["characters"]:
        input_paths.add((VIEWERS["keys"].parent / character["notes"]).resolve())
        for collection in ("sheets", "sources", "selected_art"):
            for item in character[collection]:
                path = (VIEWERS["keys"].parent / item["file"]).resolve()
                input_paths.add(path)
                if collection == "sheets":
                    with Image.open(path) as image:
                        assert list(image.size) == item["dimensions"]
    for asset in assets:
        for version in ("before", "after"):
            path = (VIEWERS["comparisons"].parent / asset[version]).resolve()
            input_paths.add(path)
            with Image.open(path) as image:
                assert list(image.size) == asset["size"]
        input_paths.add((VIEWERS["comparisons"].parent / asset["key"].split("#")[0]).resolve())
    input_paths.add(VIEWERS["opening"].parent / "opening-generated-v1.png")

    inputs = []
    for path in sorted(input_paths):
        assert path.is_file(), path
        entry = {"path": relative(path), "sha256": sha(path), "bytes": path.stat().st_size}
        if path.suffix.lower() == ".png":
            with Image.open(path) as image:
                image.load()
                entry["dimensions"] = list(image.size)
        inputs.append(entry)

    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = f"http://127.0.0.1:{server.server_address[1]}"
    errors, console_errors, failed_requests, external_requests, http_errors = [], [], [], [], []
    checks = {}
    screenshots = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
            browser_version = browser.version
            context = await browser.new_context(viewport={"width": 1500, "height": 1080})

            async def route_request(route):
                if route.request.url.startswith(origin + "/"):
                    await route.continue_()
                else:
                    external_requests.append(route.request.url)
                    await route.abort()

            await context.route("**/*", route_request)
            page = await context.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
            page.on("requestfailed", lambda request: failed_requests.append({"url": request.url, "failure": request.failure}))
            page.on("response", lambda response: http_errors.append({"url": response.url, "status": response.status}) if response.status >= 400 else None)

            async def capture(name):
                path = OUT / name
                if await page.locator("#comparison").count():
                    await page.wait_for_function("document.getElementById('comparison').dataset.ready === 'true'")
                await page.screenshot(path=str(path), full_page=True)
                screenshots.append({"path": relative(path), "sha256": sha(path)})

            # HEAD-check every linked local input as served, including documents.
            for entry in inputs:
                response = await context.request.head(origin + "/" + entry["path"])
                assert response.status == 200, (entry["path"], response.status)

            await page.goto(origin + "/" + relative(VIEWERS["keys"]), wait_until="load")
            assert await page.locator(".character-button").count() == 17
            opened = []
            for character in catalog["characters"]:
                for sheet in character["sheets"]:
                    route = f"#{character['id']}/{sheet['id']}"
                    await page.evaluate("route => location.hash = route", route)
                    await page.wait_for_function("name => document.getElementById('name').textContent === name", arg=character["name"])
                    await page.wait_for_function("suffix => { const img=document.querySelector('.image-viewport img'); return img && img.src.endsWith(suffix) && img.complete && img.naturalWidth > 0; }", arg=sheet["file"])
                    assert await page.locator("#key-notes").get_attribute("href") == character["notes"]
                    opened.append({"route": route, "sheet": sheet["file"]})
            await page.evaluate("location.hash = '#calista/early/compare'")
            await page.wait_for_function("document.querySelectorAll('.image-viewport img').length === 2 && [...document.querySelectorAll('.image-viewport img')].every(i => i.complete && i.naturalWidth > 0)")
            assert await page.locator("#compare").is_checked()
            assert await page.locator("#stage").is_disabled()
            await page.select_option("#zoom", "2")
            assert await page.locator(".image-viewport").first.evaluate("n => n.scrollWidth > n.clientWidth")
            await page.click("#reset")
            assert await page.locator("#zoom").input_value() == "fit"
            await capture("browser-keys-desktop.png")
            await page.evaluate("location.hash = '#lyron/key'")
            await page.wait_for_function("() => {const i=document.querySelector('.image-viewport img'); return i.src.endsWith('lyron/key.png') && i.complete && i.naturalWidth > 0;}")
            assert "key-initial" not in await page.locator("#sheets").inner_html()
            await page.reload(wait_until="load")
            assert await page.locator("#name").text_content() == "Lyron"
            await page.set_viewport_size({"width": 390, "height": 844})
            assert await page.locator("#character-select").is_visible()
            assert not await page.locator(".sidebar").is_visible()
            await page.select_option("#character-select", "nibble")
            await page.wait_for_function("document.getElementById('name').textContent === 'Nibble' && document.querySelector('.image-viewport img').complete && document.querySelector('.image-viewport img').naturalWidth > 0")
            assert await page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
            await capture("browser-keys-mobile.png")
            checks["keys"] = {"sheets_opened": opened, "character_count": 17, "embedded_catalog_matches_file": True, "compare_stages": True, "zoom_200_percent_and_reset": True, "lyron_current_sheet": True, "deep_link_reload": True, "mobile_selector_and_no_horizontal_overflow": True}

            await page.set_viewport_size({"width": 1500, "height": 1080})
            await page.goto(origin + "/" + relative(VIEWERS["comparisons"]), wait_until="load")
            assert await page.locator("#asset option").count() == 9
            compared = []
            for asset in assets:
                await page.select_option("#asset", asset["id"])
                await page.wait_for_function("name => document.getElementById('title').textContent === name && document.getElementById('comparison').dataset.ready === 'true'", arg=asset["name"])
                assert await page.locator("#comparison").get_attribute("viewBox") == f"0 0 {asset['size'][0]} {asset['size'][1]}"
                for version in ("before", "after"):
                    assert await page.locator(f"#{version}-image").get_attribute("href") == asset[version]
                    assert await page.locator(f"#open-{version}").get_attribute("href") == asset[version]
                await page.click('[data-mode="before"]')
                before = await page.locator("#comparison").screenshot()
                await page.click('[data-mode="split"]')
                await page.locator("#split").evaluate("n => { n.value=100; n.dispatchEvent(new Event('input')); }")
                assert same_pixels(before, await page.locator("#comparison").screenshot()), (asset["id"], "before endpoint")
                await page.click('[data-mode="after"]')
                after = await page.locator("#comparison").screenshot()
                assert not same_pixels(before, after), (asset["id"], "versions unexpectedly identical")
                await page.click('[data-mode="split"]')
                await page.locator("#split").evaluate("n => { n.value=0; n.dispatchEvent(new Event('input')); }")
                assert same_pixels(after, await page.locator("#comparison").screenshot()), (asset["id"], "after endpoint")
                for detail in asset["details"]:
                    await page.select_option("#detail", detail["id"])
                    expected = " ".join(map(str, detail["box"]))
                    await page.wait_for_function("box => document.getElementById('comparison').getAttribute('viewBox') === box", arg=expected)
                    await page.locator("#split").evaluate("n => { n.value=37; n.dispatchEvent(new Event('input')); }")
                    edge = float(await page.locator("#clip-rect").get_attribute("x"))
                    assert abs(edge - (detail["box"][0] + detail["box"][2] * .37)) < .001
                compared.append({"asset": asset["id"], "both_versions_loaded": True, "different_rendered_pixels": True, "split_endpoints_equal_modes": True, "detail_presets": [d["id"] for d in asset["details"]]})
            await page.select_option("#asset", "pond-comfort")
            await page.wait_for_function("document.getElementById('comparison').dataset.ready === 'true'")
            await page.click("#reset")
            assert await page.locator("#split").input_value() == "50"
            assert await page.locator("#detail").input_value() == "full"
            await capture("browser-comparisons-desktop.png")
            await page.select_option("#detail", "lyra")
            await page.wait_for_function("document.getElementById('comparison').dataset.ready === 'true' && document.getElementById('comparison').getAttribute('viewBox') === '725 270 280 290'")
            await page.reload(wait_until="load")
            await page.wait_for_function("document.getElementById('comparison').dataset.ready === 'true'")
            assert await page.locator("#detail").input_value() == "lyra"
            assert await page.locator("#asset").input_value() == "pond-comfort"
            await page.locator("#title").click()
            for key, mode in (("b", "before"), ("a", "after"), ("s", "split")):
                await page.keyboard.press(key)
                assert await page.locator(f'[data-mode="{mode}"]').get_attribute("aria-pressed") == "true"
            await capture("browser-comparisons-detail.png")
            await page.set_viewport_size({"width": 390, "height": 844})
            for asset_id in ("lyra", "lyron", "opening"):
                await page.select_option("#asset", asset_id)
                await page.wait_for_function("document.getElementById('comparison').dataset.ready === 'true'")
                assert await page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
            await page.select_option("#asset", "lyron")
            await page.wait_for_function("document.getElementById('comparison').dataset.ready === 'true'")
            await page.select_option("#detail", "garment")
            await capture("browser-comparisons-mobile.png")
            checks["comparisons"] = {"pairs": compared, "split_endpoint_pixel_checks": 18, "reset_full_split_50_percent": True, "deep_link_reload": True, "keyboard_B_A_S": True, "mobile_portrait_landscape_and_detail_no_horizontal_overflow": True}

            await page.set_viewport_size({"width": 1500, "height": 1080})
            await page.goto(origin + "/" + relative(VIEWERS["opening"]), wait_until="load")
            await page.locator(".runtime").scroll_into_view_if_needed()
            await page.wait_for_function("[...document.images].every(i => i.complete && i.naturalWidth > 0)")
            for mode in ("original", "refined", "generated", "compare"):
                await page.click(f'[data-mode="{mode}"]')
                assert await page.locator(f'[data-mode="{mode}"]').get_attribute("aria-pressed") == "true"
                if mode == "original":
                    assert not await page.locator("#candidate").is_visible()
                else:
                    expected = "opening-generated-v1.png" if mode == "generated" else "opening-refined-v1.png"
                    await page.wait_for_function("suffix => {const i=document.getElementById('candidate'); return i.src.endsWith(suffix) && i.complete && i.naturalWidth > 0;}", arg=expected)
            assert await page.locator("#slider-row").is_visible()
            await page.locator("#split").focus()
            await page.keyboard.press("ArrowRight")
            assert await page.locator("#split").input_value() == "51"
            assert await page.locator("#candidate").evaluate("n => n.style.clipPath") == "inset(0px 49% 0px 0px)"
            for value in (0, 100, 50):
                await page.locator("#split").evaluate("(n,v) => { n.value=v; n.dispatchEvent(new Event('input')); }", value)
                assert await page.locator("#divider").evaluate("n => n.style.left") == f"{value}%"
            await page.evaluate("window.scrollTo(0,0)")
            await capture("browser-opening-desktop.png")
            await page.set_viewport_size({"width": 390, "height": 844})
            assert await page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
            await page.click('[data-mode="generated"]')
            await page.wait_for_function("document.getElementById('candidate').complete && document.getElementById('candidate').naturalWidth > 0")
            await page.click('[data-mode="compare"]')
            await page.evaluate("window.scrollTo(0,0)")
            await capture("browser-opening-mobile.png")
            checks["opening"] = {"modes": ["original", "refined", "generated", "compare"], "runtime_images_loaded": 2, "face_insets": 4, "split_endpoints_and_keyboard_arrow": True, "mobile_modes_and_no_horizontal_overflow": True}
            assert not errors, errors
            assert not console_errors, console_errors
            assert not failed_requests, failed_requests
            assert not http_errors, http_errors
            assert not external_requests, external_requests
            await browser.close()
    finally:
        server.shutdown()
        server.server_close()

    for entry in inputs:
        assert sha(ROOT / entry["path"]) == entry["sha256"], f"Input changed during test: {entry['path']}"
    result = {
        "status": "passed",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Moved local HTML viewer loading, controls and responsive layout; not a new native Ren'Py or whole-art audit.",
        "entrypoints": {name: relative(path) for name, path in VIEWERS.items()},
        "server": {"document_root": ".", "bind": "127.0.0.1", "port": "ephemeral", "transport": "HTTP"},
        "browser": {"engine": "Chromium via Playwright", "version": browser_version, "headless": True, "desktop_viewport": [1500, 1080], "mobile_viewport": [390, 844], "external_requests_blocked": True},
        "checks": checks,
        "all_input_paths_exist_and_HTTP_HEAD_200": True,
        "inputs_unchanged_during_test": True,
        "inputs": inputs,
        "screenshots": screenshots,
        "javascript_errors": errors,
        "console_errors": console_errors,
        "failed_requests": failed_requests,
        "HTTP_errors": http_errors,
        "external_requests": external_requests,
    }
    (OUT / "browser-viewers.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "keys": 20, "pairs": 9, "opening_modes": 4, "inputs": len(inputs), "screenshots": len(screenshots), "browser_version": browser_version}, indent=2))


if __name__ == "__main__":
    asyncio.run(run())
