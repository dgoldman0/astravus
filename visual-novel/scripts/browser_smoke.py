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
    afterword=bool(renpy.get_screen("book_afterword")),
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
    speaker=(_history_list[-1].who if _history_list else None),
    portrait=(dialogue_portrait(_history_list[-1].who) if _history_list else None),
    portrait_visible=bool(renpy.get_widget("say", "speaker_portrait")),
    visible_actors=sorted(tag for tag in set(SPEAKER_TAGS.values()) if renpy.showing(tag)),
    people=people_names(),
    familiars=familiar_names(),
    visible_familiars=[name for name in FAMILIAR_PROFILES if renpy.showing(name.lower())],
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
            # The SDK bridge uses btoa, then decodes as UTF-8. Send ASCII Python
            # source so dialogue and date labels with Unicode survive the trip.
            wrapped = f"eval({ascii(expression)})"
            return await asyncio.wait_for(page.evaluate("expression => window.renpy_get(expression)", wrapped), 45)

        async def execute(code):
            wrapped = f"exec({ascii(code)})"
            return await asyncio.wait_for(page.evaluate("code => window.renpy_exec(code)", wrapped), 45)

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
widgets = set()
renpy.get_screen({screen!r}).visit_all(lambda item, out=widgets: out.add(id(item)))
for focus in renpy.display.focus.focus_list:
    if renpy.display.interface.trans_pause or renpy.display.interface.get_ongoing_transition():
        continue
    if id(focus.widget) not in widgets or not isinstance(focus.widget, renpy.display.behavior.Button) or focus.x is None:
        continue
    texts = []
    focus.widget.visit_all(lambda item, out=texts: out.append(item.get_all_text()) if isinstance(item, renpy.text.text.Text) else None)
    if {label!r} in texts and focus.x is not None:
        result.append([focus.x, focus.y, focus.w, focus.h])'''
            # A screen and its focus rectangles can exist during a transition
            # before the engine accepts input (notably the return-to-title fade).
            for _ in range(30):
                rectangles = await execute(code)
                if rectangles:
                    break
                if errors:
                    raise AssertionError(errors)
                await asyncio.sleep(.1)
            assert rectangles, f"No visible {label!r} button on {screen}"
            x, y, width, height = rectangles[0]
            await page.mouse.click((x + width / 2) * 2 / 3, (y + height / 2) * 2 / 3)

        assert await value("main_menu")
        expected_version = re.search(r'config.version = "([^"]+)"', (PROJECT / "game/options.rpy").read_text()).group(1)
        assert await value("config.version") == expected_version
        assert await value("config.save_directory") == "Astravus-Book-I"
        assert await value("persistent.chapter_spoiler_warnings and not chapter_read_progress()[0]")
        await page.screenshot(path=str(OUT / "browser-title.png"))
        await click_button("main_menu", "Chapters")
        await until('bool(renpy.get_screen("dev_chapters"))')
        await click_button("dev_chapters", "25 · The news")
        await until('bool(renpy.get_screen("chapter_spoiler_warning"))')
        await page.screenshot(path=str(OUT / "browser-chapter-spoiler-warning.png"))
        assert await value('main_menu and visited_scenes == [] and dev_chapter_target == "first_memory"')
        await page.keyboard.press("Escape")
        await until('not renpy.get_screen("chapter_spoiler_warning")')
        await click_button("dev_chapters", "Return")
        await until("main_menu and bool(renpy.get_screen('main_menu'))")
        await click_button("main_menu", "Settings")
        await until('bool(renpy.get_screen("preferences"))')
        await click_button("preferences", "Chapter spoiler warnings: On")
        assert not await value("persistent.chapter_spoiler_warnings")
        await page.reload()
        await page.wait_for_function('typeof window.renpy_get === "function"', timeout=90000)
        await until("main_menu")
        assert not await value("persistent.chapter_spoiler_warnings")
        await click_button("main_menu", "Settings")
        await until('bool(renpy.get_screen("preferences"))')
        await click_button("preferences", "Chapter spoiler warnings: Off")
        await page.screenshot(path=str(OUT / "browser-settings.png"))
        await click_button("preferences", "Return")
        await until("main_menu and bool(renpy.get_screen('main_menu'))")
        # A fresh browser context has no compatible Book I Continue entry.
        await page.mouse.click(220, 373)
        await until('bool(renpy.get_screen("chapter_card"))')
        await page.keyboard.press("Enter")
        await until('bool(renpy.get_screen("say"))')
        initial = await value(STATE)
        assert initial["cg"] == "first_memory" and initial["calista"] is None, initial
        assert not initial["known"] and not initial["lost"]
        assert initial["visited"] == ["first_memory"]
        assert initial["people"] == ["Cali"]
        assert initial["familiars"] == [] and initial["visible_familiars"] == []
        await page.screenshot(path=str(OUT / "browser-first-memory.png"))
        await execute("preferences.text_cps = 0\npersistent.reduced_motion = True")
        captured = {"first_memory"}
        entry_states = {"first_memory": initial}
        observed = []
        first_flute = False
        practiced_flute = False
        cassia_aged = False
        before_echo_reveal = False
        after_echo_reveal = False
        loss_seen = False
        manual_save_checked = False
        portrait_scenes = set()
        people_checked = {"Cali"}
        familiars_checked = False
        familiar_scenes = set()
        flute_events = []
        afterword_seen = False
        people_fragments = {
            "Maia": "patient, practical care", "Kael": "older brother",
            "Arin": "biomechanical interfaces", "Selene": "listen, breathe",
            "Dorian": "oral histories", "Lyra": "younger sister",
            "Sage": "through transitions", "Cassia": "storyteller",
            "Thalia": "resolve disagreements", "Lyron": "agricultural systems",
            "Joren": "eager explorer", "Soren": "systems designer", "Kaleb": "explorer",
        }
        expected_backgrounds = {
            "garden": "garden_close", "plant_disagreement": "garden_pond",
            "workshop_first": "workshop", "music_first": "music_room",
            "dorian_stories": "library", "sage_story": "sage_room",
            "tree_echoes": "echoes", "pond_scare": "garden_pond",
            "soup_experiment": "family_home", "festival_lights": "festival",
            "meeting_cassia": "community_courtyard", "meeting_joren": "construction_path",
            "treehouse": "treehouse", "rain_refuge": "treehouse_rain",
            "outer_exploration": "construction_room",
            "dome_ascent": "dome", "treehouse_dispute": "treehouse",
            "family_grief": "home_dusk", "painting_grief": "family_home",
            "cassia_grief": "treehouse", "community_memorial": "memorial_plaza",
            "mural_remembrance": "memory_mural", "treehouse_remembrance": "treehouse_memory",
            "annual_remembrance": "remembrance_plaza",
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
            if state["afterword"]:
                assert await value('renpy.get_widget("book_afterword", "itch_link").action.url == ITCH_URL')
                assert await value('chapter_read_progress()[0] == set(BOOK_SCENE_KEYS)')
                await page.screenshot(path=str(OUT / "browser-afterword.png"))
                afterword_seen = True
                await click_button("book_afterword", "Finish Book I")
                await until('bool(renpy.get_screen("chapter_end"))')
                continue
            key = state["scene"]
            if not observed or observed[-1] != key:
                observed.append(key)
                entry_states.setdefault(key, state)
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
                assert not (state["portrait"] or "").startswith("joren "), state
            if state["say"] and state["portrait"]:
                assert state["portrait_visible"], state
                if key not in portrait_scenes:
                    await page.screenshot(path=str(OUT / f"browser-portrait-{key}.png"))
                portrait_scenes.add(key)
            if state["say"] and state["speaker"] not in (None, "Calista · remembering"):
                speaker_tag = state["speaker"].lower() if state["speaker"] != "Cali" else "calista"
                assert speaker_tag in state["visible_actors"] or state["portrait_visible"] or state["cg"], ("Current speaker has no depiction", state)
            if state["number"] >= 20:
                assert state["stage"] == "later", state
            if state["say"] and state["speaker"] in people_fragments and state["speaker"] not in people_checked:
                speaker = state["speaker"]
                assert speaker in state["people"], ("Current speaker missing from People", state)
                await click_button("quick_menu", "People")
                await until('bool(renpy.get_screen("people"))')
                await click_button("people", speaker)
                displayed = await value('renpy.get_widget("people", "people_description").get_all_text()')
                assert people_fragments[speaker] in displayed, (speaker, displayed)
                await page.screenshot(path=str(OUT / f"browser-people-{speaker.lower()}.png"))
                await click_button("people", "Return")
                await until('bool(renpy.get_screen("say")) and not renpy.context()._menu')
                people_checked.add(speaker)
            assert set(state["people"]) == people_checked, ("People unlocked out of encounter order", state, people_checked)
            if state["visible_familiars"]:
                if key not in familiar_scenes:
                    await page.screenshot(path=str(OUT / f"browser-familiars-{key}.png"))
                familiar_scenes.add(key)
            if state["text"].startswith("Shadow watched from the sofa.") and not familiars_checked:
                assert state["familiars"] == ["Shadow", "Barkley", "Nibble"], state
                assert state["visible_familiars"] == state["familiars"], state
                await click_button("quick_menu", "People")
                await until('bool(renpy.get_screen("people"))')
                for name, fragment in (("Shadow", "green eyes"), ("Barkley", "golden retriever"), ("Nibble", "little rat")):
                    await click_button("people", name)
                    displayed = await value('renpy.get_widget("people", "people_description").get_all_text()')
                    assert fragment in displayed and await value('bool(renpy.get_widget("people", "familiar_portrait"))'), (name, displayed)
                    await page.screenshot(path=str(OUT / f"browser-people-{name.lower()}.png"))
                await click_button("people", "Return")
                await until('bool(renpy.get_screen("say")) and not renpy.context()._menu')
                familiars_checked = True
            assert state["familiars"] == (["Shadow", "Barkley", "Nibble"] if familiars_checked else []), state
            if state["sound"] in ("audio/flute_attempt.wav", "audio/flute_first.wav", "audio/flute_practice.wav"):
                if not flute_events or flute_events[-1] != state["sound"]:
                    flute_events.append(state["sound"])
            if state["text"] == "There was a note in there. I heard it.":
                assert flute_events == ["audio/flute_attempt.wav"], flute_events
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
                        # The previous ambience keeps playing during its fadeout.
                        # Let the scheduled rain begin before judging the scene.
                        if state["ambience"] != "audio/rain.ogg":
                            await until('renpy.music.get_playing(channel="ambience") == "audio/rain.ogg"', seconds=10)
                            state = await value(STATE)
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
        assert {"music_first", "sage_story", "pond_scare", "soup_experiment", "rain_refuge", "dome_ascent", "treehouse_remembrance"} <= portrait_scenes, portrait_scenes
        assert people_checked == {"Cali", *people_fragments}, people_checked
        assert familiars_checked and {"first_memory", "family_rhythm", "tree_echoes", "waterwheel", "outer_exploration", "treehouse_dispute", "painting_grief"} <= familiar_scenes, familiar_scenes
        assert flute_events == ["audio/flute_attempt.wav", "audio/flute_first.wav", "audio/flute_practice.wav"], flute_events
        assert afterword_seen
        await page.screenshot(path=str(OUT / "browser-end.png"))
        # End menus, persistence and Continue must remain usable after reload.
        await click_button("chapter_end", "Credits")
        await until('bool(renpy.get_screen("about"))')
        assert await value('renpy.get_widget("about", "itch_link").action.url == "https://arcadiumgames.itch.io/astravus-calista"')
        await page.screenshot(path=str(OUT / "browser-credits.png"))
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
        assert set(resumed["people"]) == people_checked, resumed
        assert resumed["familiars"] == ["Shadow", "Barkley", "Nibble"], resumed
        (PROJECT / "test-results/chapter-entrances.json").write_text(json.dumps({"version": expected_version, "entrances": entry_states}, indent=2) + "\n")
        print(f"Browser {expected_version} passed all 32 scenes: all 14 People entries and 3 illustrated familiars, familiar staging in 7 scenes, three flute cues in story order, save/load, ordered reveals, age/clothing, rain, grief, complete ending, Credits, reload and Continue; no engine/page errors.", flush=True)

        # Compare every jump with the same entrance reached through normal play.
        # Reverse order exercises removal of later encounters and revelations.
        await click_button("chapter_end", "Return to title")
        await until("main_menu")
        await click_button("main_menu", "Chapters")
        await until('bool(renpy.get_screen("dev_chapters"))')
        await page.screenshot(path=str(OUT / "browser-dev-chapters.png"))
        titles = dict(await value("BOOK_SCENES"))
        compared_fields = (
            "scene", "number", "visited", "known", "lost", "stage",
            "met_cassia", "met_joren", "bg", "cg", "calista", "cassia", "joren",
            "text", "speaker", "portrait", "people", "familiars",
            "visible_actors", "visible_familiars",
        )
        for index, key in enumerate(reversed(SCENES)):
            if index:
                await click_button("quick_menu", "Chapters")
                await until('bool(renpy.get_screen("dev_chapters"))')
            label = f"{SCENES.index(key) + 1:02d} · {titles[key]}"
            await click_button("dev_chapters", label)
            if key == "first_memory":
                await until('bool(renpy.get_screen("chapter_card"))')
                await page.keyboard.press("Enter")
            await until(f'scene_key == {key!r} and bool(_history_list) and bool(renpy.get_screen("say")) and not renpy.context()._menu')
            jumped = await value(STATE)
            expected = entry_states[key]
            differences = {field: (expected[field], jumped[field]) for field in compared_fields if expected[field] != jumped[field]}
            assert not differences, ("Chapter jump differs from normal play", key, differences)
            if key in ("family_grief", "music_first", "kaleb_walk", "first_memory"):
                await page.screenshot(path=str(OUT / f"browser-jump-{key}.png"))
            print(f"Browser chapter jump {key}: matches normal entrance", flush=True)
        assert not errors, errors
        print("All 32 chapter jumps passed against normal-play entrances, including backwards story state and character visibility.", flush=True)
        # Simulate unread chapters using the same per-line record as an older
        # installation. A completed-book flag and fabricated visited_scenes must
        # not suppress warnings for gaps in what has actually been read.
        await execute("for identifiers in CHAPTER_DIALOGUE_IDS.values():\n    for identifier in identifiers:\n        renpy.mark_translation_unseen(identifier)")
        await click_button("quick_menu", "Chapters")
        await until('bool(renpy.get_screen("dev_chapters"))')
        await click_button("dev_chapters", "25 · The news")
        await until('bool(renpy.get_screen("chapter_spoiler_warning"))')
        await click_button("chapter_spoiler_warning", "Jump anyway")
        await until('scene_key == "loss" and bool(renpy.get_screen("say")) and not renpy.context()._menu')
        assert await value('visited_scenes == list(BOOK_SCENE_KEYS[:25]) and chapter_warning_needed("family_grief") and chapter_warning_needed("garden")')
        before_cancel = await value(STATE)
        await click_button("quick_menu", "Chapters")
        await until('bool(renpy.get_screen("dev_chapters"))')
        await click_button("dev_chapters", "26 · What comfort can do")
        await until('bool(renpy.get_screen("chapter_spoiler_warning"))')
        await click_button("chapter_spoiler_warning", "Go back")
        await click_button("dev_chapters", "Return")
        await until('not renpy.context()._menu')
        after_cancel = await value(STATE)
        assert all(after_cancel[field] == before_cancel[field] for field in compared_fields), (before_cancel, after_cancel)
        await click_button("quick_menu", "Settings")
        await until('bool(renpy.get_screen("preferences"))')
        await click_button("preferences", "Chapter spoiler warnings: On")
        await click_button("preferences", "Return")
        await until('not renpy.context()._menu')
        await click_button("quick_menu", "Chapters")
        await until('bool(renpy.get_screen("dev_chapters"))')
        await click_button("dev_chapters", "26 · What comfort can do")
        await until('scene_key == "family_grief" and bool(renpy.get_screen("say")) and not renpy.context()._menu')
        assert not await value('bool(renpy.get_screen("chapter_spoiler_warning"))')
        assert not errors, errors
        print("Alpha polish passed: spoiler confirmation/cancellation, unread gaps after jumps, persistent setting, credits link and afterword.", flush=True)
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
