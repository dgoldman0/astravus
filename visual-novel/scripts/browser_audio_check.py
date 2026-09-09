#!/usr/bin/env python3
"""Check real browser audio replacement, normal fades, and saved rain playback."""
import argparse
import ast
import asyncio
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from playwright.async_api import async_playwright

from project import PROJECT, SDK, WEB_AUDIO_MEMBER, patched_web_audio

SMOKE = PROJECT / "scripts/browser_smoke.py"
STATE = '''dict(scene=scene_key, text=_history_list[-1].what,
    channels={name: dict(file=renpy.music.get_playing(channel=name),
        position=renpy.music.get_pos(channel=name), paused=renpy.music.get_pause(channel=name))
        for name in ("music", "ambience")})'''
RAIN_PLAYING = '''scene_key == "treehouse_remembrance" and all(
    renpy.music.get_playing(channel=name) == filename and (renpy.music.get_pos(channel=name) or 0) > .1
    for name, filename in (("music", "audio/remembrance_rain.ogg"), ("ambience", "audio/rain.ogg")))'''
TRACE = '''globalThis.astravusAudioTrace = [];
const originalFadeout = renpyAudio.fadeout;
renpyAudio.fadeout = function(channel, delay) {
    const before = {file: renpyAudio.playing_name(channel), position: renpyAudio.get_pos(channel)};
    const result = originalFadeout(channel, delay);
    globalThis.astravusAudioTrace.push({channel, delay, before,
        after: {file: renpyAudio.playing_name(channel), position: renpyAudio.get_pos(channel)}});
    return result;
};'''


async def check(url, output):
    output.mkdir(parents=True, exist_ok=True)
    smoke_source = SMOKE.read_text()
    owner = next(node for node in ast.parse(smoke_source).body
                 if isinstance(node, ast.AsyncFunctionDef) and node.name == "check")
    # Reuse the complete playthrough's actual-pointer helper without duplicating
    # its focus/transition handling or substituting Ren'Py actions for clicks.
    functions = {node.name: ast.get_source_segment(smoke_source, node) for node in ast.walk(owner)
                 if isinstance(node, ast.AsyncFunctionDef) and node.name in ("value", "execute", "click_button")}
    expected_audio_hash = hashlib.sha256(patched_web_audio((SDK / WEB_AUDIO_MEMBER).read_bytes())).hexdigest()
    cases = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(args=["--enable-unsafe-swiftshader", "--use-angle=swiftshader"])
        for name, reduced, settled in (("rapid", True, False), ("normal-fades", False, True)):
            context = await browser.new_context(viewport={"width": 1280, "height": 720})
            page = await context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            namespace = {"page": page, "errors": errors, "asyncio": asyncio}
            for helper in ("value", "execute", "click_button"):
                exec(compile(functions[helper], str(SMOKE) + ":" + helper, "exec"), namespace)
            value, execute, click = (namespace[helper] for helper in ("value", "execute", "click_button"))

            async def until(expression, seconds=15):
                try:
                    async with asyncio.timeout(seconds):
                        while not await value(expression):
                            assert not errors, errors
                            await asyncio.sleep(.1)
                except TimeoutError:
                    state = await value(STATE)
                    (output / (name + "-failure.json")).write_text(json.dumps(state, indent=2) + "\n")
                    raise AssertionError((expression, state)) from None
                await asyncio.sleep(.25)

            namespace["until"] = until
            await page.goto(url)
            await page.wait_for_function('typeof window.renpy_get === "function"', timeout=90000)
            await until('bool(renpy.get_screen("main_menu"))')
            loaded_hash = await value('__import__("hashlib").sha256(renpy.loader.load("_audio.js").read()).hexdigest()')
            assert loaded_hash == expected_audio_hash, ("Browser did not load the patched engine", loaded_hash)
            await execute(f'persistent.chapter_spoiler_warnings=False\npersistent.reduced_motion={reduced!r}\npreferences.text_cps=0')
            await execute('import emscripten\nemscripten.run_script(' + repr(TRACE) + ')')
            await click("main_menu", "Chapters")
            await until('bool(renpy.get_screen("dev_chapters"))')
            title = await value('dict(BOOK_SCENES)["mural_remembrance"]')
            await click("dev_chapters", "30 · " + title)
            await until('scene_key == "mural_remembrance" and bool(renpy.get_screen("say")) and not renpy.context()._menu')
            if settled:
                await until('renpy.music.get_playing(channel="ambience") == "audio/garden_air.ogg" and (renpy.music.get_pos(channel="ambience") or 0) > 1')
            steps = []
            for _ in range(30):
                state = await value(STATE)
                steps.append(state)
                if state["scene"] == "treehouse_remembrance":
                    break
                assert state["scene"] == "mural_remembrance", state
                await page.keyboard.press("Space")
                await asyncio.sleep(.8 if settled else .06)
            else:
                raise AssertionError("Treehouse remembrance was not reached")
            first = await value(STATE)
            started = asyncio.get_running_loop().time()
            await until(RAIN_PLAYING, seconds=8)
            elapsed = asyncio.get_running_loop().time() - started
            reached = await value(STATE)
            await page.screenshot(path=str(output / (name + "-rain.png")))
            trace = json.loads(await value('__import__("emscripten").run_script_string("JSON.stringify(globalThis.astravusAudioTrace)")'))
            garden_fades = [event for event in trace if event["before"]["file"] == "audio/garden_air.ogg" and event["delay"] == 2]
            assert garden_fades, trace
            if settled:
                assert any(event["before"]["position"] > 0 and event["after"]["file"] == "audio/garden_air.ogg"
                           for event in garden_fades), ("Normal fade was replaced by an immediate stop", garden_fades)

            # Save in the rainy scene, move to a different ambience, then load
            # through the real menus. Both score and ambience must resume.
            await click("quick_menu", "Save")
            await until('bool(renpy.get_screen("save"))')
            await click("save", "Empty slot")
            await until('renpy.can_load("1-1")')
            await page.keyboard.press("Escape")
            await until('bool(renpy.get_screen("say")) and not renpy.context()._menu')
            for _ in range(35):
                if await value('scene_key == "annual_remembrance"'):
                    break
                await page.keyboard.press("Space")
                await asyncio.sleep(.15)
            await until('scene_key == "annual_remembrance" and renpy.music.get_playing(channel="ambience") == "audio/plaza_air.ogg"')
            await click("quick_menu", "Load")
            await until('bool(renpy.get_screen("load"))')
            label = await value('FileTime(1, format="%b %d · %H:%M", empty="Empty slot")')
            await click("load", label)
            await until('bool(renpy.get_screen("confirm"))')
            await click("confirm", "Yes")
            await until(RAIN_PLAYING, seconds=8)
            await until('not renpy.context()._menu')
            restored = await value(STATE)
            assert restored["text"] == reached["text"], (reached, restored)
            assert not errors, errors
            cases.append({"case": name, "loaded_audio_sha256": loaded_hash, "steps": steps,
                          "first_rain_scene": first, "playing_after_seconds": elapsed,
                          "playing": reached, "fadeout_trace": trace, "restored": restored, "errors": errors})
            print(f"Browser audio {name}: score and rain playing in {elapsed:.2f}s; save/load restores both.", flush=True)
            await context.close()
        version = browser.version
        await browser.close()
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(), "url": url, "browser": version,
              "passed": True, "cases": cases, "smoke_sha256": hashlib.sha256(smoke_source.encode()).hexdigest(),
              "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "web_zip_sha256": hashlib.sha256((PROJECT / "build/web.zip").read_bytes()).hexdigest()}
    (output / "browser-audio.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8000/?preview=0.1-alpha")
    parser.add_argument("--output", type=Path, default=PROJECT / "test-results/browser-audio")
    args = parser.parse_args()
    asyncio.run(check(args.url, args.output))
