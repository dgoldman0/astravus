#!/usr/bin/env python3
"""Verify selected images, provenance, and current location continuity reviews."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

PROJECT = Path(__file__).resolve().parents[1]
REPOSITORY = PROJECT.parent
MANIFESTS = ("assets.json", "character-assets.json", "environment-assets.json", "familiar-assets.json")


def location_reference_signature(location):
    references = [reference["file"] + ":" + hashlib.sha256((PROJECT / reference["file"]).read_bytes()).hexdigest()
                  for reference in location["canonical_references"]]
    return hashlib.sha256("\n".join(references).encode()).hexdigest()


def cg_reference_signature(data, item):
    characters = {character["id"]: character for character in data["characters"]}
    references = {data["relative_height_production_contract"]["file"]}
    references.update(item.get("face_review", {}).get("reference_files", []))
    specifications = []
    for actor in item["cast"]:
        character = characters[actor["character"]]
        references.add(character["wiki"])
        references.update(character["stage_references"][actor["stage"]])
        specifications.append({"character": actor["character"], "stage": actor["stage"], "specs": character["specs"]})
    parts = [json.dumps(specifications, sort_keys=True)]
    parts += [name + ":" + hashlib.sha256((PROJECT / name).read_bytes()).hexdigest() for name in sorted(references)]
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()


def check_cg_characters(assets):
    data = json.loads((PROJECT / "docs/cg-character-review.json").read_text())
    assert data["schema_version"] == 1, "Unsupported CG character-review schema"
    characters = {item["id"]: item for item in data["characters"]}
    assert len(characters) == len(data["characters"]), "Duplicate CG character ID"
    issues = {item["id"]: item for item in data["issues"]}
    assert len(issues) == len(data["issues"]), "Duplicate CG character issue ID"
    contract = (PROJECT / data["relative_height_production_contract"]["file"]).resolve()
    assert contract.is_relative_to(PROJECT) and contract.is_file(), "Missing shared character stature contract"
    for character in characters.values():
        wiki = (PROJECT / character["wiki"]).resolve()
        assert wiki.is_relative_to(REPOSITORY) and wiki.is_file(), f"Missing CG identity source: {character['id']}"
        for anchor in character["wiki_anchors"]:
            assert anchor in wiki.read_text(), f"Changed character source needs CG review: {character['id']} / {anchor}"
        for references in character["stage_references"].values():
            assert all(name in assets for name in references), f"Unknown CG identity reference: {character['id']}"
    reviewed = {}
    errors = []
    for item in data["assets"]:
        name = item["file"]
        assert name not in reviewed, f"Duplicate CG review: {name}"
        reviewed[name] = item
        assert name in assets and name.startswith("game/images/cg/"), f"Unknown CG review image: {name}"
        assert item["cast"], f"CG review needs an explicit cast: {name}"
        for actor in item["cast"]:
            assert actor["character"] in characters, f"Unknown CG cast member: {name}"
            assert actor["stage"] in characters[actor["character"]]["stage_references"], f"Unknown CG character stage: {name}"
        if item["reviewed_sha256"] != assets[name]["sha256"]:
            errors.append(f"Changed CG needs character scale/identity review: {name}")
        if item["reviewed_reference_signature"] != cg_reference_signature(data, item):
            errors.append(f"Changed character reference or stature contract needs CG review: {name}")
        if item["review_status"] not in data["review_policy"]["passing_statuses"]:
            errors.append(f"CG character review is {item['review_status']}: {name}")
        face = item.get("face_review", {})
        assert all(reference in assets for reference in face.get("reference_files", [])), f"Unknown CG facial reference: {name}"
        required_face_checks = {"facial_anatomy", "iris_pigment_and_light", "stage_identity", "reference_comparison"}
        if (face.get("status") != "accepted" or not face.get("method") or not face.get("notes")
                or not required_face_checks <= set(face.get("checks", []))):
            errors.append(f"CG needs an explicit face/iris review independent of stature: {name}")
        for issue_id in item["findings"]:
            assert issue_id in issues and issues[issue_id]["file"] == name, f"Unknown CG character finding: {name} / {issue_id}"
            if issues[issue_id]["status"] != "resolved":
                errors.append(f"Open CG character issue {issue_id}: {name}")
    expected = {name for name in assets if name.startswith("game/images/cg/")}
    assert set(reviewed) == expected, f"Unreviewed or missing CGs: {set(reviewed) ^ expected}"
    for issue in issues.values():
        assert issue["file"] in reviewed, f"Orphan CG character issue: {issue['id']}"
        if issue["status"] == "resolved":
            assert issue.get("resolution"), f"Missing CG figure repair record: {issue['id']}"
        elif issue["id"] not in reviewed[issue["file"]]["findings"]:
            errors.append(f"Open CG character issue omitted from image review: {issue['id']}")
    assert not errors, "CG character review incomplete:\n" + "\n".join(errors)
    print(f"CG character review passed: {len(reviewed)} images with current cast/stage/reference reviews.")


def check_location_continuity(assets):
    data = json.loads((PROJECT / "docs/location-continuity.json").read_text())
    assert data["schema_version"] == 1, "Unsupported location-continuity schema"
    locations = {item["id"]: item for item in data["locations"]}
    assert len(locations) == len(data["locations"]), "Duplicate location ID"
    issues = {item["id"]: item for item in data["issues"]}
    assert len(issues) == len(data["issues"]), "Duplicate location issue ID"
    registered = {}
    reference_signatures = {}
    errors = []
    theme = json.loads((PROJECT / "game/closing_theme.json").read_text())["shots"]
    for location in locations.values():
        for reference in location["canonical_references"] + location["source_facts"]:
            path = (PROJECT / reference["file"]).resolve()
            assert path.is_relative_to(REPOSITORY), f"External location reference: {path}"
            assert path.is_file(), f"Missing location reference: {path}"
            if reference.get("anchor"):
                assert reference["anchor"] in path.read_text(), f"Changed source passage needs location review: {path} / {reference['anchor']}"
        landmarks = [item["id"] for item in location["invariants"]]
        assert len(landmarks) == len(set(landmarks)), f"Duplicate landmark in {location['id']}"
        reference_signatures[location["id"]] = location_reference_signature(location)
    for item in data["assets"]:
        name = item["file"]
        assert name not in registered, f"Duplicate location asset: {name}"
        registered[name] = item
        assert name in assets, f"Unknown location asset: {name}"
        assert item["location_id"] in locations, f"Unknown location: {name}"
        location = locations[item["location_id"]]
        assert item["view_id"] in {view["id"] for view in location["views"]}, f"Unknown view: {name}"
        landmarks = {entry["id"] for entry in location["invariants"]}
        assert item["required_invariants"] and set(item["required_invariants"]) <= landmarks, f"Unknown or missing landmarks: {name}"
        actual_theme_starts = [shot["at"] for shot in theme if "game/" + shot["image"] == name]
        assert item["closing_theme_starts"] == actual_theme_starts, f"Changed theme use needs location review: {name}"
        if item["reviewed_sha256"] != assets[name]["sha256"]:
            errors.append(f"Changed image needs visual location review: {name}")
        if item["reviewed_reference_signature"] != reference_signatures[item["location_id"]]:
            errors.append(f"Location reference changed; dependent image needs visual review: {name}")
        if item["review_status"] not in data["review_policy"]["passing_statuses"]:
            errors.append(f"Location review is {item['review_status']}: {name}")
        for issue_id in item["findings"]:
            assert issue_id in issues and issues[issue_id]["file"] == name, f"Unknown location finding: {name} / {issue_id}"
            if issues[issue_id]["status"] != "resolved":
                errors.append(f"Open location issue {issue_id}: {name}")
    for pattern in data["tracked_asset_patterns"]:
        for path in PROJECT.glob(pattern):
            assert path.relative_to(PROJECT).as_posix() in registered, f"Unreviewed recurring-location image: {path}"
    for issue in issues.values():
        assert issue["file"] in registered, f"Orphan location issue: {issue['id']}"
        if issue["status"] == "resolved":
            assert issue.get("resolution"), f"Missing visual repair record: {issue['id']}"
        if issue["status"] != "resolved" and issue["id"] not in registered[issue["file"]]["findings"]:
            errors.append(f"Open location issue omitted from its image review: {issue['id']}")
    assert not errors, "Location continuity review incomplete:\n" + "\n".join(errors)
    print(f"Location continuity passed: {len(registered)} reviewed images across {len(locations)} locations.")


def check():
    assets = {}
    generations = {}
    retouch_file = PROJECT / "docs/iris-retouches.json"
    retouches = {r["id"]: r for r in json.loads(retouch_file.read_text())["retouches"]} if retouch_file.exists() else {}
    selected_retouches = set()
    for name in MANIFESTS:
        data = json.loads((PROJECT / "docs" / name).read_text())
        for item in data["assets"]:
            assert item["file"] not in assets, f"Duplicate asset: {item['file']}"
            assets[item["file"]] = item
        for item in data["generations"]:
            assert item["id"] not in generations, f"Duplicate generation: {item['id']}"
            generations[item["id"]] = item

    source = "\n".join(p.read_text() for p in (PROJECT / "game").glob("*.rpy"))
    theme_images = {shot["image"] for shot in
                    json.loads((PROJECT / "game/closing_theme.json").read_text())["shots"]}
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
        if "postprocess" in item:
            post = item["postprocess"]
            assert post["recipe_file"] == "docs/iris-retouches.json", f"Unknown retouch register: {name}"
            recipe = retouches[post["id"]]
            signature = hashlib.sha256(json.dumps(recipe, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            assert signature == post["recipe_sha256"], f"Retouch recipe changed: {name}"
            assert recipe["file"] == name and recipe["output_sha256"] == item["sha256"], f"Retouch output mismatch: {name}"
            assert recipe["source_generation"] == item["generation"], f"Retouch source generation mismatch: {name}"
            assert len(recipe["source_sha256"]) == 64 and recipe["mask_geometry"], f"Incomplete retouch source/mask: {name}"
            script = PROJECT / recipe["script_file"]
            assert script.resolve().is_relative_to(PROJECT / "scripts"), f"External retouch script: {name}"
            assert hashlib.sha256(script.read_bytes()).hexdigest() == recipe["script_sha256"], f"Retouch implementation changed: {name}"
            proof = recipe["verification"]
            assert 0 < proof["changed_pixels"] < item["size"][0] * item["size"][1] * .01, f"Retouch not local: {name}"
            assert proof["outside_mask_pixels_changed"] == 0 and proof["protected_pupil_and_highlight_pixels_changed"] == 0, f"Retouch changed protected pixels: {name}"
            assert proof["outside_mask_identical"] and proof["canvas_and_mode_unchanged"], f"Retouch verification incomplete: {name}"
            selected_retouches.add(post["id"])
        runtime_name = name.removeprefix("game/")
        assert runtime_name in source or runtime_name in theme_images, f"No runtime definition: {name}"
        selected.add(item["generation"])

    image_files = {
        p.relative_to(PROJECT).as_posix()
        for p in (PROJECT / "game/images").rglob("*")
        if p.is_file() and p.suffix.lower() in (".png", ".webp", ".jpg", ".jpeg")
    }
    assert image_files == set(assets), f"Uncatalogued or missing images: {image_files ^ set(assets)}"
    assert selected_retouches == set(retouches), "Unselected or missing iris retouch records"
    assert theme_images <= {name.removeprefix("game/") for name in assets}, "Uncatalogued theme image"
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
    check_location_continuity(assets)
    check_cg_characters(assets)
    from character_layout import check as check_character_layout
    check_character_layout()
    print(f"Image audit passed: {len(assets)} selected files; {len(generations)} complete generation records.")


if __name__ == "__main__":
    check()
