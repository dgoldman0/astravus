# Derive this guide from the current reading, including saves made before 0.2.2.
# The current spoken line is already in Ren'Py's rollback-aware history.
init python:
    PEOPLE_PROFILES = {
        "Cali": "A curious child who sees the world through color and drawing. Her older self is remembering these scenes. Her five parents are partners in a constellation; their family includes the children they raise together.",
        "Maia": "One of Cali's five parents. She tends living ecosystems and helps Cali discover the garden through patient, practical care.",
        "Kael": "Cali's older brother. Eager to explore and usually ready with a plan, he shares her childhood adventures and looks after their younger sister, Lyra.",
        "Arin": "One of Cali's five parents. They design biomechanical interfaces and welcome Cali into their workshop, making room for mistakes as well as discoveries.",
        "Selene": "One of Cali's five parents. She works with sound and teaches Cali to listen, breathe, and find her way through music.",
        "Dorian": "One of Cali's five parents. He keeps oral histories and brings distant journeys to life through stories and maps.",
        "Lyra": "Cali's younger sister. Full of questions and quick to speak her mind, she wants a place in the games and discoveries around her.",
        "Sage": "One of Cali's five parents. They help people through transitions and give the children stories, patient attention, and a place to be heard.",
        "Cassia": "Cali's friend: a storyteller who always has room for one more idea.",
        "Thalia": "Cassia's mother. She helps people resolve disagreements by listening carefully and giving them time to find common ground.",
        "Lyron": "Cassia's father. He tends agricultural systems and shows the children how water connects gardens and the people who care for them.",
        "Joren": "Cali's friend: an eager explorer with an infectious laugh.",
        "Soren": "Joren's mother, a systems designer whose workshop is full of tools, plans, and unfinished inventions.",
        "Kaleb": "Joren's father, an explorer who shares his discoveries and the stories of his journeys.",
    }
    # Completed scenes recover entries even if an older save's history was
    # shortened. Within the current scene, only actual speakers are added.
    PEOPLE_INTRODUCTIONS = (
        ("Maia", "garden"), ("Kael", "plant_disagreement"),
        ("Arin", "workshop_first"), ("Selene", "music_first"),
        ("Dorian", "dorian_stories"), ("Lyra", "dorian_stories"),
        ("Sage", "sage_story"), ("Cassia", "meeting_cassia"),
        ("Thalia", "cassia_home"), ("Lyron", "cassia_home"),
        ("Joren", "meeting_joren"), ("Soren", "joren_home"),
        ("Kaleb", "kaleb_walk"),
    )

    def people_names():
        names = ["Cali"]
        for name, scene in PEOPLE_INTRODUCTIONS:
            if scene in visited_scenes and BOOK_SCENE_LOOKUP[scene][0] < scene_number:
                names.append(name)
        for entry in _history_list:
            if entry.who in PEOPLE_PROFILES and entry.who not in names:
                names.append(entry.who)
        # These existing save fields also cover a curtailed encounter history.
        for name, met in (("Cassia", met_cassia), ("Joren", met_joren)):
            if met and name not in names:
                names.append(name)
        return names

    def people_description(name):
        if name in FAMILIAR_PROFILES:
            return FAMILIAR_PROFILES[name][1]
        if name == "Lumen":
            return people_lumen_description()
        if name == "Joren":
            return people_joren_description()
        if name == "Cassia" and joren_lost:
            return "Cali's closest friend, a storyteller. They are learning how to remember Joren together."
        return PEOPLE_PROFILES[name]

    # Animals never speak, so their encounter comes from narration instead.
    # Read existing history/progress: older saves need no new unlock fields.
    FAMILIAR_INTRODUCTION = "Shadow watched from the sofa. Barkley came to meet us at the door. Nibble's tiny feet tickled when she ran across my hand."
    FAMILIAR_PROFILES = {
        "Shadow": ("Cat", "The family's sleek black cat, with watchful green eyes. She likes a good vantage point on the sofa and quiet company beside Cali. Shadow is one of the household's familiars: animal companions who share the family's daily life."),
        "Barkley": ("Golden retriever", "The family's golden retriever, always ready to greet someone at the door. Gentle and full of energy, he is quick to join the children on an adventure. He and Shadow and Nibble are familiars, part of the family Cali grows up with."),
        "Nibble": ("Rat", "The family's inquisitive little rat, with fluffy black-and-white fur, a tousled white blaze, and one violet eye and one coral eye. Her tiny feet tickle as she explores a hand, and a shoulder makes an excellent lookout. She shares the household with Shadow and Barkley."),
    }

    def familiar_names():
        if "first_memory" in visited_scenes and scene_number > 1:
            return list(FAMILIAR_PROFILES)
        if any(entry.what == FAMILIAR_INTRODUCTION for entry in _history_list):
            return list(FAMILIAR_PROFILES)
        return []
