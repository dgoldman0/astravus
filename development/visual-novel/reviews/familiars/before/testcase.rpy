testcase familiar_compositing_review:
    assert screen "main_menu"
    $ persistent.chapter_spoiler_warnings = False
    $ _test.force = True
    $ _test.screenshot_directory = "/tmp/astravus-familiar-runtime/before"
    click "Chapters"
    click "09 · The Tree of Echoes"
    advance until eval (renpy.showing("calista home") and renpy.showing("barkley"))
    pause .25
    screenshot "echoes-dialogue"
    keysym "h"
    pause .25
    screenshot "echoes-clean"
    keysym "h"
    click "Chapters"
    click "21 · The unfinished world"
    advance until eval (renpy.showing("nibble") and renpy.showing("bg construction_path"))
    pause .25
    screenshot "construction-path-dialogue"
    keysym "h"
    pause .25
    screenshot "construction-path-clean"
    keysym "h"
    advance until eval (renpy.showing("bg construction_room"))
    pause .25
    screenshot "construction-room-dialogue"
    keysym "h"
    pause .25
    screenshot "construction-room-clean"
    keysym "h"
    click "Chapters"
    click "01 · First memory"
    advance until eval (renpy.showing("nibble") and renpy.showing("bg family_home"))
    pause .25
    screenshot "home-dialogue"
    keysym "h"
    pause .25
    screenshot "home-clean"
    exit
