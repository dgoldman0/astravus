# Development-only audio state checks; excluded from exported builds.
# This suite verifies Ren'Py playback/state transitions with the test backend.
# It is not a listening assessment of timbre, composition or subjective balance.
init python:
    def _score_review_begin():
        import hashlib
        from pathlib import Path
        project = Path(config.basedir)
        paths = [*project.glob("game/*.rpy"), *project.glob("game/audio/*.ogg"),
                 *project.glob("game/audio/*.wav"), project / "scripts/score_catalog.py"]
        # Test evidence lives outside the game store so save/load and rollback
        # cannot erase the observations of those same operations.
        renpy._astravus_score_review = {
            "records": [],
            "inputs": {str(path.relative_to(project)): hashlib.sha256(path.read_bytes()).hexdigest()
                       for path in sorted(paths)},
        }

    def _score_review_note(beat):
        renpy._astravus_score_review["records"].append({
            "beat": beat, "scene": scene_key,
            "music": renpy.music.get_playing(channel="music"),
            "ambience": renpy.music.get_playing(channel="ambience"),
            "sound": renpy.music.get_playing(channel="sound"),
            "line": _history_list[-1].what if _history_list else None,
        })

    def _score_review_finish():
        import json
        from pathlib import Path
        destination = Path(config.basedir) / "test-results/score-runtime.json"
        destination.write_text(json.dumps({
            "method": "Native Ren'Py playback state at all 32 direct chapter entries and protected reader-reached beats, including rollback and save/load. Headless test audio backend; no subjective listening claim.",
            "inputs": renpy._astravus_score_review["inputs"],
            "records": renpy._astravus_score_review["records"],
        }, indent=2) + "\n")

testcase score_review:
    assert screen "main_menu"
    $ persistent.chapter_spoiler_warnings = False
    $ _score_review_begin()

    # Each actual chapter entry selects its own cue, independent of the one
    # playing before the jump. The title card is unique to the first chapter.
    click "Chapters"
    click "01 · First memory"
    assert screen "chapter_card" timeout 5.0
    click "Enter the memory"
    assert eval (scene_key == "first_memory" and renpy.music.get_playing() == "audio/first_light.ogg") timeout 5.0
    $ _score_review_note("01-entry")
    click "Chapters"
    click "02 · A small beginning"
    assert eval (scene_key == "garden" and renpy.music.get_playing() == "audio/garden_growth.ogg") timeout 5.0
    $ _score_review_note("02-entry")
    click "Chapters"
    click "03 · Room for both"
    assert eval (scene_key == "plant_disagreement" and renpy.music.get_playing() == "audio/garden_growth.ogg") timeout 5.0
    $ _score_review_note("03-entry")
    click "Chapters"
    click "04 · The scattered pieces"
    assert eval (scene_key == "workshop_first" and renpy.music.get_playing() == "audio/workshop_play.ogg") timeout 5.0
    $ _score_review_note("04-entry")
    click "Chapters"
    click "05 · A color you can hear"
    assert eval (scene_key == "music_first" and renpy.music.get_playing() is None) timeout 5.0
    $ _score_review_note("05-entry")
    click "Chapters"
    click "06 · Routes through a story"
    assert eval (scene_key == "dorian_stories" and renpy.music.get_playing() == "audio/home_evening.ogg") timeout 5.0
    $ _score_review_note("06-entry")
    click "Chapters"
    click "07 · Three ways forward"
    assert eval (scene_key == "sage_story" and renpy.music.get_playing() == "audio/home_tender.ogg") timeout 5.0
    $ _score_review_note("07-entry")
    click "Chapters"
    click "08 · The days between"
    assert eval (scene_key == "family_rhythm" and renpy.music.get_playing() == "audio/home_theme.ogg") timeout 5.0
    $ _score_review_note("08-entry")
    click "Chapters"
    click "09 · The Tree of Echoes"
    assert eval (scene_key == "tree_echoes" and renpy.music.get_playing() == "audio/wonder_theme.ogg") timeout 5.0
    $ _score_review_note("09-entry")
    click "Chapters"
    click "10 · The shallow water"
    assert eval (scene_key == "pond_scare" and renpy.music.get_playing() is None) timeout 5.0
    $ _score_review_note("10-entry")
    click "Chapters"
    click "11 · A little too much"
    assert eval (scene_key == "soup_experiment" and renpy.music.get_playing() == "audio/home_theme.ogg") timeout 5.0
    $ _score_review_note("11-entry")
    click "Chapters"
    click "12 · Wishes in the light"
    assert eval (scene_key == "festival_lights" and renpy.music.get_playing() == "audio/festival_theme.ogg") timeout 5.0
    $ _score_review_note("12-entry")
    click "Chapters"
    click "13 · An invitation"
    assert eval (scene_key == "meeting_cassia" and renpy.music.get_playing() == "audio/friendship_theme.ogg") timeout 5.0
    $ _score_review_note("13-entry")
    click "Chapters"
    click "14 · Room for another story"
    assert eval (scene_key == "cassia_home" and renpy.music.get_playing() == "audio/friendship_theme.ogg") timeout 5.0
    $ _score_review_note("14-entry")
    click "Chapters"
    click "15 · Something worth finding"
    assert eval (scene_key == "meeting_joren" and renpy.music.get_playing() == "audio/discovery_theme.ogg") timeout 5.0
    $ _score_review_note("15-entry")
    click "Chapters"
    click "16 · Things we could make"
    assert eval (scene_key == "joren_home" and renpy.music.get_playing() == "audio/workshop_play.ogg") timeout 5.0
    $ _score_review_note("16-entry")
    click "Chapters"
    click "17 · Beyond the familiar paths"
    assert eval (scene_key == "kaleb_walk" and renpy.music.get_playing() == "audio/outward_paths.ogg") timeout 5.0
    $ _score_review_note("17-entry")
    click "Chapters"
    click "18 · Our place in the branches"
    assert eval (scene_key == "treehouse" and renpy.music.get_playing() == "audio/friendship_theme.ogg") timeout 5.0
    $ _score_review_note("18-entry")
    click "Chapters"
    click "19 · A story under the rain"
    assert eval (scene_key == "rain_refuge" and renpy.music.get_playing() == "audio/rain_refuge.ogg") timeout 5.0
    $ _score_review_note("19-entry")
    click "Chapters"
    click "20 · Something that turns"
    assert eval (scene_key == "waterwheel" and renpy.music.get_playing() == "audio/workshop_play.ogg") timeout 5.0
    $ _score_review_note("20-entry")
    click "Chapters"
    click "21 · The unfinished world"
    assert eval (scene_key == "outer_exploration" and renpy.music.get_playing() == "audio/outward_paths.ogg") timeout 5.0
    $ _score_review_note("21-entry")
    click "Chapters"
    click "22 · A place beside us"
    assert eval (scene_key == "lyra_included" and renpy.music.get_playing() == "audio/home_tender.ogg") timeout 5.0
    $ _score_review_note("22-entry")
    click "Chapters"
    click "23 · The view from above"
    assert eval (scene_key == "dome_ascent" and renpy.music.get_playing() == "audio/discovery_careful.ogg") timeout 5.0
    $ _score_review_note("23-entry")
    click "Chapters"
    click "24 · Which way we go"
    assert eval (scene_key == "treehouse_dispute" and renpy.music.get_playing() == "audio/friendship_play.ogg") timeout 5.0
    $ _score_review_note("24-entry")
    click "Chapters"
    click "25 · The news"
    assert eval (scene_key == "loss" and renpy.music.get_playing() is None) timeout 5.0
    $ _score_review_note("25-entry")
    click "Chapters"
    click "26 · What comfort can do"
    assert eval (scene_key == "family_grief" and renpy.music.get_playing() == "audio/grief_theme.ogg") timeout 5.0
    $ _score_review_note("26-entry")
    click "Chapters"
    click "27 · What the hand remembers"
    assert eval (scene_key == "painting_grief" and renpy.music.get_playing() == "audio/painting_theme.ogg") timeout 5.0
    $ _score_review_note("27-entry")
    click "Chapters"
    click "28 · Between the two of us"
    assert eval (scene_key == "cassia_grief" and renpy.music.get_playing() == "audio/shared_grief.ogg") timeout 5.0
    $ _score_review_note("28-entry")
    click "Chapters"
    click "29 · The names we carry"
    assert eval (scene_key == "community_memorial" and renpy.music.get_playing() is None) timeout 5.0
    $ _score_review_note("29-entry")
    click "Chapters"
    click "30 · A place to remember"
    assert eval (scene_key == "mural_remembrance" and renpy.music.get_playing() == "audio/painting_theme.ogg") timeout 5.0
    $ _score_review_note("30-entry")
    click "Chapters"
    click "31 · The rain returns"
    assert eval (scene_key == "treehouse_remembrance" and renpy.music.get_playing() == "audio/remembrance_rain.ogg") timeout 5.0
    $ _score_review_note("31-entry")
    click "Chapters"
    click "32 · What remains"
    assert eval (scene_key == "annual_remembrance" and renpy.music.get_playing() == "audio/remembrance_theme.ogg") timeout 5.0
    $ _score_review_note("32-entry")

    # Music reaches the success only with the reader. Returning across that
    # point or loading the earlier save must restore the working arrangement.
    click "Chapters"
    click "20 · Something that turns"
    advance until eval (_history_list[-1].what.startswith("When we carried it to the pond,"))
    assert eval (renpy.music.get_playing() == "audio/workshop_play.ogg") timeout 5.0
    pause 1.0
    assert eval (renpy.music.get_playing() == "audio/workshop_play.ogg")
    run FileSave(19, confirm=False, page="1")
    $ _score_review_note("waterwheel-before-success")
    advance
    assert eval (_history_list[-1].what == "Look at it go!" and renpy.music.get_playing() == "audio/workshop_success.ogg") timeout 5.0
    $ _score_review_note("waterwheel-success")
    run Rollback(force=True)
    assert eval (_history_list[-1].what.startswith("When we carried it to the pond,") and renpy.music.get_playing() == "audio/workshop_play.ogg") timeout 5.0
    $ _score_review_note("waterwheel-rollback")
    click "Chapters"
    click "26 · What comfort can do"
    assert eval (renpy.music.get_playing() == "audio/grief_theme.ogg") timeout 5.0
    run FileLoad(19, confirm=False, page="1")
    assert eval (scene_key == "waterwheel" and renpy.music.get_playing() == "audio/workshop_play.ogg") timeout 5.0
    $ _score_review_note("waterwheel-load-restores-music")

    # The actual flute performances stay unobscured, even at test reading speed.
    click "Chapters"
    click "05 · A color you can hear"
    advance until eval (renpy.music.get_playing(channel="sound") == "audio/flute_attempt.wav")
    assert eval (renpy.music.get_playing() is None and _history_list[-1].what == "The first sound trembled, thinned, and broke.")
    $ _score_review_note("flute-single-broken-breath")
    advance until eval (_history_list[-1].what == "There was a note in there. I heard it.")
    assert eval (renpy.music.get_playing() is None and renpy.music.get_playing(channel="sound") != "audio/flute_first.wav")
    advance until eval (renpy.music.get_playing(channel="sound") == "audio/flute_first.wav")
    assert eval (renpy.music.get_playing() is None and _history_list[-1].what.startswith("We went a few notes at a time."))
    $ _score_review_note("flute-hesitant-phrase")
    click "Chapters"
    click "08 · The days between"
    advance until eval (renpy.music.get_playing(channel="sound") == "audio/flute_practice.wav")
    assert eval (renpy.music.get_playing() is None)
    $ _score_review_note("flute-practiced-phrase")

    click "Chapters"
    click "09 · The Tree of Echoes"
    advance until eval (renpy.music.get_playing(channel="sound") == "audio/tree_creak.wav")
    assert eval (renpy.music.get_playing() is None)
    $ _score_review_note("tree-listening")
    click "Chapters"
    click "10 · The shallow water"
    advance until eval (renpy.music.get_playing(channel="sound") == "audio/water_splash.wav")
    assert eval (renpy.music.get_playing() is None)
    $ _score_review_note("pond-rescue")
    advance until eval (_history_list[-1].what == "I know. You're here.")
    assert eval (renpy.music.get_playing() is None)
    advance
    assert eval (renpy.music.get_playing() == "audio/home_tender.ogg") timeout 5.0
    $ _score_review_note("pond-safe-comfort")

    # Preserve ordinary warmth to the end of chapter 24, silence through 25,
    # and no musical lead-in underneath the memorial address.
    click "Chapters"
    click "24 · Which way we go"
    advance until eval (_history_list[-1].what.startswith("Our days were filled with discovery"))
    assert eval (renpy.music.get_playing() == "audio/friendship_warm.ogg") timeout 5.0
    pause 1.0
    assert eval (renpy.music.get_playing() == "audio/friendship_warm.ogg")
    $ _score_review_note("24-final-warmth")
    advance until eval (joren_lost)
    assert eval (scene_key == "loss" and renpy.music.get_playing() is None and renpy.music.get_playing(channel="ambience") is None) timeout 3.0
    $ _score_review_note("25-news-silence")
    advance until eval (_history_list[-1].what.startswith("The places we had explored together now felt different,"))
    assert eval (renpy.music.get_playing() is None)
    $ _score_review_note("25-final-silence")
    click "Chapters"
    click "29 · The names we carry"
    advance until eval (_history_list[-1].what.startswith("Joren was a light in our lives."))
    assert eval (renpy.music.get_playing() is None)
    $ _score_review_note("memorial-speech-silence")
    advance until eval (_history_list[-1].what.startswith("He looked out across the people gathered there."))
    assert eval (renpy.music.get_playing() is None)
    advance
    assert eval (renpy.music.get_playing() == "audio/remembrance_theme.ogg") timeout 5.0
    $ _score_review_note("memorial-after-address")

    click "Chapters"
    click "32 · What remains"
    advance until screen "book_afterword"
    assert eval (renpy.music.get_playing() == "audio/home_theme.ogg") timeout 5.0
    $ _score_review_note("afterword-handoff")
    run MainMenu(confirm=False)
    assert screen "main_menu" timeout 5.0
    assert eval (renpy.music.get_playing() == "audio/first_light.ogg" and all(renpy.music.get_playing(channel=channel) is None for channel in ("ambience", "sound", "closing_theme"))) timeout 5.0
    $ _score_review_note("title-audio-cleanup")
    $ _score_review_finish()
    exit
