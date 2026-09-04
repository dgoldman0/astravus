#!/usr/bin/env python3
"""Exercise the exported WebGL chapter through Chromium (requires Playwright)."""
import argparse
import asyncio
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit

from playwright.async_api import async_playwright

OUT = Path(__file__).resolve().parents[1] / "test-results/screenshots"
PROJECT = OUT.parents[1]


async def check_cache(page, url):
    """A cached response must revalidate online and remain available offline."""
    await page.goto(urljoin(url, "startup.js"))
    result = await page.evaluate('''async () => {
        await navigator.serviceWorker.register('./service-worker.js', {updateViaCache:'none'});
        await navigator.serviceWorker.ready;
        if (!navigator.serviceWorker.controller) {
            await new Promise(resolve => navigator.serviceWorker.addEventListener('controllerchange', resolve, {once:true}));
        }
        navigator.serviceWorker.controller.postMessage(['loadCache']);
        const cache = await caches.open('astravus-a-place-to-begin');
        const catalogURL = new URL('pwa_catalog.json', location.href).href;
        const oldHeaders = {'Last-Modified':'Sat, 01 Jan 2000 00:00:00 GMT'};
        await cache.put(catalogURL, new Response('{"version":"stale-copy"}', {headers:oldHeaders}));
        await cache.put(new URL('game.zip', location.href).href, new Response('stale-game', {headers:oldHeaders}));
        const fresh = await (await fetch(catalogURL)).json();
        const saved = await (await cache.match(catalogURL)).json();
        return {fresh:fresh.version, saved:saved.version};
    }''')
    expected = json.loads((PROJECT / "build/web/pwa_catalog.json").read_text())["version"]
    assert result == {"fresh": expected, "saved": expected}, result
    await page.context.set_offline(True)
    try:
        cached = await page.evaluate('async () => (await (await fetch("pwa_catalog.json")).json()).version')
        assert cached == expected, cached
    finally:
        await page.context.set_offline(False)
    print("Browser cache passed: stale copy replaced online; refreshed copy remains available offline.")


async def check(url):
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--enable-unsafe-swiftshader", "--use-angle=swiftshader"])
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("console", lambda message: errors.append(message.text)
                if "Full traceback:" in message.text or "While running game code:" in message.text else None)
        await check_cache(page, url)
        await page.goto(url)
        await page.wait_for_function('typeof window.renpy_get === "function"')

        async def value(expression):
            return await asyncio.wait_for(page.evaluate("expression => window.renpy_get(expression)", expression), 45)

        async def until(expression, seconds=20):
            async with asyncio.timeout(seconds):
                while not await value(expression):
                    await asyncio.sleep(.1)
            # A screen exists while its menu transition is still consuming input.
            await asyncio.sleep(.3)

        assert await value("main_menu")
        expected_version = re.search(r'config.version = "([^"]+)"', (PROJECT / "game/options.rpy").read_text()).group(1)
        assert await value("config.version") == expected_version
        await page.screenshot(path=str(OUT / "browser-title.png"))
        await page.mouse.click(220, 373)
        await until('bool(renpy.get_screen("chapter_card"))')
        await page.keyboard.press("Enter")
        await until('bool(renpy.get_screen("say"))')
        assert await value('renpy.showing("cg first_memory") and not renpy.showing("calista")')
        await page.screenshot(path=str(OUT / "browser-first-memory.png"))
        # Speed up reveal, while advancing the actual story with input events.
        await page.evaluate('() => window.renpy_exec("preferences.text_cps = 0")')
        captured = set()
        locations = {2: "garden_close", 3: "community_courtyard", 4: "construction_path", 5: "treehouse"}
        home_seen = False
        rain_seen = False
        for _ in range(360):
            if await value('bool(renpy.get_screen("chapter_end"))'):
                break
            scene = await value("scene_number")
            if not home_seen and await value('renpy.showing("bg family_home")'):
                assert not await value('renpy.showing("cg")')
                await until('bool(renpy.get_screen("say")) and _history_list[-1].what.startswith("The home I grew")')
                await page.screenshot(path=str(OUT / "browser-family-home.png"))
                home_seen = True
            if scene in (2, 3, 4, 5) and scene not in captured:
                if await value('bool(renpy.get_screen("say")) and (renpy.showing("calista") or renpy.showing("cassia"))'):
                    assert await value(f'renpy.showing("bg {locations[scene]}")'), scene
                    await page.screenshot(path=str(OUT / f"browser-scene-{scene}.png"))
                    captured.add(scene)
            if not rain_seen and await value('renpy.showing("bg treehouse_rain")'):
                await until('renpy.music.get_playing(channel="ambience") == "audio/rain.wav"')
                assert not await value('renpy.showing("cassia") or renpy.showing("joren")')
                await page.screenshot(path=str(OUT / "browser-treehouse-rain.png"))
                rain_seen = True
            await page.keyboard.press("Space")
            await asyncio.sleep(.08)
        else:
            raise AssertionError("The browser chapter did not reach its end.")
        assert await value("persistent.chapter_complete and met_cassia and met_joren")
        assert captured == {2, 3, 4, 5}, captured
        assert home_seen and rain_seen
        await page.screenshot(path=str(OUT / "browser-end.png"))
        # A successful ending must remain usable, including across page reloads.
        await page.mouse.click(640, 454)
        await until('bool(renpy.get_screen("about"))')
        await page.keyboard.press("Escape")
        await until('bool(renpy.get_screen("chapter_end")) and not renpy.context()._menu')
        await page.mouse.click(640, 398)
        await until("main_menu")
        await page.reload()
        await page.wait_for_function('typeof window.renpy_get === "function"')
        await until("main_menu")
        await page.mouse.click(220, 373)
        await until('bool(renpy.get_screen("chapter_end"))')
        assert not errors, errors
        print(f"Browser {expected_version} playthrough passed: First Memory, home, distinct scene locations, visible rain with rain audio, ending, Credits, title, reload, Continue; no page or Ren'Py errors.")
        await browser.close()

        # Match the reported embedded-preview failure: no WebGL, no user input.
        browser = await p.chromium.launch(args=["--disable-webgl"])
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        requests = []
        page.on("request", lambda request: requests.append(request.url))
        await page.goto(url)
        await page.locator("#startup-fallback").wait_for()
        assert await page.locator("#game-address").input_value() == page.url
        assert await page.locator("#open-browser").get_attribute("target") == "_blank"
        assert not any(urlsplit(path).path.endswith(("/renpy.js", "/renpy-pre.js", "/renpy.wasm", "/game.zip")) for path in requests)
        assert await page.evaluate('typeof window.renpy_get') == "undefined"
        await page.screenshot(path=str(OUT / "browser-no-webgl.png"))
        print("Unsupported graphics startup passed: useful fallback shown before any engine or game download.")
        await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    asyncio.run(check(parser.parse_args().url))
