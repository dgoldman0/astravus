# Development-only tests. This file is excluded from exported builds.
init python:
    def _test_screen_text(name):
        pieces = []
        screen = renpy.get_screen(name)
        if screen:
            screen.visit_all(lambda item: pieces.append(item.get_all_text()) if isinstance(item, renpy.text.text.Text) else None)
        return "\n".join(pieces)

testsuite global:
    setup:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 60.0
        $ _test.screenshot_directory = renpy.config.basedir + "/test-results/screenshots"
        $ preferences.text_cps = 0
        $ persistent.large_text = False
        $ persistent.high_contrast = False
        $ persistent.reduced_motion = True
        $ persistent.book_one_complete = False
    teardown:
        exit

# Keep this identifier: scripts/project.py invokes it explicitly.
testcase chapter_playthrough:
    assert screen "main_menu"
    assert eval (config.version == "0.2.0" and config.save_directory == "Astravus-Book-I")
    screenshot "title"
    click "Begin Book I"
    assert screen "chapter_card" timeout 4.0
    click "Enter the memory"
    assert eval (renpy.showing("cg first_memory") and not renpy.showing("calista")) timeout 4.0
    assert eval (visited_scenes == ["first_memory"] and not lumen_known and not joren_lost)
    screenshot "first-memory"
    click "People"
    assert screen "people"
    assert eval ("living Astravus" not in _test_screen_text("people") and "Joren" not in _test_screen_text("people"))
    screenshot "people-before-reveal"
    click "Return"
    advance until eval (renpy.showing("bg family_home"))
    assert eval (not renpy.showing("cg"))
    advance until eval (_history_list[-1].what.startswith("The home I grew"))
    screenshot "family-home"
    advance until eval (_history_list[-1].what == "Here, Cali.")
    assert eval (scene_key == "garden" and renpy.showing("bg garden_close") and renpy.showing("calista young"))
    screenshot "garden"
    run FileSave(1, confirm=False, page="1")
    assert eval (renpy.slot_json("1-1").get("book_id") == BOOK_SAVE_ID)
    advance
    advance
    run FileLoad(1, confirm=False, page="1")
    assert eval (_history_list[-1].what == "Here, Cali." and scene_key == "garden") timeout 4.0
    click "History"
    assert screen "history"
    screenshot "history"
    click "Return"
    click "Settings"
    assert screen "preferences"
    click "Larger dialogue text"
    click "Solid dialogue background"
    click "Reduced motion"
    assert eval (persistent.large_text and persistent.high_contrast and not persistent.reduced_motion)
    screenshot "settings"
    click "Reduced motion"
    click "Return"
    screenshot "large-text"
    click "Settings"
    click "Solid dialogue background"
    click "Larger dialogue text"
    click "Return"
    advance until eval (scene_key == "plant_disagreement" and renpy.showing("calista home"))
    assert eval (renpy.showing("kael young") and childhood_stage == "early")
    screenshot "siblings-garden"
    advance until eval (scene_key == "workshop_first" and renpy.showing("arin everyday"))
    assert eval (renpy.showing("bg workshop") and renpy.showing("calista home"))
    screenshot "workshop"
    advance until eval (renpy.music.get_playing(channel="sound") == "audio/flute_first.wav")
    assert eval (scene_key == "music_first" and renpy.showing("bg music_room") and not renpy.showing("calista"))
    screenshot "first-melody"
    advance until eval (scene_key == "dorian_stories" and renpy.showing("dorian everyday"))
    assert eval (renpy.showing("bg library"))
    screenshot "library"
    advance until eval (scene_key == "sage_story")
    assert eval (renpy.showing("bg sage_room") and not lumen_known)
    screenshot "sage-story"
    advance until eval (renpy.music.get_playing(channel="sound") == "audio/flute_practice.wav")
    assert eval (scene_key == "family_rhythm" and renpy.showing("bg music_room"))
    advance until eval (scene_key == "tree_echoes")
    assert eval (not lumen_known and renpy.showing("bg echoes"))
    advance until eval (lumen_known)
    click "People"
    assert eval ("living Astravus" in _test_screen_text("people"))
    screenshot "people-after-reveal"
    click "Return"
    screenshot "tree-of-echoes"
    advance until eval (scene_key == "pond_scare")
    assert eval (not renpy.showing("calista") and not renpy.showing("lyra"))
    screenshot "pond"
    advance until eval (scene_key == "soup_experiment")
    assert eval (renpy.showing("bg family_home"))
    advance until eval (renpy.showing("calista festival"))
    assert eval (scene_key == "festival_lights" and renpy.showing("bg festival"))
    screenshot "festival"
    advance until eval (met_cassia)
    assert eval (scene_key == "meeting_cassia" and renpy.showing("bg community_courtyard") and renpy.showing("cassia young"))
    advance until eval (met_joren)
    assert eval (scene_key == "meeting_joren" and renpy.showing("bg construction_path") and renpy.showing("joren young"))
    click "People"
    assert eval ("Joren" in _test_screen_text("people") and "His death" not in _test_screen_text("people"))
    screenshot "people-friends"
    click "Return"
    advance until eval (scene_key == "treehouse" and renpy.showing("cassia"))
    assert eval (renpy.showing("bg treehouse") and childhood_stage == "early" and renpy.showing("cassia young") and renpy.showing("joren young"))
    screenshot "treehouse"
    advance until eval (scene_key == "rain_refuge" and renpy.showing("bg treehouse_rain"))
    assert eval (renpy.music.get_playing(channel="ambience") == "audio/rain.ogg") timeout 4.0
    assert eval (not renpy.showing("cassia") and not renpy.showing("joren"))
    screenshot "treehouse-rain"
    run Rollback(force=True)
    assert eval (renpy.showing("bg treehouse") and scene_key == "treehouse") timeout 4.0
    assert eval (renpy.music.get_playing(channel="ambience") == "audio/garden_air.ogg") timeout 4.0
    advance until eval (scene_key == "rain_refuge" and renpy.showing("bg treehouse_rain"))
    assert eval (renpy.music.get_playing(channel="ambience") == "audio/rain.ogg") timeout 4.0
    advance until eval (scene_key == "waterwheel" and renpy.showing("calista older"))
    assert eval (childhood_stage == "later" and renpy.showing("joren older"))
    screenshot "older-children"
    advance until eval (scene_key == "waterwheel" and renpy.showing("cassia older"))
    assert eval (not joren_lost and childhood_stage == "later")
    screenshot "cassia-older"
    advance until eval (renpy.showing("bg waterwheel"))
    assert eval (scene_key == "waterwheel")
    screenshot "waterwheel"
    advance until eval (scene_key == "outer_exploration" and renpy.showing("bg construction_room"))
    assert eval (not joren_lost)
    screenshot "construction-room"
    advance until eval (scene_key == "dome_ascent" and renpy.showing("bg dome"))
    assert eval (not joren_lost)
    screenshot "dome"
    advance until eval (scene_key == "treehouse_dispute" and renpy.showing("calista frustrated"))
    assert eval (renpy.showing("joren frustrated"))
    screenshot "disagreement"
    advance until eval (joren_lost)
    assert eval (scene_key == "loss" and not renpy.showing("joren"))
    screenshot "the-news"
    advance until eval (scene_key == "family_grief" and renpy.showing("calista mourning"))
    assert eval (not renpy.showing("joren") and renpy.music.get_playing() == "audio/grief_theme.ogg") timeout 4.0
    screenshot "family-grief"
    click "People"
    assert eval ("His death" in _test_screen_text("people"))
    screenshot "people-remembrance"
    click "Return"
    advance until eval (scene_key == "painting_grief" and renpy.showing("calista painting"))
    assert eval (not renpy.showing("joren"))
    screenshot "painting"
    advance until eval (scene_key == "cassia_grief" and renpy.showing("cassia mourning"))
    assert eval (not renpy.showing("joren"))
    screenshot "cassia-grief"
    advance until eval (scene_key == "community_memorial")
    assert eval (not renpy.showing("joren"))
    screenshot "memorial"
    advance until eval (scene_key == "mural_remembrance")
    assert eval (not renpy.showing("joren"))
    screenshot "mural"
    advance until eval (scene_key == "treehouse_remembrance")
    assert eval (renpy.showing("bg treehouse_memory") and not renpy.showing("joren"))
    screenshot "remembering-in-rain"
    advance until screen "chapter_end"
    assert eval (persistent.book_one_complete and visited_scenes == list(BOOK_SCENE_KEYS))
    assert eval (scene_number == BOOK_SCENE_COUNT == 32 and scene_key == "annual_remembrance")
    assert eval (lumen_known and joren_lost and childhood_stage == "later")
    screenshot "end"
    click "Credits"
    assert screen "about"
    screenshot "credits"
    click "Return"
    assert screen "chapter_end"
    click "Return to title"
    assert screen "main_menu" timeout 4.0
    click "Continue"
    assert screen "chapter_end" timeout 10.0
    assert eval (scene_key == "annual_remembrance" and len(visited_scenes) == 32)
    screenshot "resumed"
    click "Return to title"
    assert screen "main_menu" timeout 4.0
    click "How to read"
    assert screen "help"
    click "Return"
    click "Begin Book I"
    click "Enter the memory"
    assert eval (visited_scenes == ["first_memory"] and not lumen_known and not joren_lost and childhood_stage == "early") timeout 4.0
    click "People"
    assert eval ("living Astravus" not in _test_screen_text("people") and "Joren" not in _test_screen_text("people"))
    exit
