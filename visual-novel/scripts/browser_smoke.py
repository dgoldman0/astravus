#!/usr/bin/env python3
"""Play the complete exported Book I in Chromium, including save/cache regressions."""
import argparse
import asyncio
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit

from playwright.async_api import async_playwright

OUT = Path(__file__).resolve().parents[1] / "test-results/screenshots"
PROJECT = OUT.parents[1]
SCENES = (
    "first_memory", "garden", "plant_disagreement", "workshop_first", "music_first",
    "dorian_stories", "sage_story", "family_rhythm", "tree_echoes", "pond_scare",
    "soup_experiment", "festival_lights", "meeting_cassia", "cassia_home",
    "meeting_joren", "joren_home", "kaleb_walk", "treehouse", "rain_refuge",
    "waterwheel", "outer_exploration", "lyra_included", "dome_ascent",
    "treehouse_dispute", "loss", "family_grief", "painting_grief", "cassia_grief",
    "community_memorial", "mural_remembrance", "treehouse_remembrance", "annual_remembrance",
)
# One bridge request per story step: avoid dozens of IPC roundtrips per scene.
STATE = '''dict(
    end=bool(renpy.get_screen("chapter_end")), say=bool(renpy.get_screen("say")),
    scene=scene_key, number=scene_number, visited=list(visited_scenes),
    known=lumen_known, lost=joren_lost, stage=childhood_stage,
    met_cassia=met_cassia, met_joren=met_joren,
    bg=" ".join(renpy.get_attributes("bg") or ()),
    cg=" ".join(renpy.get_attributes("cg") or ()),
    calista=(" ".join(renpy.get_attributes("calista") or ()) if renpy.showing("calista") else None),
    cassia=(" ".join(renpy.get_attributes("cassia") or ()) if renpy.showing("cassia") else None),
    joren=(" ".join(renpy.get_attributes("joren") or ()) if renpy.showing("joren") else None),
    music=renpy.music.get_playing(), ambience=renpy.music.get_playing(channel="ambience"),
    sound=renpy.music.get_playing(channel="sound"),
    text=(_history_list[-1].what if _history_list else ""),
    complete=persistent.book_one_complete)'''


async def check_cache(page, url):
    """A cached response must revalidate online and remain available offline."""
    await page.goto(urljoin(url, "startup.js"))
    worker = (PROJECT / "web/service-worker.js").read_text()
    cache_name = re.search(r"var cacheName = '([^']+)'", worker).group(1)
    result = await page.evaluate('''async cacheName => {
        await navigator.serviceWorker.register('./service-worker.js', {updateViaCache:'none'});
        await navigator.serviceWorker.ready;
        if (!navigator.serviceWorker.controller) {
            await new Promise(resolve => navigator.serviceWorker.addEventListener('controllerchange', resolve, {once:true}));
        }
        navigator.serviceWorker.controller.postMessage(['loadCache']);
        const cache = await caches.open(cacheName);
        const catalogURL = new URL('pwa_catalog.json', location.href).href;
        const oldHeaders = {'Last-Modified':'Sat, 01 Jan 2000 00:00:00 GMT'};
        await cache.put(catalogURL, new Response('{"version":"stale-copy"}', {headers:oldHeaders}));
        await cache.put(new URL('game.zip', location.href).href, new Response('stale-game', {headers:oldHeaders}));
        const fresh = await (await fetch(catalogURL)).json();
        const saved = await (await cache.match(catalogURL)).json();
        return {fresh:fresh.version, saved:saved.version};
    }''', cache_name)
    expected = json.loads((PROJECT / "build/web/pwa_catalog.json").read_text())["version"]
    assert result == {"fresh": expected, "saved": expected}, result
    await page.context.set_offline(True)
    try:
        cached = await page.evaluate('async () => (await (await fetch("pwa_catalog.json")).json()).version')
        assert cached == expected, cached
    finally:
        await page.context.set_offline(False)
    print("Browser cache passed: stale copy replaced online; refreshed copy remains available offline.", flush=True)


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
        await page.wait_for_function('typeof window.renpy_get === "function"', timeout=90000)

        async def value(expression):
            return await asyncio.wait_for(page.evaluate("expression => window.renpy_get(expression)", expression), 45)

        async def execute(code):
            return await asyncio.wait_for(page.evaluate("code => window.renpy_exec(code)", code), 45)

        async def until(expression, seconds=30):
            async with asyncio.timeout(seconds):
                while not await value(expression):
                    if errors:
                        raise AssertionError(errors)
                    await asyncio.sleep(.1)
            await asyncio.sleep(.25)

        async def click_button(screen, label):
            # Read the engine's rendered focus rectangles, then send a real click.
            assert await value(f'bool(renpy.get_screen({screen!r}))')
            code = f'''result = []
for focus in renpy.display.focus.focus_list:
    if focus.widget is None or focus.x is None:
        continue
    texts = []
    focus.widget.visit_all(lambda item, out=texts: out.append(item.get_all_text()) if isinstance(item, renpy.text.text.Text) else None)
    if {label!r} in texts and focus.x is not None:
        result.append([focus.x, focus.y, focus.w, focus.h])'''
            rectangles = await execute(code)
            assert rectangles, f"No visible {label!r} button on {screen}"
            x, y, width, height = rectangles[0]
            await page.mouse.click((x + width / 2) * 2 / 3, (y + height / 2) * 2 / 3)

        assert await value("main_menu")
        expected_version = re.search(r'config.version = "([^"]+)"', (PROJECT / "game/options.rpy").read_text()).group(1)
        assert await value("config.version") == expected_version
        assert await value("config.save_directory") == "Astravus-Book-I"
        await page.screenshot(path=str(OUT / "browser-title.png"))
        # A fresh browser context has no compatible Book I Continue entry.
        await page.mouse.click(220, 373)
        await until('bool(renpy.get_screen("chapter_card"))')
        await page.keyboard.press("Enter")
        await until('bool(renpy.get_screen("say"))')
        initial = await value(STATE)
        assert initial["cg"] == "first_memory" and initial["calista"] is None, initial
        assert not initial["known"] and not initial["lost"]
        assert initial["visited"] == ["first_memory"]
        await page.screenshot(path=str(OUT / "browser-first-memory.png"))
        await execute("preferences.text_cps = 0\npersistent.reduced_motion = True")
        captured = {"first_memory"}
        observed = []
        first_flute = False
        practiced_flute = False
        cassia_aged = False
        before_echo_reveal = False
        after_echo_reveal = False
        loss_seen = False
        manual_save_checked = False
        expected_backgrounds = {
            "garden": "garden_close", "plant_disagreement": "garden_close",
            "workshop_first": "workshop", "music_first": "music_room",
            "dorian_stories": "library", "sage_story": "sage_room",
            "tree_echoes": "echoes", "pond_scare": "garden_close",
            "soup_experiment": "family_home", "festival_lights": "festival",
            "meeting_cassia": "community_courtyard", "meeting_joren": "construction_path",
            "treehouse": "treehouse", "rain_refuge": "treehouse_rain",
            "outer_exploration": "construction_room",
            "dome_ascent": "dome", "treehouse_dispute": "treehouse",
            "family_grief": "home_dusk", "painting_grief": "family_home",
            "cassia_grief": "treehouse", "community_memorial": "memorial_plaza",
            "mural_remembrance": "memory_mural", "treehouse_remembrance": "treehouse_memory",
            "annual_remembrance": "memorial_plaza",
        }
        actor_requirements = {
            "garden": ("calista", "young"), "meeting_cassia": ("cassia", "young"),
            "meeting_joren": ("joren", "young"),
            "plant_disagreement": ("calista", "home"),
            "festival_lights": ("calista", "festival"),
            "treehouse": ("cassia", "young"), "waterwheel": ("calista", "older"),
            "treehouse_dispute": ("calista", "frustrated"),
            "family_grief": ("calista", "mourning"),
            "painting_grief": ("calista", "painting"),
            "cassia_grief": ("cassia", "mourning"),
        }
        for step in range(1500):
            state = await value(STATE)
            if errors:
                raise AssertionError(errors)
            if state["end"]:
                break
            key = state["scene"]
            if not observed or observed[-1] != key:
                observed.append(key)
                print(f"Browser scene {state['number']:02d}/32: {key}", flush=True)
            assert state["number"] == SCENES.index(key) + 1, state
            if state["number"] < 9:
                assert not state["known"], state
            if key == "tree_echoes":
                before_echo_reveal |= not state["known"]
                after_echo_reveal |= state["known"]
            if state["lost"]:
                loss_seen = True
                assert state["joren"] is None, state
            if state["number"] >= 20:
                assert state["stage"] == "later", state
            first_flute |= state["sound"] == "audio/flute_first.wav"
            practiced_flute |= state["sound"] == "audio/flute_practice.wav"
            if key == "waterwheel" and state["cassia"] == "older":
                assert not state["lost"]
                if not cassia_aged:
                    await page.screenshot(path=str(OUT / "browser-cassia-older.png"))
                cassia_aged = True
            if key == "garden" and not manual_save_checked and state["text"] == "Here, Cali.":
                await click_button("quick_menu", "Save")
                await until('bool(renpy.get_screen("save"))')
                await click_button("save", "1")
                await asyncio.sleep(.2)
                await click_button("save", "Empty slot")
                await until('renpy.can_load("1-1")')
                await page.keyboard.press("Escape")
                await until('bool(renpy.get_screen("say")) and not renpy.context()._menu')
                await page.keyboard.press("Space")
                await asyncio.sleep(.1)
                await page.keyboard.press("Space")
                await asyncio.sleep(.1)
                await click_button("quick_menu", "Load")
                await until('bool(renpy.get_screen("load"))')
                await click_button("load", "1")
                await asyncio.sleep(.2)
                saved_label = await value('FileTime(1, format="%b %d · %H:%M", empty="Empty slot")')
                await click_button("load", saved_label)
                await until('bool(renpy.get_screen("confirm"))')
                await click_button("confirm", "Yes")
                await until('_history_list[-1].what == "Here, Cali." and not renpy.context()._menu')
                assert await value('renpy.slot_json("1-1").get("book_id") == BOOK_SAVE_ID')
                manual_save_checked = True
            if key not in captured and state["say"]:
                desired_bg = expected_backgrounds.get(key)
                actor = actor_requirements.get(key)
                if (desired_bg is None or state["bg"] == desired_bg) and (actor is None or state[actor[0]] == actor[1]):
                    if key in ("rain_refuge", "treehouse_remembrance"):
                        assert state["ambience"] == "audio/rain.ogg", state
                    if key == "rain_refuge":
                        assert state["joren"] is None and state["cassia"] is None, state
                    if key == "family_grief":
                        assert state["music"] == "audio/grief_theme.ogg", state
                    await page.screenshot(path=str(OUT / f"browser-{key}.png"))
                    captured.add(key)
            if key == "first_memory" and state["bg"] == "family_home" and "home-view" not in captured:
                assert not state["cg"], state
                await page.screenshot(path=str(OUT / "browser-family-home.png"))
                captured.add("home-view")
            await page.keyboard.press("Space")
            await asyncio.sleep(.06)
        else:
            raise AssertionError(f"Book I did not finish after 1500 input steps; last state: {state}")
        assert state["complete"] and state["met_cassia"] and state["met_joren"], state
        assert state["visited"] == list(SCENES), state["visited"]
        assert observed == list(SCENES), observed
        assert set(SCENES) <= captured, set(SCENES) - captured
        assert all((first_flute, practiced_flute, cassia_aged, before_echo_reveal, after_echo_reveal, loss_seen, manual_save_checked))
        await page.screenshot(path=str(OUT / "browser-end.png"))
        # End menus, persistence and Continue must remain usable after reload.
        await click_button("chapter_end", "Credits")
        await until('bool(renpy.get_screen("about"))')
        await page.keyboard.press("Escape")
        await until('bool(renpy.get_screen("chapter_end")) and not renpy.context()._menu')
        await click_button("chapter_end", "Return to title")
        await until("main_menu")
        await page.reload()
        await page.wait_for_function('typeof window.renpy_get === "function"', timeout=90000)
        await until("main_menu")
        await page.mouse.click(220, 373)
        await until('bool(renpy.get_screen("chapter_end"))')
        resumed = await value(STATE)
        assert resumed["scene"] == "annual_remembrance" and resumed["visited"] == list(SCENES)
        assert not errors, errors
        print(f"Browser {expected_version} passed all 32 scenes: save/load, ordered reveals, age/clothing, rain, grief, complete ending, Credits, reload and Continue; no engine/page errors.", flush=True)
        await browser.close()

        # Match the original embedded-preview failure: no WebGL and no input.
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
        print("Unsupported graphics passed: useful fallback appears before any engine or game download.", flush=True)
        await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    asyncio.run(check(parser.parse_args().url))
