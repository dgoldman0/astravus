#!/usr/bin/env python3
"""Verify selected image files and the complete generation/reference chain."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

PROJECT = Path(__file__).resolve().parents[1]
REPOSITORY = PROJECT.parent
MANIFESTS = ("assets.json", "character-assets.json", "environment-assets.json")


def check():
    assets = {}
    generations = {}
    for name in MANIFESTS:
        data = json.loads((PROJECT / "docs" / name).read_text())
        for item in data["assets"]:
            assert item["file"] not in assets, f"Duplicate asset: {item['file']}"
            assets[item["file"]] = item
        for item in data["generations"]:
            assert item["id"] not in generations, f"Duplicate generation: {item['id']}"
            generations[item["id"]] = item

    source = "\n".join(p.read_text() for p in (PROJECT / "game").glob("*.rpy"))
    selected = set()
    for name, item in assets.items():
        path = PROJECT / name
        assert path.resolve().is_relative_to(PROJECT / "game/images"), name
        assert path.is_file(), f"Missing image: {name}"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"], f"Changed pixels: {name}"
        with Image.open(path) as picture:
            assert list(picture.size) == item["size"], f"Dimensions: {name}"
            assert picture.mode == item["mode"], f"Color mode: {name}"
            picture.verify()
        assert item["generation"] in generations, f"Missing generation: {name}"
        assert name.removeprefix("game/") in source, f"No runtime definition: {name}"
        selected.add(item["generation"])

    image_files = {
        p.relative_to(PROJECT).as_posix()
        for p in (PROJECT / "game/images").rglob("*")
        if p.is_file() and p.suffix.lower() in (".png", ".webp", ".jpg", ".jpeg")
    }
    assert image_files == set(assets), f"Uncatalogued or missing images: {image_files ^ set(assets)}"
    declared_selected = {name for name, item in generations.items() if item["selected"]}
    assert selected == declared_selected, f"Selection mismatch: {selected ^ declared_selected}"

    visited = set()

    def visit(name, chain=()):
        assert name in generations, f"Unknown generation reference: {name}"
        assert name not in chain, f"Cyclic generation references: {chain + (name,)}"
        if name in visited:
            return
        item = generations[name]
        assert item.get("prompt") and item.get("output_id"), f"Incomplete provenance: {name}"
        for reference in item.get("references", []):
            if reference.startswith("generation:"):
                visit(reference.removeprefix("generation:"), chain + (name,))
            else:
                path = REPOSITORY / reference
                assert path.resolve().is_relative_to(REPOSITORY), f"External path: {reference}"
                assert path.is_file(), f"Missing reference: {reference}"
        visited.add(name)

    for name in generations:
        visit(name)
    print(f"Image audit passed: {len(assets)} selected files; {len(generations)} complete generation records.")


if __name__ == "__main__":
    check()
