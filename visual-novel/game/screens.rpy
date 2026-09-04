# Custom interface. Standard Ren'Py actions handle game state and accessibility.
init offset = -1

style default:
    font "fonts/Lato-Regular.ttf"
    size 28
    color "#eee7d8"

style button:
    padding (18, 12)
    background None
    hover_background Solid("#d7bb8620")

style button_text:
    color "#c3cdc5"
    hover_color "#f6d99f"
    selected_color "#f6d99f"
    insensitive_color "#687772"
    size 28

style label_text:
    color "#d9bf8e"
    size 27

style slider:
    xsize 510
    ysize 28
    base_bar Solid("#36504d")
    left_bar Solid("#bdac82")
    thumb Solid("#ecd5a0", xsize=12, ysize=28)
    thumb_offset 0

style bar is slider

style vscrollbar:
    xsize 8
    base_bar Solid("#213b38")
    thumb Solid("#9aaa90")

style input:
    color "#f5dcac"

style title_text:
    font "fonts/Story-Serif.ttf"
    color "#f4e7cb"
    size 67

style eyebrow_text:
    size 19
    kerning 4
    color "#d3bb8e"

style small_text:
    size 23
    color "#b6c3b9"

screen main_menu():
    tag menu
    add "bg garden"
    add "ui/menu-shade.svg"
    vbox:
        xpos 130
        ypos 110
        spacing 18
        add "ui/constellation.svg"
        text "A S T R A V U S" style "title_text" size 67
        text "SEEDS OF YOUTH" style "eyebrow_text" size 24
        null height 12
        text "A life remembered.\nA world that holds it." size 31 color "#c6ccbc" line_spacing 8
        null height 20
        if latest_reading_slot():
            textbutton "Continue" action FileLoad(latest_reading_slot(), slot=True, confirm=False) style "title_button"
        textbutton "Begin Book I" action Start() style "title_button"
        hbox:
            spacing 14
            textbutton "Load" action ShowMenu("load")
            textbutton "Settings" action ShowMenu("preferences")
            textbutton "Credits" action ShowMenu("about")
        textbutton "How to read" action ShowMenu("help")
        if not renpy.variant("web"):
            textbutton "Quit" action Quit(confirm=False)
    vbox:
        xpos 150
        ypos 932
        spacing 12
        text "BOOK I   /   SEEDS OF YOUTH" style "eyebrow_text"
        text "The complete first book · A kinetic novel · About an hour" style "small_text" size 20
    text "01" xpos 1780 ypos 936 font "fonts/Story-Serif.ttf" size 64 color "#e6cf9b"

style title_button:
    xsize 450
    padding (20, 16)
    background Solid("#c2ae8522")
    hover_background Solid("#c2ae8540")

style title_button_text:
    size 33
    color "#f4e5c9"
    hover_color "#ffffff"

screen say(who, what):
    if pending_scene_save == scene_key:
        timer 0.5 repeat True action Function(save_scene_checkpoint)
    add "ui/dialogue-shade.svg" yalign 1.0
    if persistent.high_contrast:
        add Solid("#061719", xsize=1920, ysize=300) pos (0, 780) anchor (0, 0)
    window:
        id "window"
        background None
        xpos 230
        ypos 807
        xsize 1460
        ysize 215
        vbox:
            spacing 13
            if who is not None:
                text who id "who" size 26
            else:
                text "CALISTA · A MEMORY" style "eyebrow_text" size 18
            text what id "what" size readable_text() line_spacing 7
    text "[scene_title]" xpos 60 ypos 40 size 23 color "#e8ddc8" outlines [(1, "#081b1c", 0, 1)]
    text "[scene_number:02d] / [BOOK_SCENE_COUNT:02d]" xpos 1750 ypos 40 size 20 color "#e8ddc8" outlines [(1, "#081b1c", 0, 1)]

screen quick_menu():
    zorder 100
    if quick_menu and not main_menu:
        hbox:
            xalign 0.5
            yalign 1.0
            spacing 18
            style_prefix "quick"
            textbutton "Back" action Rollback()
            textbutton "History" action ShowMenu("history")
            textbutton "Save" action ShowMenu("save")
            textbutton "Load" action ShowMenu("load")
            textbutton "Auto" action Preference("auto-forward", "toggle")
            textbutton "Skip" action Skip() alternate Skip(fast=True, confirm=True)
            textbutton "People" action ShowMenu("people")
            textbutton "Settings" action ShowMenu("preferences")

init python:
    config.overlay_screens.append("quick_menu")

style quick_button:
    padding (12, 11)

style quick_button_text:
    size 21
    color "#aebdb2"
    hover_color "#f4d698"
    selected_color "#f4d698"

screen chapter_card(kicker, title, subtitle):
    modal True
    add Solid("#07191de8")
    vbox:
        xalign .5
        yalign .47
        spacing 30
        add "ui/constellation.svg" xalign .5
        text kicker style "eyebrow_text" xalign .5
        text title style "title_text" xalign .5
        text subtitle size 28 color "#b4c1b5" xalign .5
        null height 35
        textbutton "Enter the memory" action Return() xalign .5
    key "dismiss" action Return()

screen chapter_end():
    modal True
    add Solid("#07191dd9")
    vbox:
        xalign .5
        yalign .45
        spacing 25
        text "END OF BOOK I · SEEDS OF YOUTH" style "eyebrow_text" xalign .5
        text "What remains." style "title_text" xalign .5
        text "Thank you for sharing this part of Calista's life." size 29 color "#bfcabb" xalign .5
        null height 25
        textbutton "Return to title" action Return() xalign .5
        textbutton "Credits" action ShowMenu("about") xalign .5

# Every menu shares one navigation system; Return restores the reading position.
screen book_menu(title):
    add "bg garden"
    add Solid("#07191df5")
    add Solid("#c5ac7d") xpos 380 ypos 115 xsize 1 ysize 850
    vbox:
        xpos 60
        ypos 105
        spacing 15
        add "ui/constellation.svg"
        text "ASTRAVUS" style "eyebrow_text" size 24
        null height 22
        textbutton "Return" action Return()
        if not main_menu:
            textbutton "Save" action ShowMenu("save")
            textbutton "History" action ShowMenu("history")
            textbutton "People" action ShowMenu("people")
        textbutton "Load" action ShowMenu("load")
        textbutton "Settings" action ShowMenu("preferences")
        textbutton "How to read" action ShowMenu("help")
        textbutton "Credits" action ShowMenu("about")
        if not main_menu:
            textbutton "Title screen" action MainMenu()
        if not renpy.variant("web"):
            textbutton "Quit" action Quit()
    text title style "title_text" xpos 450 ypos 108 size 53
    frame:
        xpos 450
        ypos 215
        xsize 1380
        ysize 795
        background None
        padding (0, 0)
        transclude
    key "game_menu" action Return()

screen pause_menu():
    tag menu
    use book_menu("A moment of quiet"):
        vbox:
            spacing 26
            text "Your place in the story is kept while you pause." size 33
            text "[scene_title]" color "#d9bf8e"
            textbutton "Keep reading" action Return()
            textbutton "Quick save" action [QuickSave(), Notify("Your place is saved.")]

screen save():
    tag menu
    use file_slots("Save your place", saving=True)

screen load():
    tag menu
    use file_slots("Return to a memory")

screen file_slots(title, saving=False):
    use book_menu(title):
        vbox:
            spacing 22
            hbox:
                spacing 18
                textbutton "Automatic" action FilePage("auto")
                textbutton "Quick" action FilePage("quick")
                for page in range(1, 4):
                    textbutton "[page]" action FilePage(page)
            grid 3 2:
                spacing 24
                for slot in range(1, 7):
                    button:
                        xsize 420
                        ysize 288
                        padding (15, 15)
                        background Solid("#1a3030")
                        hover_background Solid("#2c4240")
                        action FileAction(slot)
                        sensitive saving or FileJson(slot, "book_id") == BOOK_SAVE_ID
                        key "save_delete" action FileDelete(slot)
                        vbox:
                            spacing 8
                            add FileScreenshot(slot) xysize (390, 219)
                            if FileLoadable(slot) and FileJson(slot, "book_id") != BOOK_SAVE_ID:
                                text "Earlier draft save" size 23
                            else:
                                text FileTime(slot, format="%b %d · %H:%M", empty="Empty slot") size 23
            text "Automatic saves keep each new scene. Manual saves keep your exact place." style "small_text"

screen preferences():
    tag menu
    use book_menu("Make yourself comfortable"):
        vbox:
            spacing 25
            hbox:
                spacing 70
                vbox:
                    spacing 15
                    label "Reading"
                    text "Text reveal speed" size 24
                    bar value Preference("text speed")
                    text "Auto-advance delay" size 24
                    bar value Preference("auto-forward time")
                    textbutton "Larger dialogue text" action ToggleField(persistent, "large_text")
                    textbutton "Solid dialogue background" action ToggleField(persistent, "high_contrast")
                    textbutton "Reduced motion" action ToggleField(persistent, "reduced_motion")
                    textbutton "Self-voicing" action Preference("self voicing", "toggle")
                vbox:
                    spacing 15
                    label "Sound"
                    text "Music" size 24
                    bar value Preference("music volume")
                    text "Environment and effects" size 24
                    bar value Preference("sound volume")
                    textbutton "Mute all sound" action Preference("all mute", "toggle")
                    null height 10
                    label "Display"
                    hbox:
                        textbutton "Window" action Preference("display", "window")
                        textbutton "Full screen" action Preference("display", "fullscreen")
            null height 10
            label "Skipping"
            textbutton "Allow skipping unread text" action Preference("skip", "toggle")
            text "Click once to reveal a line, then again to advance.\nYou can read at your own pace; no response is timed." style "small_text" line_spacing 8

screen history():
    tag menu
    predict False
    use book_menu("The words we keep"):
        viewport:
            scrollbars "vertical"
            mousewheel True
            draggable True
            yinitial 1.0
            vbox:
                spacing 27
                if not _history_list:
                    text "Your reading history will appear here."
                for entry in _history_list:
                    vbox:
                        spacing 7
                        if entry.who:
                            text entry.who size 23 color "#d6be8c" substitute False
                        text entry.what size 29 xmaximum 1250 line_spacing 5 substitute False

screen people():
    tag menu
    use book_menu("A constellation of people"):
        viewport:
            scrollbars "vertical"
            mousewheel True
            draggable True
            vbox:
                spacing 25
                text "The people you have met" style "eyebrow_text"
                text "Cali / Calista" color "#d9bf8e" size 31
                text "A curious child who sees the world through color and drawing. Her older self is remembering these scenes." xmaximum 1220
                text "Her five parents" color "#d9bf8e" size 31
                text "Maia tends living ecosystems. Arin designs biomechanical interfaces. Selene works with sound. Dorian keeps oral histories. Sage helps people through transitions. Together they raise Cali, her older brother Kael, and her younger sister Lyra." xmaximum 1220 line_spacing 6
                if met_cassia:
                    text "Cassia" color "#d9bf8e" size 31
                    if joren_lost:
                        text "Cali's closest friend, a storyteller. They are learning how to remember Joren together." xmaximum 1220
                    else:
                        text "Cali's friend: a storyteller who always has room for one more idea." xmaximum 1220
                if "cassia_home" in visited_scenes:
                    text "Thalia and Lyron" color "#d9bf8e" size 31
                    text "Cassia's parents. Thalia helps people resolve disagreements; Lyron tends agricultural systems and shares a friendship with Dorian." xmaximum 1220 line_spacing 6
                if met_joren:
                    text "Joren" color "#d9bf8e" size 31
                    text people_joren_description() xmaximum 1220
                if "joren_home" in visited_scenes:
                    text "Soren" color "#d9bf8e" size 31
                    text "Joren's mother, a systems designer whose workshop is full of tools, plans and unfinished inventions." xmaximum 1220
                if "kaleb_walk" in visited_scenes:
                    text "Kaleb" color "#d9bf8e" size 31
                    text "Joren's father, an explorer who shares his discoveries and the stories of his journeys." xmaximum 1220
                text "Lumen" color "#d9bf8e" size 31
                text people_lumen_description() xmaximum 1220 line_spacing 6

screen help():
    tag menu
    use book_menu("Take your time"):
        vbox:
            spacing 26
            text "Book I tells one fixed story. There are no branching paths or timed choices." xmaximum 1210 size 32
            for control, description in [("Click · Enter · Space", "Reveal the current line, then move to the next."), ("Mouse wheel up · Page Up", "Return to an earlier line."), ("Escape · Right click", "Open or close the reading menu."), ("H", "Hide the interface to look at the illustration."), ("V", "Toggle self-voicing."), ("Touch", "Tap to read; use the bottom controls for menus and history.")]:
                hbox:
                    text control xsize 420 color "#d9bf8e" size 26
                    text description xmaximum 825 size 26
            text "Auto advances the text for you. Skip moves through previously read lines.\nSettings include larger text, stronger contrast, reduced motion, and separate sound controls." xmaximum 1250 style "small_text" line_spacing 8

screen about():
    tag menu
    use book_menu("Made from a remembered world"):
        viewport:
            scrollbars "vertical"
            mousewheel True
            draggable True
            vbox:
                spacing 25
                text "Astravus · Seeds of Youth" size 35 color "#d9bf8e"
                text "An adaptation of Book I of Calista's story from the Astravus Collection by dgoldman0." xmaximum 1200
                text "Story, world, and original visual references\nThe Astravus Collection" line_spacing 7
                text "Adaptation, interface, and implementation\nDeveloped with Codex" line_spacing 7
                text "Illustrations\nGenerated with OpenAI image generation using the collection's visual references, with editorial review." xmaximum 1200 line_spacing 7
                text "Sound\nOriginal synthesized score, environmental sound and musical lesson cues created for this adaptation. No downloaded recordings or sample libraries." xmaximum 1200 line_spacing 7
                text "Typography\nLato by Łukasz Dziedzic · DejaVu Serif by the DejaVu project\nFont licenses are included with the game." line_spacing 7
                text "Built with Ren'Py [renpy.version_only]. Engine license information is included in the distribution." xmaximum 1200
                textbutton "Ren'Py licenses" action OpenURL("https://www.renpy.org/doc/html/license.html")
                text "Book I preview · Version [config.version]" style "small_text"

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid("#031013e8")
    frame:
        xalign .5
        yalign .5
        padding (60, 45)
        background Solid("#172e2e")
        vbox:
            spacing 35
            text message xmaximum 980 text_align .5 xalign .5 size 32
            hbox:
                xalign .5
                spacing 65
                textbutton "Yes" action yes_action
                textbutton "No" action no_action
    key "game_menu" action no_action

screen notify(message):
    zorder 110
    frame:
        xpos 50
        ypos 100
        padding (25, 15)
        background Solid("#102c2def")
        text message size 24
    timer 3.0 action Hide("notify")

screen skip_indicator():
    zorder 110
    text "Skipping · click to stop" xpos 70 ypos 90 size 22 color "#f5d99a"
