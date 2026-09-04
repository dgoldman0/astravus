# Astravus: Seeds of Youth — the complete first book, told as a kinetic novel.
init -10 python:
    gui.init(1920, 1080)

    # Menus and dialogue use actual text so self-voicing can read them.
    renpy.music.register_channel("ambience", mixer="sfx", loop=True)

    def remember_scene(key):
        if key not in persistent.seen_scenes:
            persistent.seen_scenes.append(key)
            renpy.save_persistent()

    def latest_reading_slot():
        # A desktop checkout also sees game/saves from the rough prototype.
        # Keep those files, but never Continue into an incompatible old script.
        slots = renpy.list_slots(r"(?:auto-|quick-|[0-9]+-)[0-9]+$")
        current = [slot for slot in slots if compatible_book_save(slot)]
        return max(current, key=lambda slot: renpy.slot_mtime(slot) or 0) if current else None

    def readable_text():
        return 39 if persistent.large_text else 33

    def mood_transition():
        return None if persistent.reduced_motion else Dissolve(0.65)

define config.name = "Astravus — Seeds of Youth"
define config.version = "0.2.0"
define build.name = "astravus-book-one"
define config.save_directory = "Astravus-Book-I"
define config.window_title = "Astravus · Seeds of Youth"
define config.has_sound = True
define config.has_music = True
define config.has_voice = False
define config.main_menu_music = "audio/first_light.ogg"
define config.default_music_volume = 0.32
define config.default_sfx_volume = 0.4
define config.default_text_cps = 38
define config.default_afm_time = 12
define config.history_length = 1200
define config.autosave_slots = 3
define config.autosave_on_quit = True
define config.autosave_on_choice = False
define config.quicksave_slots = 3
define config.enter_transition = Dissolve(0.15)
define config.exit_transition = Dissolve(0.15)
define config.end_game_transition = Fade(0.4, 0.0, 0.5)
define config.game_menu_action = ShowMenu("pause_menu")
define config.thumbnail_width = 384
define config.thumbnail_height = 216
define config.mouse_hide_time = 3.0
define config.gl2 = True
define config.check_conflicting_properties = True

default persistent.large_text = False
default persistent.reduced_motion = False
default persistent.high_contrast = False
default persistent.seen_scenes = []
default persistent.chapter_complete = False
default quick_menu = True
default met_cassia = False
default met_joren = False

init python:
    # Source and selected assets are tracked. Local SDKs and exports are not.
    build.classify("**/.**", None)
    build.classify("**/__pycache__/**", None)
    build.classify("game/cache/**", None)
    build.classify("game/saves/**", None)
    build.classify("game/testcases.rpy*", None)
    build.classify("test-results/**", None)
    build.classify("tests/**", None)
    build.classify("scripts/**", None)
    build.classify("web/**", None)
    build.classify("docs/**", None)
    build.classify("build/**", None)
    build.classify("dist/**", None)
    build.classify("**.pyc", None)
    build.classify("**.sh", None)
    build.classify("game/fonts/LICENSE-*.txt", "all")
    build.classify("**.txt", None)
    build.classify("game/audio/README.md", "all")
    build.documentation("README.md")
