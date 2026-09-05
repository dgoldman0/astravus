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
