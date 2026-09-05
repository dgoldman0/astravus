#!/usr/bin/env python3
"""Capture focused reader-control checks against an actual exported web build.

Uses real keyboard/mouse events. The Ren'Py bridge reads visible focus geometry,
state and text; it does not invoke menu actions or inject story progress. A fresh
browser context isolates the temporary saves and preferences from player data.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

from playwright.async_api import async_playwright

PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = PROJECT / "test-results/usability"


async def check(url: str, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    report = {"url": url, "started_utc": datetime.now(timezone.utc).isoformat(),
              "method": "Real Chromium keyboard and mouse events with read-only engine observations",
              "checks": [], "captures": [], "errors": []}
    build_path = PROJECT / "build/release-builds.json"
    if build_path.exists():
        report["web_build_record"] = json.loads(build_path.read_text()).get("builds", {}).get("web")
    report["web_artifact_hashes"] = {
        str(path.relative_to(PROJECT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in [PROJECT / "build/web.zip", PROJECT / "build/web/game.zip", PROJECT / "build/web/index.html"]
        if path.exists()
    }
    report_path = out / "browser-usability.json"

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(args=["--enable-unsafe-swiftshader", "--use-angle=swiftshader"])
        context = await browser.new_context(viewport={"width": 1280, "height": 720})
        page = await context.new_page()
        page.on("pageerror", lambda error: report["errors"].append(str(error)))
        page.on("console", lambda message: report["errors"].append(message.text)
                if "Full traceback:" in message.text or "While running game code:" in message.text else None)

        async def value(expression):
            return await asyncio.wait_for(page.evaluate(
                "expression => window.renpy_get(expression)", f"eval({ascii(expression)})"), 45)

        async def execute(code):
            return await asyncio.wait_for(page.evaluate(
                "code => window.renpy_exec(code)", f"exec({ascii(code)})"), 45)

        async def until(expression, seconds=35):
            async with asyncio.timeout(seconds):
                while not await value(expression):
                    assert not report["errors"], report["errors"]
                    await asyncio.sleep(.12)
            await asyncio.sleep(.3)

        async def text_of(screen):
            return await execute(f'''result = []
renpy.get_screen({screen!r}).visit_all(lambda item, out=result: out.append(item.get_all_text()) if isinstance(item, renpy.text.text.Text) else None)''')

        async def buttons(screen):
            return await execute(f'''result = []
def _usability_button_info(item, out=result):
    if not isinstance(item, renpy.display.behavior.Button):
        return
    texts = []
    item.visit_all(lambda child, out=texts: out.append(child.get_all_text()) if isinstance(child, renpy.text.text.Text) else None)
    out.append(dict(text=texts, sensitive=bool(item.is_sensitive())))
renpy.get_screen({screen!r}).visit_all(_usability_button_info)''')

        async def rects(screen, label):
            return await execute(f'''result = []
widgets = set()
renpy.get_screen({screen!r}).visit_all(lambda item, out=widgets: out.add(id(item)))
for focus in renpy.display.focus.focus_list:
    if renpy.display.interface.trans_pause or renpy.display.interface.get_ongoing_transition():
        continue
    if id(focus.widget) not in widgets or not isinstance(focus.widget, renpy.display.behavior.Button) or focus.x is None:
        continue
    texts = []
    focus.widget.visit_all(lambda item, out=texts: out.append(item.get_all_text()) if isinstance(item, renpy.text.text.Text) else None)
    if {label!r} in texts:
        result.append([focus.x, focus.y, focus.w, focus.h])''')

        async def click(screen, label, activate=True):
            await until(f'bool(renpy.get_screen({screen!r}))')
            rectangles = []
            for _ in range(40):
                rectangles = await rects(screen, label)
                if rectangles:
                    break
                await asyncio.sleep(.15)
            assert rectangles, f"No active rendered {label!r} button on {screen}"
            x, y, w, h = rectangles[0]
            width, height = await value("[config.screen_width, config.screen_height]")
            viewport = page.viewport_size
            assert 0 <= x < width and 0 <= y < height and x + w <= width + 1 and y + h <= height + 1, (label, rectangles)
            px = (x + w / 2) * viewport["width"] / width
            py = (y + h / 2) * viewport["height"] / height
            if activate:
                await page.mouse.click(px, py)
            else:
                await page.mouse.move(px, py)
            await asyncio.sleep(.15)

        async def capture(name, screen=None):
            await asyncio.sleep(.4)
            viewport = page.viewport_size
            filename = f"{viewport['width']}x{viewport['height']}-{name}.png"
            await page.screenshot(path=str(out / filename))
            item = {"file": filename, "viewport": viewport}
            if screen:
                item["visible_text"] = await text_of(screen)
                item["buttons"] = await buttons(screen)
            report["captures"].append(item)
            print(f"Captured {filename}", flush=True)

        async def focused_text():
            return await execute('''result = []
widget = renpy.display.focus.get_focused()
if widget:
    widget.visit_all(lambda item, out=result: out.append(item.get_all_text()) if isinstance(item, renpy.text.text.Text) else None)''')

        async def story_state():
            return await value('dict(scene=scene_key, visited=list(visited_scenes), text=(_history_list[-1].what if _history_list else ""), lost=joren_lost, people=people_names(), glossary=glossary_entries())')

        async def back_to_story(screen, keyboard=False):
            if keyboard:
                await page.keyboard.press("Escape")
            else:
                await click(screen, "Return")
            await until('bool(renpy.get_screen("say")) and not renpy.context()._menu')

        try:
            await page.goto(url)
            await page.wait_for_function('typeof window.renpy_get === "function"', timeout=90000)
            await until('main_menu and bool(renpy.get_screen("main_menu"))')
            report["config_version"] = await value("config.version")
            await capture("title", "main_menu")

            # Arrow keys navigate Ren'Py focus; Tab toggles skip and is not focus-next.
            await page.mouse.move(1270, 10)
            trace = []
            for _ in range(12):
                await page.keyboard.press("ArrowDown")
                await asyncio.sleep(.12)
                trace.append(await focused_text())
                if "Load" in trace[-1]:
                    break
            assert trace and "Load" in trace[-1], trace
            await capture("keyboard-focus-load", "main_menu")
            await page.keyboard.press("Enter")
            await until('bool(renpy.get_screen("load"))')
            report["checks"].append({"check": "arrow-focus-enter-activation", "focus_trace": trace, "result": "pass"})
            await click("load", "1")
            empty = [b for b in await buttons("load") if "Empty slot" in b["text"]]
            assert len(empty) == 6 and all(not b["sensitive"] for b in empty), empty
            await capture("empty-load", "load")
            await page.keyboard.press("Escape")
            await until('main_menu and bool(renpy.get_screen("main_menu"))')
            report["checks"].append({"check": "fresh-load-empty-disabled-and-escape", "empty_slots": len(empty), "result": "pass"})

            await click("main_menu", "Begin Book I")
            await until('bool(renpy.get_screen("chapter_card"))')
            await page.keyboard.press("Enter")
            await until('bool(renpy.get_screen("say"))')
            initial = await story_state()
            assert initial["people"] == ["Cali"] and initial["glossary"] == {} and not initial["lost"], initial
            await capture("initial-story", "quick_menu")

            # Inspect both native menu scale and a smaller 16:9 browser window.
            for width, height in [(1280, 720), (960, 540)]:
                await page.set_viewport_size({"width": width, "height": height})
                await asyncio.sleep(.6)
                for screen, label in [("people", "People"), ("glossary", "Glossary"), ("history", "History")]:
                    await click("quick_menu", label)
                    await until(f'bool(renpy.get_screen({screen!r}))')
                    texts = await text_of(screen)
                    if screen == "people":
                        assert await value('people_names() == ["Cali"] and familiar_names() == []')
                        assert not any("Joren" in text or "Cassia" in text for text in texts), texts
                    elif screen == "glossary":
                        assert any("No terms yet" in text for text in texts), texts
                        assert not any("Transcendence" in text or "Astraviin" in text for text in texts), texts
                    await capture(screen, screen)
                    await back_to_story(screen, keyboard=screen == "history")
                    assert await story_state() == initial

                await click("quick_menu", "Settings")
                await until('bool(renpy.get_screen("preferences"))')
                await capture("settings-default" if width == 1280 else "settings-enabled", "preferences")
                if width == 1280:
                    for label, field in [("Larger dialogue text", "large_text"), ("Solid dialogue background", "high_contrast"), ("Reduced motion", "reduced_motion")]:
                        old = await value(f"persistent.{field}")
                        await click("preferences", label)
                        assert await value(f"persistent.{field}") != old
                    await capture("settings-enabled", "preferences")
                await click("preferences", "How to read")
                await until('bool(renpy.get_screen("help"))')
                await capture("help", "help")
                await back_to_story("help")
                assert await story_state() == initial
                await capture("large-solid-dialogue", "quick_menu")

                await click("quick_menu", "Chapters")
                await until('bool(renpy.get_screen("dev_chapters"))')
                await capture("chapters", "dev_chapters")
                await click("dev_chapters", "25 · The news")
                await until('bool(renpy.get_screen("chapter_spoiler_warning"))')
                await capture("chapter-warning", "chapter_spoiler_warning")
                if width == 1280:
                    await click("chapter_spoiler_warning", "Go back")
                else:
                    await page.keyboard.press("Escape")
                await until('not renpy.get_screen("chapter_spoiler_warning")')
                await back_to_story("dev_chapters")
                assert await story_state() == initial

                await page.keyboard.press("Escape")
                await until('bool(renpy.get_screen("pause_menu"))')
                await capture("pause", "pause_menu")
                await click("pause_menu", "Keep reading")
                await until('bool(renpy.get_screen("say")) and not renpy.context()._menu')
                assert await story_state() == initial
            report["checks"].append({"check": "early-knowledge-menu-return-warning-cancel-layouts", "sizes": [[1280,720],[960,540]], "story_unchanged": True, "result": "pass"})

            # Numbered/quick/automatic pages, disabled empty loads, actual save and overwrite No.
            await click("quick_menu", "Load")
            await click("load", "Automatic")
            assert await value('FileCurrentPage() == "auto"')
            await capture("automatic-load", "load")
            await click("load", "Save")
            await until('bool(renpy.get_screen("save"))')
            assert await value('FileCurrentPage() == "1"')
            for label in ["Quick", "2", "3"]:
                await click("save", label)
                expected = "quick" if label == "Quick" else label
                assert await value(f'FileCurrentPage() == {expected!r}')
            save_empty = [b for b in await buttons("save") if "Empty slot" in b["text"]]
            assert len(save_empty) == 6 and all(b["sensitive"] for b in save_empty), save_empty
            await capture("empty-save-page3", "save")
            await click("save", "Empty slot")
            await until('renpy.can_load("3-1")')
            before_save = await value('dict(time=renpy.slot_mtime("3-1"), metadata=renpy.slot_json("3-1"))')
            label = await value('FileTime(1, format="%b %d · %H:%M", empty="Empty slot")')
            await click("save", label)
            await until('bool(renpy.get_screen("confirm"))')
            await capture("overwrite-confirm", "confirm")
            await click("confirm", "No")
            await until('not renpy.get_screen("confirm")')
            after_save = await value('dict(time=renpy.slot_mtime("3-1"), metadata=renpy.slot_json("3-1"))')
            assert after_save == before_save
            await click("save", label, activate=False)
            await page.keyboard.press("Delete")
            await until('bool(renpy.get_screen("confirm"))')
            await capture("delete-confirm", "confirm")
            await click("confirm", "No")
            await until('not renpy.get_screen("confirm")')
            assert await value('dict(time=renpy.slot_mtime("3-1"), metadata=renpy.slot_json("3-1"))') == before_save
            await back_to_story("save")
            assert await story_state() == initial
            await click("quick_menu", "Load")
            await click("load", "3")
            await capture("load-saved-page3", "load")
            await click("load", label)
            await until('bool(renpy.get_screen("confirm"))')
            await page.keyboard.press("Escape")
            await until('not renpy.get_screen("confirm")')
            await back_to_story("load")
            assert await story_state() == initial
            report["checks"].append({"check": "save-load-pages-and-negative-confirmations", "save_unchanged_after_no": True, "story_unchanged": True, "result": "pass"})

            # Exercise the opt-out with a real later-chapter selection, then theme controls.
            await click("quick_menu", "Settings")
            await click("preferences", "Chapter spoiler warnings: On")
            assert not await value("persistent.chapter_spoiler_warnings")
            await capture("warning-optout", "preferences")
            await back_to_story("preferences")
            await click("quick_menu", "Chapters")
            final_label = await value('"32 · " + BOOK_SCENES[-1][1]')
            await click("dev_chapters", final_label)
            await until('scene_key == "annual_remembrance" and bool(renpy.get_screen("say"))')
            assert not await value('bool(renpy.get_screen("chapter_spoiler_warning"))')
            later = await story_state()
            await click("quick_menu", "People")
            await until('bool(renpy.get_screen("people"))')
            await capture("populated-people", "people")
            for familiar in await value("familiar_names()"):
                await click("people", familiar)
                await capture("familiar-" + familiar.lower(), "people")
            await back_to_story("people")
            assert await story_state() == later
            await click("quick_menu", "Glossary")
            await until('bool(renpy.get_screen("glossary"))')
            await capture("populated-glossary", "glossary")
            for entry in (await value("list(glossary_entries().values())"))[:2]:
                await click("glossary", entry["title"])
                await capture("glossary-" + entry["title"].lower().replace(" ", "-"), "glossary")
            await back_to_story("glossary")
            assert await story_state() == later
            for _ in range(24):
                if await value('bool(renpy.get_screen("book_afterword"))'):
                    break
                await page.keyboard.press("Space")
                await asyncio.sleep(.25)
            await until('bool(renpy.get_screen("book_afterword"))')
            await capture("afterword", "book_afterword")
            await click("book_afterword", "Play closing theme")
            await until('bool(renpy.get_screen("closing_theme"))')
            await until('renpy.get_widget("closing_theme", "montage").position() > .5')
            assert await value('renpy.get_widget("closing_theme", "montage").reduced_motion')
            await capture("theme-playing", "closing_theme")
            await click("closing_theme", "Pause")
            assert await value('renpy.music.get_pause(channel="closing_theme")')
            await capture("theme-paused", "closing_theme")
            await page.set_viewport_size({"width": 1280, "height": 720})
            await capture("theme-paused", "closing_theme")
            await page.keyboard.press("Space")
            await until('not renpy.music.get_pause(channel="closing_theme")')
            await page.keyboard.press("Escape")
            await until('bool(renpy.get_screen("chapter_end"))')
            await capture("ending", "chapter_end")
            await click("chapter_end", "Replay closing theme")
            await until('bool(renpy.get_screen("closing_theme"))')
            await click("closing_theme", "Skip closing theme")
            await until('bool(renpy.get_screen("chapter_end"))')
            assert not await value('renpy.music.is_playing(channel="closing_theme")')
            report["checks"].append({"check": "warning-optout-reduced-motion-theme-pause-space-escape-skip", "result": "pass"})
            assert not report["errors"], report["errors"]
            for filename, expected in report["web_artifact_hashes"].items():
                assert hashlib.sha256((PROJECT / filename).read_bytes()).hexdigest() == expected, "Web artifact changed during usability inspection"
            report["result"] = "pass"
            report["manual_review_required"] = "Inspect the captured layouts, focus highlight, reading contrast and control discoverability before recording the overall reader-usability row."
        except Exception as error:
            report["result"] = "fail"
            report["failure"] = repr(error)
            await page.screenshot(path=str(out / "failure.png"))
            raise
        finally:
            report["finished_utc"] = datetime.now(timezone.utc).isoformat()
            report_path.write_text(json.dumps(report, indent=2) + "\n")
            await context.close()
            await browser.close()
    print(f"Focused browser usability checks passed; inspect captures in {out}.", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    asyncio.run(check(args.url, args.output.resolve()))
