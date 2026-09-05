# Development-only targeted captures. Excluded from exported builds.
# Run only after the revised environments and their story routing are installed.
# These assertions establish capture/state coverage, not artistic approval.
init python:
    def _environment_review_inputs():
        import hashlib
        from pathlib import Path
        root = Path(config.basedir)
        paths = sorted((root / "game").glob("*.rpy"))
        paths += sorted((root / "game/images").rglob("*.png"))
        return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in paths}

    def _environment_review_begin():
        import os
        renpy.store._environment_review_input_hashes = _environment_review_inputs()
        renpy.store._environment_review_frames = []
        os.makedirs(config.basedir + "/test-results/environment-states", exist_ok=True)

    def _environment_review_note(name):
        renpy.store._environment_review_frames.append({
            "screenshot": name + ".png",
            "scene_key": scene_key,
            "scene_number": scene_number,
            "dialogue": _history_list[-1].what,
            "windows_hidden": bool(_windows_hidden),
            "shown": [" ".join((tag,) + tuple(renpy.get_attributes(tag) or ()))
                      for tag in sorted(renpy.get_showing_tags())],
        })

    def _environment_review_finish():
        import json
        from datetime import datetime, timezone
        from pathlib import Path
        assert _environment_review_inputs() == _environment_review_input_hashes, "Source changed during capture"
        assert len(_environment_review_frames) == 15, "Missing requested view"
        output = Path(config.basedir) / "test-results/environment-states/capture-state.json"
        output.write_text(json.dumps({
            "captured_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "method": "Native Ren'Py chapter navigation and dialogue advancement; H hides UI for support-plane views.",
            "scope": "Eight requested scene states plus the two new project-background states; fifteen captures. Capture coverage is not an artistic acceptance decision.",
            "inputs": _environment_review_input_hashes,
            "captures": _environment_review_frames,
        }, indent=2) + "\n")
        return True

testcase environment_state_review:
    assert screen "main_menu"
    $ persistent.chapter_spoiler_warnings = False
    $ _test.force = True
    $ _test.screenshot_directory = config.basedir + "/test-results/environment-states"
    $ _environment_review_begin()

    click "Chapters"
    click "18 · Our place in the branches"
    advance until eval (_history_list[-1].what.startswith("Our drawings covered the walls."))
    assert eval (scene_key == "treehouse" and renpy.showing("bg treehouse") and renpy.get_screen("say"))
    pause .25
    screenshot "18-first-treehouse-dialogue"
    $ _environment_review_note("18-first-treehouse-dialogue")
    advance until eval (_history_list[-1].what == "Do you think we'll ever outgrow this place?")
    assert eval (renpy.showing("cassia young") and renpy.showing("joren young"))
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "18-first-treehouse-actors"
    $ _environment_review_note("18-first-treehouse-actors")
    keysym "h"

    click "Chapters"
    click "19 · A story under the rain"
    assert eval (scene_key == "rain_refuge" and renpy.showing("bg treehouse_rain") and _history_list[-1].what.startswith("On rainy afternoons,")) timeout 4.0
    pause .25
    screenshot "19-rain-refuge-dialogue"
    $ _environment_review_note("19-rain-refuge-dialogue")
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "19-rain-refuge-room"
    $ _environment_review_note("19-rain-refuge-room")
    keysym "h"

    click "Chapters"
    click "24 · Which way we go"
    advance until eval (_history_list[-1].what.startswith("Barkley sat down and whined softly,"))
    assert eval (scene_key == "treehouse_dispute" and renpy.showing("bg treehouse_later") and all(renpy.showing(tag) for tag in ("shadow", "barkley", "nibble", "calista frustrated", "joren frustrated")))
    pause .25
    screenshot "24-later-dispute-dialogue"
    $ _environment_review_note("24-later-dispute-dialogue")
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "24-later-dispute-support"
    $ _environment_review_note("24-later-dispute-support")
    keysym "h"

    click "Chapters"
    click "28 · Between the two of us"
    advance until eval (_history_list[-1].what == "I miss him.")
    assert eval (scene_key == "cassia_grief" and renpy.showing("bg treehouse_later") and renpy.showing("calista mourning") and renpy.showing("cassia mourning") and not renpy.showing("cg"))
    pause .25
    screenshot "28-cassia-before-cg"
    $ _environment_review_note("28-cassia-before-cg")
    advance until eval (_history_list[-1].what == "I reached for her hand.")
    assert eval (renpy.showing("cg cassia_comfort") and not renpy.showing("calista") and not renpy.showing("cassia"))
    pause .25
    screenshot "28-cassia-comfort-cg"
    $ _environment_review_note("28-cassia-comfort-cg")

    click "Chapters"
    click "31 · The rain returns"
    assert eval (scene_key == "treehouse_remembrance" and renpy.showing("bg treehouse_memory") and _history_list[-1].what.startswith("We brought new drawings to the treehouse,")) timeout 4.0
    pause .25
    screenshot "31-remembrance-dialogue"
    $ _environment_review_note("31-remembrance-dialogue")
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "31-remembrance-room"
    $ _environment_review_note("31-remembrance-room")
    keysym "h"

    click "Chapters"
    click "22 · A place beside us"
    advance until eval (_history_list[-1].what == "Are you going again?")
    assert eval (scene_key == "lyra_included" and renpy.showing("calista older") and renpy.showing("lyra young"))
    pause .25
    screenshot "22-lyra-dialogue"
    $ _environment_review_note("22-lyra-dialogue")

    click "Chapters"
    click "32 · What remains"
    assert eval (scene_key == "annual_remembrance" and renpy.showing("bg remembrance_plaza") and _history_list[-1].what.startswith("Each year, the community gathered")) timeout 4.0
    pause .25
    screenshot "32-annual-remembrance-dialogue"
    $ _environment_review_note("32-annual-remembrance-dialogue")

    click "Chapters"
    click "20 · Something that turns"
    advance until eval (_history_list[-1].what == "If the water pushes here, the whole thing turns.")
    assert eval (scene_key == "waterwheel" and renpy.showing("bg workshop_waterwheel") and renpy.showing("calista older") and renpy.showing("joren older"))
    pause .25
    screenshot "20-workshop-project-dialogue"
    $ _environment_review_note("20-workshop-project-dialogue")

    click "Chapters"
    click "27 · What the hand remembers"
    advance until eval (_history_list[-1].what == "That's his side of the map. He wanted the path to go there.")
    assert eval (scene_key == "painting_grief" and renpy.showing("bg family_home_painting") and all(renpy.showing(tag) for tag in ("shadow", "barkley", "nibble")))
    pause .25
    screenshot "27-painting-project-familiars"
    $ _environment_review_note("27-painting-project-familiars")

    click "Chapters"
    click "25 · The news"
    advance until eval (_history_list[-1].what.startswith("An unexpected malfunction caused"))
    # One dismissal, then no input: allow the real one-second story pause to
    # finish. Repeated `advance until` would dismiss that pause prematurely.
    keysym "K_RETURN"
    pause 1.25
    assert eval (scene_key == "loss" and joren_lost and renpy.showing("bg home_dusk") and renpy.get_screen("say") and _history_list[-1].what.startswith("In our world, where transcendence")) timeout 3.0
    screenshot "25-loss-after-pause-dialogue"
    $ _environment_review_note("25-loss-after-pause-dialogue")
    assert eval (_environment_review_finish())
    exit

# A separate, short matte check; it does not repeat the fifteen-state review.
testcase barkley_edge_review:
    assert screen "main_menu"
    $ persistent.chapter_spoiler_warnings = False
    $ _test.force = True
    $ _test.screenshot_directory = config.basedir + "/test-results/barkley-edge"
    $ __import__("os").makedirs(_test.screenshot_directory, exist_ok=True)
    click "Chapters"
    click "24 · Which way we go"
    advance until eval (_history_list[-1].what.startswith("Barkley sat down and whined softly,"))
    assert eval (renpy.showing("barkley") and renpy.showing("bg treehouse_later"))
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "dispute-support"
    keysym "h"
    click "People"
    click "Barkley"
    assert eval ("golden retriever" in _test_screen_text("people") and renpy.get_widget("people", "familiar_portrait") is not None)
    pause .25
    screenshot "people-barkley"
    exit

# Pond review stays separate from unrelated room/matte suites. These captures
# establish the actual source, scene, support view and montage usage to inspect.
init python:
    def _pond_review_inputs():
        import hashlib
        from pathlib import Path
        inputs = _environment_review_inputs()
        cue = Path(config.basedir) / "game/closing_theme.json"
        inputs["game/closing_theme.json"] = hashlib.sha256(cue.read_bytes()).hexdigest()
        return inputs

    def _pond_review_begin():
        import os
        renpy.store._pond_review_input_hashes = _pond_review_inputs()
        renpy.store._pond_review_frames = []
        os.makedirs(config.basedir + "/test-results/pond-states", exist_ok=True)

    def _pond_review_note(name):
        theme = renpy.get_screen("closing_theme") is not None
        entry = {
            "screenshot": name + ".png",
            "scene_key": scene_key,
            "scene_number": scene_number,
            "screen": "closing_theme" if theme else "story",
            "dialogue": None if theme else _history_list[-1].what,
            "windows_hidden": bool(_windows_hidden),
            "shown": [" ".join((tag,) + tuple(renpy.get_attributes(tag) or ()))
                      for tag in sorted(renpy.get_showing_tags())],
        }
        if theme:
            import bisect
            player = renpy.get_widget("closing_theme", "montage")
            position = player.position()
            index = bisect.bisect_right(THEME_STARTS, position) - 1
            entry["theme"] = {
                "position_seconds": position,
                "shot_index": index,
                "image": "game/" + CLOSING_THEME["shots"][index]["image"],
                "label": CLOSING_THEME["shots"][index]["label"],
                "paused": renpy.music.get_pause(channel="closing_theme"),
                "reduced_motion": player.reduced_motion,
                "note": "Actual ClosingTheme displayable paused on its fully settled shared cue; not an MP4 frame or direct image preview.",
            }
        renpy.store._pond_review_frames.append(entry)

    def _pond_review_seek_theme():
        assert renpy.music.get_pause(channel="closing_theme")
        expected = "images/cg/book-one/garden-compromise.png"
        matches = [i for i, shot in enumerate(CLOSING_THEME["shots"]) if shot["image"] == expected]
        assert len(matches) == 1, "The reviewed garden CG must have exactly one montage cue"
        index = matches[0]
        start = CLOSING_THEME["shots"][index]["at"] + CLOSING_THEME["dissolve"]
        end = THEME_STARTS[index + 1]
        renpy.get_widget("closing_theme", "montage").last_position = (start + end) / 2.0
        return True

    def _pond_review_finish():
        import hashlib
        import json
        from datetime import datetime, timezone
        from pathlib import Path
        assert _pond_review_inputs() == _pond_review_input_hashes, "Source changed during pond captures"
        assert len(_pond_review_frames) == 12, "Missing requested pond view"
        assert config.version == "0.1-alpha", "Release identity must remain locked"
        root = Path(config.basedir)
        for entry in _pond_review_frames:
            path = root / "test-results/pond-states" / entry["screenshot"]
            assert path.is_file(), "Missing screenshot: " + str(path)
            entry["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        (root / "test-results/pond-states/capture-state.json").write_text(json.dumps({
            "captured_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "version": config.version,
            "method": "Native chapter navigation and dialogue advancement; H hides story UI for support views. The actual ClosingTheme screen is paused at the shared garden CG cue.",
            "scope": "Planting background/CG; pond establishing/rescue/comfort; completed waterwheel/familiars; garden CG in the actual runtime theme. Capture coverage is not artistic approval or audio review.",
            "inputs": _pond_review_input_hashes,
            "captures": _pond_review_frames,
        }, indent=2) + "\n")
        return True

testcase pond_state_review:
    assert screen "main_menu"
    assert eval (config.version == "0.1-alpha")
    $ persistent.chapter_spoiler_warnings = False
    $ persistent.large_text = False
    $ persistent.high_contrast = False
    $ persistent.reduced_motion = True
    $ _test.force = True
    $ _test.screenshot_directory = config.basedir + "/test-results/pond-states"
    $ _pond_review_begin()

    click "Chapters"
    click "03 · Room for both"
    assert eval (scene_key == "plant_disagreement" and renpy.showing("bg garden_work_area") and _history_list[-1].what.startswith("Maia let us help arrange")) timeout 4.0
    pause .25
    screenshot "03-planting-background-dialogue"
    $ _pond_review_note("03-planting-background-dialogue")
    advance until eval (_history_list[-1].what == "Here. There's loads of light.")
    assert eval (renpy.showing("calista home") and renpy.showing("kael young"))
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "03-planting-actors-support"
    $ _pond_review_note("03-planting-actors-support")
    keysym "h"
    advance until eval (renpy.showing("cg garden_compromise"))
    assert eval (not any(renpy.showing(tag) for tag in ("calista", "kael", "maia")) and renpy.get_screen("say"))
    pause .25
    screenshot "03-planting-compromise-dialogue"
    $ _pond_review_note("03-planting-compromise-dialogue")
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "03-planting-compromise-support"
    $ _pond_review_note("03-planting-compromise-support")
    keysym "h"

    click "Chapters"
    click "10 · The shallow water"
    assert eval (scene_key == "pond_scare" and renpy.showing("bg garden_pond") and not renpy.showing("cg")) timeout 4.0
    pause .25
    screenshot "10-pond-establishing-dialogue"
    $ _pond_review_note("10-pond-establishing-dialogue")
    advance until eval (_history_list[-1].what == "I can't swim!")
    assert eval (renpy.showing("cg pond_rescue") and dialogue_portrait("Lyra") is None)
    pause .25
    screenshot "10-pond-rescue-dialogue"
    $ _pond_review_note("10-pond-rescue-dialogue")
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "10-pond-rescue-support"
    $ _pond_review_note("10-pond-rescue-support")
    keysym "h"
    advance until eval (_history_list[-1].what == "You're out. You're out now.")
    assert eval (renpy.showing("cg pond_comfort") and not any(renpy.showing(tag) for tag in ("calista", "kael", "lyra")))
    pause .25
    screenshot "10-pond-comfort-dialogue"
    $ _pond_review_note("10-pond-comfort-dialogue")
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "10-pond-comfort-support"
    $ _pond_review_note("10-pond-comfort-support")
    keysym "h"

    click "Chapters"
    click "20 · Something that turns"
    advance until eval (renpy.showing("bg waterwheel"))
    assert eval (scene_key == "waterwheel" and _history_list[-1].what.startswith("When we carried it to the pond,"))
    pause .25
    screenshot "20-waterwheel-background-dialogue"
    $ _pond_review_note("20-waterwheel-background-dialogue")
    advance until eval (renpy.showing("nibble") and renpy.showing("bg waterwheel"))
    assert eval (all(renpy.showing(tag) for tag in ("shadow", "barkley", "nibble")))
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "20-waterwheel-familiar-support"
    $ _pond_review_note("20-waterwheel-familiar-support")
    keysym "h"

    click "Chapters"
    click "32 · What remains"
    advance until screen "book_afterword"
    $ persistent.reduced_motion = False
    click "Play closing theme"
    assert screen "closing_theme"
    pause .5
    click "Pause"
    assert eval (_pond_review_seek_theme())
    pause .3
    assert eval (not renpy.get_widget("closing_theme", "montage").reduced_motion and renpy.music.get_pause(channel="closing_theme"))
    screenshot "theme-garden-compromise-native"
    $ _pond_review_note("theme-garden-compromise-native")
    click "Skip closing theme"
    assert screen "chapter_end"
    assert eval (_pond_review_finish())
    exit
