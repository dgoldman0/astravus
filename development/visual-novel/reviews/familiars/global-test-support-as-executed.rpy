# Development-only tests. This file is excluded from exported builds.
init python:
    def _test_screen_text(name):
        pieces = []
        screen = renpy.get_screen(name)
        if screen:
            screen.visit_all(lambda item: pieces.append(item.get_all_text()) if isinstance(item, renpy.text.text.Text) else None)
        return "\n".join(pieces)

    def _test_clear_chapter_reading():
        for identifiers in CHAPTER_DIALOGUE_IDS.values():
            for identifier in identifiers:
                renpy.mark_translation_unseen(identifier)

    def _test_chapter_dialogue_coverage():
        story_files = {"script.rpy", "family_book_one.rpy", "friendships_book_one.rpy"}
        expected = {
            node.identifier
            for filename, translations in renpy.game.script.translator.file_translates.items()
            if filename.replace("\\", "/").rsplit("/", 1)[-1] in story_files
            for label, node in translations
        }
        assigned = [identifier for identifiers in CHAPTER_DIALOGUE_IDS.values() for identifier in identifiers]
        return bool(expected) and all(CHAPTER_DIALOGUE_IDS.values()) and len(assigned) == len(set(assigned)) and set(assigned) == expected

    def _test_theme_buffered_clock():
        # Exercise the real player clock against an audio backend that updates
        # only every 80ms, then disappears, pauses, and returns behind the film.
        # Raw get_pos-driven animation would stall and leap on this sequence.
        original_pos, original_pause = renpy.music.get_pos, renpy.music.get_pause
        state = {"audio": 0.0, "paused": False}
        try:
            renpy.music.get_pos = lambda channel: state["audio"]
            renpy.music.get_pause = lambda channel: state["paused"]
            player = ClosingTheme()
            positions = []
            for frame in range(601):
                st = frame / 60.0
                state["audio"] = int(st / .08) * .08
                positions.append(player.position(st))
            steps = [b - a for a, b in zip(positions, positions[1:])]
            assert min(steps) >= .95 / 60.0 - 1e-8
            assert max(steps) <= 1.05 / 60.0 + 1e-8
            assert abs(positions[-1] - 10.0) < .10
            # An event may be newer than the render timestamp beside it. Do
            # not count that interval twice if calls arrive out of order.
            assert player.position(9.99) == positions[-1]
            assert player.position(10.0) == positions[-1]
            state["paused"] = True
            paused_at = player.last_position
            state["audio"] = 11.0
            assert player.position(11.0) == paused_at
            state["paused"], state["audio"] = False, None
            assert abs(player.position(12.0) - paused_at - 1.0) < 1e-8
            state["audio"] = 0.0
            resumed_at = player.last_position
            assert 0 < player.position(12.0 + 1.0 / 60.0) - resumed_at <= 1.0 / 60.0
            return True
        finally:
            renpy.music.get_pos, renpy.music.get_pause = original_pos, original_pause

    def _test_render_character_framing():
        import os
        directory = os.path.join(config.basedir, "test-results/character-layout")
        os.makedirs(directory, exist_ok=True)
        for path in CHARACTER_LAYOUT["actors"]:
            name = os.path.basename(path).removesuffix(".png").replace("-", " ")
            actor = At(renpy.display.image.ImageReference(name), at_center)
            renpy.render_to_file(Fixed(actor, xysize=(1920, 1080)),
                                os.path.join(directory, os.path.basename(path)), resize=True)
        for background, filename in (("bg garden_close", "bright-scene"), ("bg treehouse", "dark-scene")):
            children = [renpy.display.image.ImageReference(background)]
            for name, x in (("lyra young", .16), ("calista home", .38), ("cassia young", .60), ("selene everyday", .82)):
                children.append(Transform(renpy.display.image.ImageReference(name), xalign=x,
                                          yanchor=1.0, ypos=CHARACTER_LAYOUT["foot_y"]))
            renpy.render_to_file(Fixed(*children, xysize=(1920, 1080)),
                                os.path.join(directory, filename + ".png"), resize=True)
        return True

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
        $ persistent.chapter_spoiler_warnings = True
        $ _test_clear_chapter_reading()
    teardown:
        exit

# Keep this identifier: scripts/project.py invokes it explicitly.
testcase chapter_playthrough:
    assert screen "main_menu"
    assert eval (config.version == "0.1-alpha" and config.save_directory == "Astravus-Book-I")
    assert eval (_test_chapter_dialogue_coverage())
    assert eval (not chapter_warning_needed("first_memory") and chapter_warning_needed("garden"))
    assert eval ("About 40–50 minutes" in _test_screen_text("main_menu") and "Version 0.1-alpha" in _test_screen_text("main_menu"))
    screenshot "title"
    click "Chapters"
    click "25 · The news"
    assert screen "chapter_spoiler_warning"
    assert eval (main_menu and visited_scenes == [] and dev_chapter_target == "first_memory")
    screenshot "chapter-spoiler-warning"
    click "Go back"
    assert eval (not renpy.get_screen("chapter_spoiler_warning") and renpy.get_screen("dev_chapters"))
    click "Return"
    click "Begin Book I"
    assert screen "chapter_card" timeout 4.0
    click "Enter the memory"
    assert eval (renpy.showing("cg first_memory") and not renpy.showing("calista")) timeout 4.0
    assert eval (visited_scenes == ["first_memory"] and not lumen_known and not joren_lost)
    assert eval (chapter_warning_needed("garden") and not chapter_warning_needed("first_memory"))
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
    assert eval ("first_memory" in chapter_read_progress()[0] and not chapter_warning_needed("garden") and chapter_warning_needed("plant_disagreement"))
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
    click "Load"
    assert screen "load" timeout 4.0
    screenshot "load-before-automatic"
    # FilePage supplies this accessible label to Ren'Py's native test selector.
    click "File page auto"
    assert eval (FileCurrentPage() == "auto")
    click "Save"
    assert eval (renpy.get_screen("save") and FileCurrentPage() == "1") timeout 4.0
    screenshot "save-from-automatic"
    click "Return"
    assert eval (renpy.music.is_playing(channel="ambience")) timeout 4.0
    run MainMenu(confirm=False)
    assert screen "main_menu" timeout 4.0
    assert eval (not renpy.music.is_playing(channel="ambience") and not renpy.music.is_playing(channel="closing_theme")) timeout 4.0
    run FileLoad(1, confirm=False, page="1")
    assert eval (_history_list[-1].what == "Here, Cali." and scene_key == "garden") timeout 4.0
    click "History"
    assert screen "history"
    screenshot "history"
    click "Return"
    click "Settings"
    assert screen "preferences"
    click "Chapter spoiler warnings: On"
    assert eval (not persistent.chapter_spoiler_warnings and not chapter_warning_needed("loss"))
    click "Chapter spoiler warnings: Off"
    assert eval (persistent.chapter_spoiler_warnings and chapter_warning_needed("loss"))
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
    assert eval (renpy.showing("bg garden_work_area") and renpy.showing("kael young") and childhood_stage == "early")
    screenshot "siblings-garden"
    advance until eval (renpy.showing("cg garden_compromise"))
    assert eval (scene_key == "plant_disagreement" and not any(renpy.showing(tag) for tag in ("calista", "kael", "maia")))
    screenshot "garden-compromise"
    advance until eval (scene_key == "workshop_first" and renpy.showing("arin everyday"))
    assert eval (renpy.showing("bg workshop") and renpy.showing("calista home"))
    screenshot "workshop"
    advance until eval (renpy.music.get_playing(channel="sound") == "audio/flute_attempt.wav")
    assert eval (scene_key == "music_first" and renpy.showing("cg flute_playing") and not renpy.showing("calista"))
    screenshot "first-melody"
    advance until eval (_history_list[-1].what == "That wasn't it.")
    assert eval (renpy.showing("cg flute_rest") and dialogue_portrait("Cali") is None and renpy.get_widget("say", "speaker_portrait") is None)
    assert eval (renpy.music.get_playing(channel="sound") != "audio/flute_first.wav")
    screenshot "flute-rest"
    run FileSave(2, confirm=False, page="1")
    advance
    run FileLoad(2, confirm=False, page="1")
    assert eval (_history_list[-1].what == "That wasn't it." and renpy.showing("cg flute_rest") and renpy.get_widget("say", "speaker_portrait") is None) timeout 4.0
    click "People"
    assert eval (people_names() == ["Cali", "Maia", "Kael", "Arin", "Selene"])
    screenshot "people-selene"
    click "Return"
    advance until eval (renpy.music.get_playing(channel="sound") == "audio/flute_first.wav")
    assert eval (_history_list[-1].what.startswith("We went a few notes at a time."))
    assert eval (renpy.showing("cg flute_playing") and not renpy.showing("selene"))
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
    assert eval (scene_key == "family_rhythm" and renpy.showing("cg flute_playing"))
    screenshot "flute-practice"
    advance until eval (_history_list[-1].what == "You're too slow.")
    assert eval (renpy.showing("cg flute_rest") and dialogue_portrait("Lyra") == "lyra young" and renpy.get_widget("say", "speaker_portrait") is not None)
    screenshot "flute-listener"
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
    assert eval (renpy.showing("cg pond_rescue") and dialogue_portrait("Lyra") is None and renpy.get_widget("say", "speaker_portrait") is None)
    screenshot "pond-rescue"
    advance until eval (_history_list[-1].what == "I slipped.")
    assert eval (renpy.showing("cg pond_comfort") and not any(renpy.showing(tag) for tag in ("calista", "kael", "lyra")))
    screenshot "pond-comfort"
    advance until eval (scene_key == "soup_experiment")
    assert eval (renpy.showing("bg family_home"))
    advance until eval (_history_list[-1].what == "Did someone add something?")
    assert eval (renpy.get_widget("say", "speaker_portrait") is not None)
    screenshot "soup-speaking"
    advance until eval (renpy.showing("calista festive"))
    assert eval (scene_key == "festival_lights" and not renpy.showing("calista festival"))
    screenshot "festival-arrival"
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
    assert eval (scene_key == "meeting_cassia" and renpy.showing("cg cassia_storytelling") and not renpy.showing("cassia"))
    screenshot "cassia-storytelling"
    advance until eval (_history_list[-1].who == "Thalia")
    assert eval ("Thalia" in people_names() and "Lyron" not in people_names())
    assert eval (dialogue_portrait("Thalia") == "thalia everyday" and renpy.get_widget("say", "speaker_portrait") is not None)
    screenshot "thalia-speaking"
    advance until eval (_history_list[-1].who == "Lyron")
    assert eval (dialogue_portrait("Lyron") == "lyron everyday" and renpy.get_widget("say", "speaker_portrait") is not None)
    screenshot "lyron-speaking"
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
    advance until eval (_history_list[-1].who == "Soren")
    assert eval (dialogue_portrait("Soren") == "soren everyday" and renpy.get_widget("say", "speaker_portrait") is not None)
    screenshot "soren-speaking"
    advance until eval (_history_list[-1].who == "Kaleb")
    assert eval (dialogue_portrait("Kaleb") == "kaleb everyday" and renpy.get_widget("say", "speaker_portrait") is not None)
    screenshot "kaleb-speaking"
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
    advance until eval (renpy.showing("cg family_embrace"))
    assert eval (scene_key == "family_grief" and not renpy.showing("maia") and not renpy.showing("calista"))
    screenshot "family-embrace"
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
    advance until eval (renpy.showing("cg cassia_comfort"))
    assert eval (scene_key == "cassia_grief" and not renpy.showing("cassia") and not renpy.showing("calista"))
    screenshot "cassia-comfort"
    advance until eval (scene_key == "community_memorial")
    assert eval (not renpy.showing("joren"))
    screenshot "memorial"
    advance until eval (scene_key == "mural_remembrance")
    assert eval (not renpy.showing("joren"))
    screenshot "mural"
    advance until eval (scene_key == "treehouse_remembrance")
    assert eval (renpy.showing("bg treehouse_memory") and not renpy.showing("joren"))
    screenshot "remembering-in-rain"
    advance until screen "book_afterword"
    assert eval ("laughter, love, and wonder" in _test_screen_text("book_afterword") and renpy.get_widget("book_afterword", "itch_link").action.url == ITCH_URL)
    screenshot "afterword"
    click "Finish Book I"
    assert screen "chapter_end"
    assert eval (chapter_read_progress()[0] == set(BOOK_SCENE_KEYS) and not chapter_warning_needed("loss"))
    assert eval (persistent.book_one_complete and visited_scenes == list(BOOK_SCENE_KEYS))
    assert eval (scene_number == BOOK_SCENE_COUNT == 32 and scene_key == "annual_remembrance")
    assert eval (lumen_known and joren_lost and childhood_stage == "later")
    screenshot "end"
    click "Credits"
    assert screen "about"
    assert eval (("{a=" + ASTRAVUS_REPO_URL + "}dgoldman0{/a}") in renpy.get_widget("about", "author_credit").get_all_text() and renpy.get_widget("about", "itch_link").action.url == ITCH_URL)
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
    assert eval (renpy.showing("cg family_embrace") and dialogue_portrait("Maia") is None and renpy.get_widget("say", "speaker_portrait") is None)
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
    assert eval (renpy.music.get_playing() == "audio/outward_paths.ogg") timeout 4.0
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
    advance until screen "book_afterword"
    click "Finish Book I"
    assert screen "chapter_end"
    click "Return to title"
    click "Chapters"
    click "01 · First memory"
    assert screen "chapter_card" timeout 4.0
    click "Enter the memory"
    assert eval (visited_scenes == ["first_memory"] and not joren_lost and not lumen_known and people_names() == ["Cali"] and familiar_names() == []) timeout 4.0
    # Jumping ahead must not convert reconstructed story state into read text.
    $ _test_clear_chapter_reading()
    click "Chapters"
    click "25 · The news"
    assert screen "chapter_spoiler_warning"
    click "Jump anyway"
    assert eval (scene_key == "loss" and visited_scenes == list(BOOK_SCENE_KEYS[:25])) timeout 4.0
    assert eval (not chapter_read_progress()[0] and chapter_warning_needed("family_grief") and chapter_warning_needed("garden"))
    run FileSave(11, confirm=False, page="1")
    click "Chapters"
    click "26 · What comfort can do"
    assert screen "chapter_spoiler_warning"
    click "Go back"
    click "Return"
    assert eval (scene_key == "loss")
    click "Settings"
    click "Chapter spoiler warnings: On"
    click "Return"
    click "Chapters"
    click "26 · What comfort can do"
    assert eval (scene_key == "family_grief" and not renpy.get_screen("chapter_spoiler_warning")) timeout 4.0
    run FileLoad(11, confirm=False, page="1")
    assert eval (scene_key == "loss" and not persistent.chapter_spoiler_warnings) timeout 4.0
    click "Settings"
    click "Chapter spoiler warnings: Off"
    click "Return"
    assert eval (persistent.chapter_spoiler_warnings and chapter_warning_needed("garden"))
    exit

# Focused review for the closing-film addition; avoids a full-book release run.
testcase character_framing_review:
    assert screen "main_menu"
    assert eval (_test_render_character_framing())
    exit

testcase environment_grounding_review:
    assert screen "main_menu"
    $ persistent.chapter_spoiler_warnings = False
    $ _test.force = True
    click "Chapters"
    click "15 · Something worth finding"
    advance until eval (renpy.showing("calista young") and renpy.showing("joren young"))
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "grounding-first-joren"
    keysym "h"
    click "Chapters"
    click "17 · Beyond the familiar paths"
    advance until eval (renpy.showing("calista home") and renpy.showing("joren young"))
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "grounding-kaleb-path"
    keysym "h"
    click "Chapters"
    click "21 · The unfinished world"
    advance until eval (renpy.showing("nibble"))
    assert eval (renpy.showing("bg construction_path") and renpy.showing("calista older") and renpy.showing("joren older"))
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "grounding-expedition-path"
    keysym "h"
    advance until eval (renpy.showing("bg construction_room"))
    keysym "h"
    pause .25
    screenshot "grounding-construction-room"
    keysym "h"
    click "Chapters"
    click "23 · The view from above"
    advance until eval (renpy.showing("calista older") and renpy.showing("joren older"))
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "grounding-dome-path"
    keysym "h"
    click "Chapters"
    click "08 · The days between"
    advance until eval (renpy.showing("shadow") and renpy.showing("bg music_room"))
    keysym "h"
    pause .25
    screenshot "grounding-music-familiars"
    keysym "h"
    click "Chapters"
    click "09 · The Tree of Echoes"
    advance until eval (renpy.showing("calista home") and renpy.showing("barkley"))
    keysym "h"
    pause .25
    screenshot "grounding-echoes-familiars"
    keysym "h"
    click "Chapters"
    click "20 · Something that turns"
    advance until eval (renpy.showing("nibble") and renpy.showing("bg waterwheel"))
    keysym "h"
    pause .25
    screenshot "grounding-waterwheel-familiars"
    keysym "h"
    click "Chapters"
    click "24 · Which way we go"
    advance until eval (renpy.showing("nibble"))
    keysym "h"
    pause .25
    screenshot "grounding-dispute-familiars"
    keysym "h"
    click "Chapters"
    click "01 · First memory"
    advance until eval (renpy.showing("nibble") and renpy.showing("bg family_home"))
    keysym "h"
    pause .25
    screenshot "grounding-home-familiars"
    keysym "h"
    click "Chapters"
    click "28 · Between the two of us"
    advance until eval (renpy.showing("cassia mourning") and renpy.showing("calista mourning"))
    keysym "h"
    pause .25
    screenshot "grounding-treehouse-grief"
    keysym "h"
    click "Chapters"
    click "02 · A small beginning"
    advance until eval (renpy.showing("calista young") and renpy.showing("maia"))
    assert eval (renpy.showing("bg garden_close"))
    keysym "h"
    assert eval (_windows_hidden)
    pause .25
    screenshot "grounding-garden-default"
    exit

testcase closing_theme_review:
    assert screen "main_menu"
    assert eval (_test_theme_buffered_clock())
    $ persistent.chapter_spoiler_warnings = False
    click "Chapters"
    click "32 · What remains"
    advance until screen "book_afterword"
    assert eval ("laughter, love, and wonder" in _test_screen_text("book_afterword"))
    screenshot "theme-afterword"
    click "Play closing theme"
    assert screen "closing_theme"
    assert eval (renpy.music.is_playing(channel="closing_theme")) timeout 5.0
    assert eval (renpy.get_widget("closing_theme", "montage").reduced_motion)
    pause 1.0
    screenshot "theme-reduced-motion"
    click "Pause"
    assert eval (renpy.music.get_pause(channel="closing_theme"))
    $ _theme_paused_at = renpy.get_widget("closing_theme", "montage").position()
    pause .6
    assert eval (abs(renpy.get_widget("closing_theme", "montage").position() - _theme_paused_at) < .1)
    click "Resume"
    pause .6
    assert eval (renpy.get_widget("closing_theme", "montage").position() > _theme_paused_at + .2)
    click "Skip closing theme"
    assert screen "chapter_end"
    assert eval (not renpy.music.is_playing(channel="closing_theme"))
    $ persistent.reduced_motion = False
    click "Replay closing theme"
    assert screen "closing_theme"
    assert eval (not renpy.get_widget("closing_theme", "montage").reduced_motion)
    pause 1.5
    screenshot "theme-camera-motion"
    # The clock keeps advancing even when an audio backend supplies no position.
    run Stop("closing_theme")
    $ _theme_silent_at = renpy.get_widget("closing_theme", "montage").position()
    pause .6
    assert eval (renpy.get_widget("closing_theme", "montage").position() > _theme_silent_at + .2)
    $ renpy.get_widget("closing_theme", "montage").last_position = 11.0
    run Function(renpy.music.set_pause, True, channel="closing_theme")
    screenshot "theme-blended-transition"
    run Function(renpy.music.set_pause, False, channel="closing_theme")
    $ renpy.get_widget("closing_theme", "montage").last_position = 106.0
    pause .2
    screenshot "theme-friends"
    $ renpy.get_widget("closing_theme", "montage").last_position = 173.0
    pause .2
    screenshot "theme-final-title"
    $ renpy.get_widget("closing_theme", "montage").last_position = CLOSING_THEME["duration"]
    assert screen "chapter_end" timeout 3.0
    click "Replay closing theme"
    click "Pause"
    click "Skip closing theme"
    assert screen "chapter_end"
    click "Replay closing theme"
    assert eval (not renpy.music.get_pause(channel="closing_theme"))
    click "Skip closing theme"
    click "Return to title"
    click "Continue"
    assert screen "chapter_end" timeout 10.0
    assert eval (not renpy.music.is_playing(channel="closing_theme"))
