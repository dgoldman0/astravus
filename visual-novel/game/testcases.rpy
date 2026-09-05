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
    assert eval (config.version == "0.2.4" and config.save_directory == "Astravus-Book-I")
    screenshot "title"
    click "Begin Book I"
    assert screen "chapter_card" timeout 4.0
    click "Enter the memory"
    assert eval (renpy.showing("cg first_memory") and not renpy.showing("calista")) timeout 4.0
    assert eval (visited_scenes == ["first_memory"] and not lumen_known and not joren_lost)
    screenshot "first-memory"
    click "People"
    assert screen "people"
    assert eval (people_names() == ["Cali"] and familiar_names() == [])
    click "Lumen"
    assert eval ("living Astravus" not in _test_screen_text("people") and "Joren" not in _test_screen_text("people"))
    screenshot "people-before-reveal"
    click "Return"
    advance until eval (renpy.showing("bg family_home"))
    assert eval (not renpy.showing("cg"))
    advance until eval (_history_list[-1].what.startswith("The home I grew"))
    screenshot "family-home"
    assert eval (familiar_names() == [] and not renpy.showing("shadow"))
    run FileSave(8, confirm=False, page="1")
    advance until eval (_history_list[-1].what == FAMILIAR_INTRODUCTION)
    assert eval (familiar_names() == ["Shadow", "Barkley", "Nibble"])
    assert eval (all(renpy.showing(tag) for tag in ("shadow", "barkley", "nibble")))
    screenshot "familiars-home"
    click "People"
    assert eval (renpy.get_widget("people", "familiar_portrait") is not None and "green eyes" in _test_screen_text("people"))
    screenshot "people-shadow"
    click "Barkley"
    assert eval ("golden retriever" in _test_screen_text("people") and renpy.get_widget("people", "familiar_portrait") is not None)
    screenshot "people-barkley"
    click "Nibble"
    assert eval ("little rat" in _test_screen_text("people") and renpy.get_widget("people", "familiar_portrait") is not None)
    screenshot "people-nibble"
    click "Return"
    run FileSave(9, confirm=False, page="1")
    run Rollback(force=True)
    assert eval (familiar_names() == [] and not renpy.showing("shadow")) timeout 4.0
    run FileLoad(9, confirm=False, page="1")
    assert eval (len(familiar_names()) == 3 and renpy.showing("nibble")) timeout 4.0
    run FileLoad(8, confirm=False, page="1")
    assert eval (familiar_names() == [] and not renpy.showing("barkley")) timeout 4.0
    run FileLoad(9, confirm=False, page="1")
    assert eval (len(familiar_names()) == 3) timeout 4.0
    advance until eval (_history_list[-1].what == "Here, Cali.")
    assert eval (scene_key == "garden" and renpy.showing("bg garden_close") and renpy.showing("calista young"))
    assert eval (len(familiar_names()) == 3 and not any(renpy.showing(tag) for tag in ("shadow", "barkley", "nibble")))
    screenshot "garden"
    click "People"
    assert eval (people_names() == ["Cali", "Maia"] and "patient, practical care" in _test_screen_text("people"))
    screenshot "people-maia"
    click "Return"
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
    advance until eval (renpy.music.get_playing(channel="sound") == "audio/flute_attempt.wav")
    assert eval (scene_key == "music_first" and renpy.showing("bg music_room") and not renpy.showing("calista"))
    screenshot "first-melody"
    advance until eval (_history_list[-1].what == "That wasn't it.")
    assert eval (dialogue_portrait("Cali") == "calista home" and renpy.get_widget("say", "speaker_portrait") is not None)
    assert eval (renpy.music.get_playing(channel="sound") != "audio/flute_first.wav")
    screenshot "flute-dialogue-portrait"
    run FileSave(2, confirm=False, page="1")
    advance
    run FileLoad(2, confirm=False, page="1")
    assert eval (_history_list[-1].what == "That wasn't it." and renpy.get_widget("say", "speaker_portrait") is not None) timeout 4.0
    click "People"
    assert eval (people_names() == ["Cali", "Maia", "Kael", "Arin", "Selene"])
    screenshot "people-selene"
    click "Return"
    advance until eval (renpy.music.get_playing(channel="sound") == "audio/flute_first.wav")
    assert eval (_history_list[-1].what.startswith("We went a few notes at a time."))
    screenshot "first-flute-phrase"
    advance until eval (scene_key == "dorian_stories" and renpy.showing("dorian everyday"))
    assert eval (renpy.showing("bg library"))
    screenshot "library"
    advance until eval (scene_key == "sage_story")
    assert eval (renpy.showing("bg sage_room") and not lumen_known)
    screenshot "sage-story"
    advance until eval (_history_list[-1].what == "I'll choose this time. There are three siblings in it.")
    assert eval (not renpy.showing("sage") and renpy.get_widget("say", "speaker_portrait") is not None)
    screenshot "sage-speaking"
    advance until eval (renpy.music.get_playing(channel="sound") == "audio/flute_practice.wav")
    assert eval (scene_key == "family_rhythm" and renpy.showing("bg music_room"))
    advance until eval (scene_key == "tree_echoes")
    assert eval (not lumen_known and renpy.showing("bg echoes"))
    advance until eval (lumen_known)
    click "People"
    assert eval (len(people_names()) == 8 and "Sage" in people_names() and "Lyra" in people_names())
    click "Lumen"
    assert eval ("living Astravus" in _test_screen_text("people"))
    screenshot "people-after-reveal"
    click "Return"
    screenshot "tree-of-echoes"
    advance until eval (scene_key == "pond_scare")
    assert eval (not renpy.showing("calista") and not renpy.showing("lyra"))
    screenshot "pond"
    advance until eval (_history_list[-1].what == "I can't swim!")
    assert eval (dialogue_portrait("Lyra") == "lyra young" and renpy.get_widget("say", "speaker_portrait") is not None)
    screenshot "pond-speaking"
    advance until eval (scene_key == "soup_experiment")
    assert eval (renpy.showing("bg family_home"))
    advance until eval (_history_list[-1].what == "Did someone add something?")
    assert eval (renpy.get_widget("say", "speaker_portrait") is not None)
    screenshot "soup-speaking"
    advance until eval (renpy.showing("calista festival"))
    assert eval (scene_key == "festival_lights" and renpy.showing("bg festival"))
    screenshot "festival"
    advance until eval (_history_list[-1].who == "Cassia")
    click "People"
    assert eval (not met_cassia and "Cassia" in people_names() and "Thalia" not in people_names())
    screenshot "people-first-cassia-line"
    click "Return"
    run FileSave(3, confirm=False, page="1")
    run Rollback(force=True)
    assert eval ("Cassia" not in people_names()) timeout 4.0
    run FileLoad(1, confirm=False, page="1")
    assert eval (people_names() == ["Cali", "Maia"]) timeout 4.0
    run FileLoad(3, confirm=False, page="1")
    assert eval ("Cassia" in people_names() and not met_cassia) timeout 4.0
    advance until eval (met_cassia)
    assert eval (scene_key == "meeting_cassia" and renpy.showing("bg community_courtyard") and renpy.showing("cassia young"))
    advance until eval (_history_list[-1].who == "Thalia")
    assert eval ("Thalia" in people_names() and "Lyron" not in people_names())
    advance until eval (_history_list[-1].who == "Lyron")
    click "People"
    assert eval ("Lyron" in people_names() and "agricultural systems" in _test_screen_text("people"))
    screenshot "people-lyron"
    click "Return"
    advance until eval (met_joren)
    assert eval (scene_key == "meeting_joren" and renpy.showing("bg construction_path") and renpy.showing("joren young"))
    click "People"
    click "Joren"
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
    advance until eval (_history_list[-1].what == "Imagine a world where the trees could talk.")
    assert eval (dialogue_portrait("Cassia") == "cassia young" and renpy.get_widget("say", "speaker_portrait") is not None)
    screenshot "rain-speaking"
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
    assert eval (not joren_lost and all(renpy.showing(tag) for tag in ("shadow", "barkley", "nibble")))
    screenshot "construction-room"
    advance until eval (scene_key == "dome_ascent" and renpy.showing("bg dome"))
    assert eval (not joren_lost)
    screenshot "dome"
    advance until eval (_history_list[-1].what == "It's like we're on top of the world.")
    assert eval (dialogue_portrait("Cassia") == "cassia older" and renpy.get_widget("say", "speaker_portrait") is not None)
    screenshot "dome-speaking"
    advance until eval (scene_key == "treehouse_dispute" and renpy.showing("calista frustrated"))
    assert eval (renpy.showing("joren frustrated"))
    screenshot "disagreement"
    advance until eval (scene_key == "treehouse_dispute" and renpy.showing("nibble"))
    assert eval (all(renpy.showing(tag) for tag in ("shadow", "barkley", "nibble")))
    screenshot "familiars-disagreement"
    advance until eval (joren_lost)
    assert eval (scene_key == "loss" and not renpy.showing("joren"))
    assert eval (not any(renpy.showing(tag) for tag in ("shadow", "barkley", "nibble")))
    assert eval (dialogue_portrait("Joren") is None and dialogue_portrait("Calista · remembering") is None)
    screenshot "the-news"
    advance until eval (scene_key == "family_grief" and renpy.showing("calista mourning"))
    assert eval (not renpy.showing("joren") and renpy.music.get_playing() == "audio/grief_theme.ogg") timeout 4.0
    screenshot "family-grief"
    click "People"
    click "Joren"
    assert eval ("His death" in _test_screen_text("people"))
    screenshot "people-remembrance"
    click "Return"
    advance until eval (scene_key == "painting_grief" and renpy.showing("calista painting"))
    assert eval (not renpy.showing("joren"))
    screenshot "painting"
    advance until eval (_history_list[-1].what == "That's his side of the map. He wanted the path to go there.")
    assert eval (all(renpy.showing(tag) for tag in ("shadow", "barkley", "nibble")) and not renpy.showing("calista"))
    assert eval (renpy.get_widget("say", "speaker_portrait") is not None)
    screenshot "familiars-painting"
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
    assert eval (people_names() == ["Cali"] and familiar_names() == [])
    click "Lumen"
    assert eval ("living Astravus" not in _test_screen_text("people") and "Joren" not in _test_screen_text("people"))
    click "Return"
    click "Chapters"
    assert screen "dev_chapters"
    screenshot "dev-chapters"
    click "Return"
    assert eval (scene_key == "first_memory" and visited_scenes == ["first_memory"])
    click "Chapters"
    click "26 · What comfort can do"
    assert eval (scene_key == "family_grief" and joren_lost and lumen_known and childhood_stage == "later") timeout 4.0
    assert eval (renpy.showing("bg home_dusk") and len(people_names()) == 14 and len(familiar_names()) == 3)
    assert eval (renpy.music.get_playing() == "audio/grief_theme.ogg") timeout 4.0
    advance until eval (_history_list[-1].what == "But it hurts so much, Maia.")
    screenshot "grief-maia-response"
    advance until eval (_history_list[-1].what == "We have each other to lean on. We'll get through this together.")
    assert eval (dialogue_portrait("Maia") == "maia home" and renpy.get_widget("say", "speaker_portrait") is not None)
    screenshot "grief-embrace"
    click "Chapters"
    click "05 · A color you can hear"
    assert eval (scene_key == "music_first" and not joren_lost and not lumen_known and childhood_stage == "early") timeout 4.0
    assert eval (people_names() == ["Cali", "Maia", "Kael", "Arin"] and len(_history_list) == 1)
    assert eval (renpy.showing("bg music_room") and renpy.music.get_playing() is None) timeout 4.0
    assert eval (not renpy.can_rollback() and scene_key == "music_first" and not joren_lost and "Joren" not in people_names())
    run FileSave(10, confirm=False, page="1")
    click "Chapters"
    click "17 · Beyond the familiar paths"
    assert eval (scene_key == "kaleb_walk" and met_joren and met_cassia and not joren_lost) timeout 4.0
    assert eval (renpy.music.get_playing() == "audio/discovery_theme.ogg") timeout 4.0
    advance until eval (scene_key == "treehouse")
    assert eval (visited_scenes == list(BOOK_SCENE_KEYS[:18]))
    run FileLoad(10, confirm=False, page="1")
    assert eval (scene_key == "music_first" and not joren_lost and not met_joren) timeout 4.0
    advance until eval (scene_key == "dorian_stories")
    assert eval (visited_scenes == list(BOOK_SCENE_KEYS[:6]))
    click "Chapters"
    click "32 · What remains"
    assert eval (scene_key == "annual_remembrance" and joren_lost and len(people_names()) == 14) timeout 4.0
    assert eval (renpy.music.get_playing() == "audio/remembrance_theme.ogg") timeout 4.0
    advance until screen "chapter_end"
    click "Return to title"
    click "Chapters"
    click "01 · First memory"
    assert screen "chapter_card" timeout 4.0
    click "Enter the memory"
    assert eval (visited_scenes == ["first_memory"] and not joren_lost and not lumen_known and people_names() == ["Cali"] and familiar_names() == []) timeout 4.0
    exit
