"""Reading-local glossary selection, shared by Ren'Py and the regression checks."""


def revealed_glossary(entries, scene_keys, current_scene, visited, history_text):
    """Return only definitions introduced at or before this reading position.

    A chapter jump reconstructs completed earlier scenes, as People does. The
    destination scene must still display its own cues. History is rollback/save
    state; neither persistent completion nor global seen-dialogue data is used.
    """
    position = scene_keys.index(current_scene)
    earlier = set(scene_keys[:position]).intersection(visited)
    displayed = set(history_text)
    revealed = {}
    for entry in entries:
        for level, stage in enumerate(entry["stages"]):
            stage_position = scene_keys.index(stage["scene"])
            if stage["scene"] in earlier or (
                stage_position <= position and stage["cue"] in displayed
            ):
                revealed[entry["id"]] = {
                    "title": entry["title"],
                    "description": stage["description"],
                    "level": level,
                }
    return dict(sorted(revealed.items(), key=lambda item: item[1]["title"].casefold()))
