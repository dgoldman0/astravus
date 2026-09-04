# Development-only tests. This file is excluded from exported builds.
testsuite global:
    setup:
        $ _test.transition_timeout = 0.05
        $ _test.screenshot_directory = renpy.config.basedir + "/test-results/screenshots"
        $ preferences.text_cps = 0
        $ persistent.large_text = False
        $ persistent.high_contrast = False
        $ persistent.reduced_motion = False
    teardown:
        exit

testcase chapter_playthrough:
    assert screen "main_menu"
    screenshot "title"
    click "Begin the chapter"
    assert screen "chapter_card" timeout 4.0
    click "Enter the memory"
    assert eval (renpy.showing("cg first_memory") and not renpy.showing("calista")) timeout 4.0
    screenshot "first-memory"
    advance until eval (renpy.showing("bg family_home"))
    assert eval (not renpy.showing("cg"))
    advance until eval (_history_list[-1].what.startswith("The home I grew"))
    screenshot "family-home"
    advance until eval (scene_number == 2)
    advance
    advance
    assert eval (_history_list[-1].what == "Here, Cali.")
    assert eval (renpy.showing("bg garden_close") and not renpy.showing("cg"))
    screenshot "garden"
    run FileSave(1, confirm=False, page="1")
    advance
    advance
    run FileLoad(1, confirm=False, page="1")
    assert eval (_history_list[-1].what == "Here, Cali.") timeout 4.0
    click "History"
    assert screen "history"
    screenshot "history"
    click "Return"
    click "Settings"
    assert screen "preferences"
    click "Larger dialogue text"
    click "Solid dialogue background"
    click "Reduced motion"
    assert eval (persistent.large_text and persistent.high_contrast and persistent.reduced_motion)
    screenshot "settings"
    click "Return"
    screenshot "large-text"
    click "Settings"
    click "Solid dialogue background"
    click "Return"
    advance until eval (met_cassia)
    assert eval (renpy.showing("bg community_courtyard"))
    click "People"
    assert screen "people"
    screenshot "people"
    click "Return"
    advance until eval (met_joren)
    assert eval (renpy.showing("bg construction_path"))
    screenshot "construction"
    advance until eval (renpy.showing("bg family_home"))
    assert eval (scene_number == 4 and not renpy.showing("joren"))
    advance until eval (scene_number == 5)
    advance until eval (renpy.showing("bg treehouse"))
    advance until eval (renpy.showing("cassia"))
    advance
    screenshot "treehouse"
    advance until eval (renpy.showing("bg treehouse_rain"))
    assert eval (renpy.music.get_playing(channel="ambience") == "audio/rain.wav") timeout 4.0
    assert eval (not renpy.showing("cassia") and not renpy.showing("joren"))
    screenshot "treehouse-rain"
    run Rollback(force=True)
    assert eval (renpy.showing("bg treehouse")) timeout 4.0
    assert eval (renpy.music.get_playing(channel="ambience") == "audio/garden_air.wav") timeout 4.0
    advance until eval (renpy.showing("bg treehouse_rain"))
    assert eval (renpy.music.get_playing(channel="ambience") == "audio/rain.wav") timeout 4.0
    advance until screen "chapter_end"
    assert eval (persistent.chapter_complete)
    screenshot "end"
    click "Return to title"
    assert screen "main_menu" timeout 4.0
    click "Continue"
    assert screen "chapter_end" timeout 10.0
    screenshot "resumed"
    assert eval (scene_number == 5)
    click "Return to title"
    assert screen "main_menu" timeout 4.0
    click "Credits"
    assert screen "about"
    click "Return"
    click "How to read"
    assert screen "help"
    exit
