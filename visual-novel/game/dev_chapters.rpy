# Chapter selection remains available in the alpha, with optional spoiler warnings.
define DEV_CHAPTER_SELECT = True
default dev_chapter_target = "first_memory"
default persistent.chapter_spoiler_warnings = True

init python:
    DEV_CHAPTER_LABELS = {
        "first_memory": "chapter_one", "garden": "garden_lesson",
        "plant_disagreement": "family_plant_disagreement",
        "workshop_first": "family_workshop_first",
        "music_first": "family_music_first",
        "dorian_stories": "family_dorian_stories",
        "sage_story": "family_sage_story",
        "family_rhythm": "family_daily_rhythm",
        "tree_echoes": "family_tree_echoes",
        "pond_scare": "family_pond_scare",
        "soup_experiment": "family_soup_experiment",
        "festival_lights": "family_festival_lights",
        "meeting_cassia": "meeting_cassia", "cassia_home": "cassia_family_visit",
        "meeting_joren": "meeting_joren", "joren_home": "joren_family_visit",
        "kaleb_walk": "chapter_kaleb_walk", "treehouse": "the_treehouse",
        "rain_refuge": "chapter_rain_refuge", "waterwheel": "book_one_later",
    }
    DEV_CHAPTER_LABELS.update({key: "chapter_" + key for key in BOOK_SCENE_KEYS[20:]})

    # Use the engine's existing per-line reading record, which survives saves,
    # rollback and upgrades. visited_scenes is unsuitable: jumps populate it with
    # earlier scenes to reconstruct the destination's story state.
    # The pinned SDK's translation catalog supplies the IDs of the compiled
    # dialogue; no second list of script text or completion flags is maintained.
    CHAPTER_DIALOGUE_IDS = {key: [] for key in BOOK_SCENE_KEYS}
    _chapter_for_label = {label: key for key, label in DEV_CHAPTER_LABELS.items()}
    _chapter_for_label["after_joren_family"] = "kaleb_walk"
    for _translations in renpy.game.script.translator.file_translates.values():
        for _label, _node in _translations:
            if _label in _chapter_for_label:
                CHAPTER_DIALOGUE_IDS[_chapter_for_label[_label]].append(_node.identifier)

    def chapter_read_progress():
        read, reached = set(), set()
        for key, identifiers in CHAPTER_DIALOGUE_IDS.items():
            seen = [renpy.seen_translation(identifier) for identifier in identifiers]
            if any(seen):
                reached.add(key)
            if seen and all(seen):
                read.add(key)
        # The currently displayed line is recorded when it is dismissed. It is
        # still safe to return to this scene while that first line is on screen.
        if not renpy.store.main_menu and renpy.store._history_list:
            reached.add(renpy.store.scene_key)
        return read, reached

    def chapter_warning_needed(key, progress=None):
        if not persistent.chapter_spoiler_warnings:
            return False
        read, reached = progress if progress is not None else chapter_read_progress()
        if key in reached:
            return False
        earlier = BOOK_SCENE_KEYS[:BOOK_SCENE_KEYS.index(key)]
        return any(previous not in read for previous in earlier)

    def chapter_start_action(key):
        return [Hide("chapter_spoiler_warning"), SetVariable("dev_chapter_target", key), Start("dev_chapter_start")]

    # These scenes normally inherit their score from the preceding scene.
    DEV_INHERITED_MUSIC = {
        "kaleb_walk": "audio/discovery_theme.ogg",
        "outer_exploration": "audio/discovery_theme.ogg",
        "painting_grief": "audio/grief_theme.ogg",
        "cassia_grief": "audio/grief_theme.ogg",
        "mural_remembrance": "audio/remembrance_theme.ogg",
        "treehouse_remembrance": "audio/remembrance_theme.ogg",
        "annual_remembrance": "audio/remembrance_theme.ogg",
    }

    def prepare_chapter_start(key):
        index = BOOK_SCENE_KEYS.index(key)
        renpy.store.visited_scenes = list(BOOK_SCENE_KEYS[:index])
        renpy.store.pending_scene_save = None
        renpy.store.met_cassia = index > BOOK_SCENE_KEYS.index("meeting_cassia")
        renpy.store.met_joren = index > BOOK_SCENE_KEYS.index("meeting_joren")
        renpy.store.lumen_known = index > BOOK_SCENE_KEYS.index("tree_echoes")
        renpy.store.joren_lost = index > BOOK_SCENE_KEYS.index("loss")
        renpy.store.childhood_stage = "later" if index >= BOOK_SCENE_KEYS.index("waterwheel") else "early"
        renpy.store._history_list = []
        renpy.store.quick_menu = True
        renpy.set_return_stack([])
        renpy.block_rollback()
        for channel in ("music", "ambience", "sound"):
            renpy.music.stop(channel=channel)
        if key in DEV_INHERITED_MUSIC:
            renpy.music.play(DEV_INHERITED_MUSIC[key], fadein=1.0)
        if key == "painting_grief":
            renpy.music.play("audio/room_air.ogg", channel="ambience", fadein=1.0)

screen dev_chapters():
    tag menu
    $ reading_progress = chapter_read_progress()
    use book_menu("Chapters"):
        if DEV_CHAPTER_SELECT:
            vbox:
                spacing 20
                text "Choose a chapter to start there. Unread jumps may reveal later events." style "small_text"
                vpgrid:
                    cols 3
                    spacing 10
                    xsize 1340
                    ysize 720
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    pagekeys True
                    for number, (key, title) in enumerate(BOOK_SCENES, 1):
                        textbutton "[number:02d] · [title]":
                            xsize 430
                            ysize 55
                            padding (14, 8)
                            text_size 25
                            background Solid("#c2ae8512")
                            hover_background Solid("#c2ae8530")
                            selected_background Solid("#c2ae8538")
                            selected not main_menu and key == scene_key
                            action If(chapter_warning_needed(key, reading_progress), Show("chapter_spoiler_warning", target=key), chapter_start_action(key))
                    null width 430 height 55

screen chapter_spoiler_warning(target):
    modal True
    zorder 250
    add Solid("#031013e8")
    frame:
        xalign .5
        yalign .5
        xsize 1120
        padding (60, 45)
        background Solid("#172e2e")
        vbox:
            spacing 28
            text "Spoilers ahead" size 43 color "#d9bf8e"
            text "You haven't read everything before this chapter. Jumping ahead may reveal later events." size 32 xmaximum 980 line_spacing 8
            text "You can turn chapter spoiler warnings off in Settings." style "small_text"
            hbox:
                xalign 1.0
                spacing 35
                textbutton "Go back" action Hide("chapter_spoiler_warning") default_focus True
                textbutton "Jump anyway" action chapter_start_action(target)
    key "game_menu" action Hide("chapter_spoiler_warning")

label dev_chapter_start:
    if not DEV_CHAPTER_SELECT:
        jump start
    $ prepare_chapter_start(dev_chapter_target)
    scene black
    window auto

    # Family episodes normally return to a caller that schedules the next one.
    # Recreate that continuation when entering partway through the sequence.
    if dev_chapter_target in BOOK_SCENE_KEYS[2:12]:
        $ dev_family_index = BOOK_SCENE_KEYS.index(dev_chapter_target)
        while dev_family_index < 12:
            call expression DEV_CHAPTER_LABELS[BOOK_SCENE_KEYS[dev_family_index]]
            $ dev_family_index += 1
        jump meeting_cassia
    elif dev_chapter_target == "cassia_home":
        call cassia_family_visit
        jump meeting_joren
    elif dev_chapter_target in ("joren_home", "kaleb_walk"):
        call expression DEV_CHAPTER_LABELS[dev_chapter_target]
        jump after_joren_family
    else:
        jump expression DEV_CHAPTER_LABELS[dev_chapter_target]
