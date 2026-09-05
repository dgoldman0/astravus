# Included in production previews. Set False to hide chapter jumping for release.
define DEV_CHAPTER_SELECT = True
default dev_chapter_target = "first_memory"

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
    use book_menu("Chapters · development"):
        if DEV_CHAPTER_SELECT:
            vbox:
                spacing 20
                text "Choose a scene to start there and keep reading." style "small_text"
                vpgrid:
                    cols 3
                    spacing 10
                    xsize 1340
                    ysize 720
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
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
                            action [SetVariable("dev_chapter_target", key), Start("dev_chapter_start")]
                    null width 430 height 55

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
