# A close-up identifies a speaker when the scene's standing pose is hidden.
# It is UI, not a claim that somebody is standing while climbing or embracing.
# Resolve from current story state so loading and rollback restore the right age.
init python:
    SPEAKER_TAGS = {
        "Cali": "calista", "Cassia": "cassia", "Joren": "joren",
        "Maia": "maia", "Arin": "arin", "Selene": "selene",
        "Dorian": "dorian", "Sage": "sage", "Kael": "kael", "Lyra": "lyra",
        "Thalia": "thalia", "Lyron": "lyron", "Soren": "soren", "Kaleb": "kaleb",
    }
    # A scene illustration replaces portraits only for people actually in it.
    # Other speakers (for example Lyra during flute practice) retain a portrait.
    CG_CAST = {
        "first_memory": (),
        "garden_compromise": ("Cali", "Kael", "Maia"),
        "flute_playing": ("Cali", "Selene"),
        "flute_rest": ("Cali", "Selene"),
        "pond_rescue": ("Cali", "Kael", "Lyra"),
        "pond_comfort": ("Cali", "Kael", "Lyra"),
        "cassia_storytelling": ("Cali", "Cassia"),
        "family_embrace": ("Cali", "Maia"),
        "cassia_comfort": ("Cali", "Cassia"),
    }
    PORTRAIT_VARIANTS = {
        "calista": ("young", "home", "festival", "festive", "older", "frustrated", "mourning", "painting"),
        "cassia": ("young", "older", "mourning"),
        "joren": ("young", "older", "frustrated"),
        "maia": ("home",), "arin": ("everyday",), "selene": ("everyday",),
        "dorian": ("everyday",), "sage": ("everyday",),
        "kael": ("young",), "lyra": ("young",),
        "thalia": ("everyday",), "lyron": ("everyday",),
        "soren": ("everyday",), "kaleb": ("everyday",),
    }
    SPEAKER_PORTRAITS = {}
    for actor, variants in PORTRAIT_VARIANTS.items():
        for variant in variants:
            # Crop the source before scaling; reuse the same chroma key as the
            # full actor. Hands, props, and lower-body poses stay out of frame.
            portrait = Transform(
                "images/characters/book-one/{}-{}.png".format(actor, variant),
                crop=(285, 0, 450, 450), xysize=(178, 178), fit="fill",
                mesh=True, shader="astravus.chroma_green")
            SPEAKER_PORTRAITS[actor + " " + variant] = portrait

    def dialogue_portrait(who):
        actor = SPEAKER_TAGS.get(who)
        if actor is None or renpy.showing(actor):
            return None
        cg = renpy.get_attributes("cg") or ()
        if cg and who in CG_CAST.get(cg[0], ()):
            return None
        if actor == "joren" and joren_lost:
            return None
        if actor == "calista":
            if joren_lost:
                variant = "painting" if scene_key in ("painting_grief", "mural_remembrance") else "mourning"
            elif childhood_stage == "later":
                variant = "frustrated" if scene_key == "treehouse_dispute" else "older"
            elif scene_key == "festival_lights":
                # The lantern pose belongs only to the moment she holds one.
                variant = "festive"
            elif scene_key in ("garden", "meeting_cassia", "meeting_joren", "treehouse", "rain_refuge"):
                variant = "young"
            else:
                variant = "home"
        elif actor in ("cassia", "joren"):
            variant = "mourning" if joren_lost else ("older" if childhood_stage == "later" else "young")
        else:
            variant = PORTRAIT_VARIANTS[actor][0]
        return actor + " " + variant
