#!/usr/bin/env python3
"""Validate each glossary reveal against the current script and source passages."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import re

PROJECT = Path(__file__).resolve().parents[1]
STORY_FILES = ("script.rpy", "family_book_one.rpy", "friendships_book_one.rpy")


def story_cues(project=PROJECT):
    cues = {}
    for name in STORY_FILES:
        scene = None
        for line in (project / "game" / name).read_text().splitlines():
            entered = re.search(r'enter_scene\("([a-z_]+)"\)', line)
            if entered:
                scene = entered[1]
            spoken = re.match(r'^\s+\w+ ("(?:[^"\\]|\\.)*")(?: id \w+)?$', line)
            if spoken and scene:
                text = ast.literal_eval(spoken[1])
                cues.setdefault(text, []).append(scene)
    return cues


def validate_glossary(project=PROJECT):
    data = json.loads((project / "game/glossary.json").read_text())
    assert data["schema_version"] == 1, "Unknown glossary schema"
    entries = data["entries"]
    assert entries and len({entry["id"] for entry in entries}) == len(entries), "Duplicate glossary IDs"
    cues = story_cues(project)
    count = 0
    for entry in entries:
        assert entry["title"] and entry["stages"], f"Incomplete glossary entry: {entry['id']}"
        for stage in entry["stages"]:
            count += 1
            assert cues.get(stage["cue"]) == [stage["scene"]], f"Missing, moved or repeated glossary cue: {entry['id']}"
            assert stage["description"] and stage["sources"], f"Unsubstantiated glossary entry: {entry['id']}"
            for source in stage["sources"]:
                path = (project / source["path"]).resolve()
                assert path.is_relative_to(project.parent), f"External glossary source: {path}"
                assert path.is_file() and source["anchor"] in path.read_text(), f"Changed glossary source: {entry['id']} / {source['path']}"
    return {"entries": len(entries), "reveal_stages": count, "status": "pass"}


if __name__ == "__main__":
    print(json.dumps(validate_glossary(), indent=2))
