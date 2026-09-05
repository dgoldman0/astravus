# Story progress belongs to the current reading/save, not global completion.
default scene_key = "first_memory"
default scene_title = "First memory"
default scene_number = 1
default visited_scenes = []
default pending_scene_save = None
default lumen_known = False
default joren_lost = False
default childhood_stage = "early"
default persistent.book_one_complete = False

init -5 python:
    BOOK_SAVE_ID = "astravus-book-one-v1"
    BOOK_SCENES = (
        ("first_memory", "First memory"),
        ("garden", "A small beginning"),
        ("plant_disagreement", "Room for both"),
        ("workshop_first", "The scattered pieces"),
        ("music_first", "A color you can hear"),
        ("dorian_stories", "Routes through a story"),
        ("sage_story", "Three ways forward"),
        ("family_rhythm", "The days between"),
        ("tree_echoes", "The Tree of Echoes"),
        ("pond_scare", "The shallow water"),
        ("soup_experiment", "A little too much"),
        ("festival_lights", "Wishes in the light"),
        ("meeting_cassia", "An invitation"),
        ("cassia_home", "Room for another story"),
        ("meeting_joren", "Something worth finding"),
        ("joren_home", "Things we could make"),
        ("kaleb_walk", "Beyond the familiar paths"),
        ("treehouse", "Our place in the branches"),
        ("rain_refuge", "A story under the rain"),
        ("waterwheel", "Something that turns"),
        ("outer_exploration", "The unfinished world"),
        ("lyra_included", "A place beside us"),
        ("dome_ascent", "The view from above"),
        ("treehouse_dispute", "Which way we go"),
        ("loss", "The news"),
        ("family_grief", "What comfort can do"),
        ("painting_grief", "What the hand remembers"),
        ("cassia_grief", "Between the two of us"),
        ("community_memorial", "The names we carry"),
        ("mural_remembrance", "A place to remember"),
        ("treehouse_remembrance", "The rain returns"),
        ("annual_remembrance", "What remains"),
    )
    BOOK_SCENE_KEYS = tuple(key for key, title in BOOK_SCENES)
    BOOK_SCENE_COUNT = len(BOOK_SCENES)
    BOOK_SCENE_LOOKUP = {key: (number, title) for number, (key, title) in enumerate(BOOK_SCENES, 1)}

    def enter_scene(key):
        number, title = BOOK_SCENE_LOOKUP[key]
        renpy.store.scene_key = key
        renpy.store.scene_number = number
        renpy.store.scene_title = title
        if key not in renpy.store.visited_scenes:
            renpy.store.visited_scenes.append(key)
        # Save from the first displayed dialogue, after background/actor changes.
        renpy.store.pending_scene_save = key

    def save_scene_checkpoint():
        if renpy.store.pending_scene_save != renpy.store.scene_key:
            return
        if renpy.store.main_menu or renpy.context()._menu or not renpy.get_screen("say"):
            return
        renpy.store.pending_scene_save = None
        renpy.force_autosave(take_screenshot=True, block=True)

    def book_save_metadata(data):
        data["book_id"] = BOOK_SAVE_ID
        data["scene_key"] = renpy.store.scene_key
        data["scene_title"] = renpy.store.scene_title

    config.save_json_callbacks.append(book_save_metadata)

    def compatible_book_save(slot):
        metadata = renpy.slot_json(slot) or {}
        return metadata.get("book_id") == BOOK_SAVE_ID

    def people_lumen_description():
        if renpy.store.lumen_known:
            return "Cali's home: a young, living Astravus, the child of Aurora and Nyx. Its gardens and gathering places bring its residents together."
        return "Cali's home: gardens, gathering places, and paths she is still learning to follow. Her family is one of the many households in its community."

    def people_joren_description():
        if renpy.store.joren_lost:
            return "Cali and Cassia remember their friend through the adventures they shared. His death during a research expedition has left an absence in their families and community."
        return "Cali's friend: an eager explorer with an infectious laugh."
