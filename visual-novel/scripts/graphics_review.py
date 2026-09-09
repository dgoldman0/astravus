"""Inventory graphics and record explicit, hash-bound production reviews.

Syncing an inventory never approves art. The story walker follows this book's
linear labels/calls and uses its actual portrait resolver; it is not Ren'Py.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import textwrap
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "../development/visual-novel/reviews/graphics/ledger.json"
MANIFESTS = ("assets.json", "character-assets.json", "environment-assets.json", "familiar-assets.json")
STORY = ("game/script.rpy", "game/family_book_one.rpy", "game/friendships_book_one.rpy")
DIMENSIONS = {
    "identity": "Recognizable facial construction, hair, skin, iris or familiar coat/eye identity; no luminous pigment substitution.",
    "anatomy_expression": "Coherent eyes/lids/pupils, face planes, mouths, hands and limbs; a natural expression appropriate to the moment.",
    "age_stature": "Correct life stage and relative body stature, judged using posture, perspective and support planes rather than hair crowns alone.",
    "setting_geometry": "Shared room/exterior landmarks, connected access, furniture and props; plausible feet/paws/contact and consistent camera geometry.",
    "lighting_style_detail": "Appealing composition and expressive presence; dimensional midtones, coherent light and preserved painterly texture/detail without cumulative degradation.",
    "scene_truth_action": "Depicted participants, action and props fit source events and the reader's knowledge; no invented metaphysics or contradictory physical actions.",
    "runtime_compositing": "Readable native scene/portrait rendering, clean mattes and edges, preserved internal colors, and no unintended UI occlusion.",
}


def read(name):
    return json.loads((ROOT / name).read_text())


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def edit_provenance(item):
    """Bind active edit metadata without treating its technical receipt as art."""
    result = {"source_generation": item["generation"]}
    if "production_edit" in item:
        pointer = item["production_edit"]
        registry = read(pointer["recipe_file"])
        recipes = [entry for entry in registry["edits"] if entry["id"] == pointer["id"]]
        if len(recipes) != 1:
            raise ValueError("Missing or ambiguous production edit: " + item["file"])
        recipe = recipes[0]
        result.update(production_edit=pointer, current_recipe_sha256=fingerprint(recipe),
            script_file=recipe["script_file"], current_script_sha256=digest(ROOT / recipe["script_file"]),
            immutable_sources=recipe["sources"])
        result["dependency_sha256"] = {entry["file"]: digest(ROOT / entry["file"])
                                       for entry in recipe.get("dependencies", [])}
        result["materials"] = []
        for material in recipe.get("material_provenance", []):
            registry = read(material["registry_file"])
            record = next(entry for entry in registry["materials"] if entry["id"] == material["id"])
            result["materials"].append({**material, "current_record_sha256": fingerprint(record),
                "current_prompt_sha256": digest(ROOT / record["prompt_file"])})
    if "postprocess" in item:
        result["postprocess"] = item["postprocess"]
    return result


def python_block(path):
    text = (ROOT / path).read_text().split("init python:\n", 1)[1]
    return ast.parse(textwrap.dedent(text))


def runtime_uses(assets):
    aliases, definitions, speakers = {}, {}, {}
    for path in sorted((ROOT / "game").glob("*.rpy")):
        for number, line in enumerate(path.read_text().splitlines(), 1):
            found = re.match(r'image (.+?) = .*?["\'](images/[^"\']+)["\']', line)
            if found and "game/" + found[2] in assets:
                aliases[found[1]] = "game/" + found[2]
                definitions[found[1]] = {"file": path.relative_to(ROOT).as_posix(), "line": number}
            found = re.match(r'define (\w+) = Character\("([^\"]+)"', line)
            if found:
                speakers[found[1]] = found[2]

    # Compile only the reviewed resolver and its literal lookup tables. No
    # displayable constructors or other init code execute in this inventory.
    tree = python_block("game/speaker_portraits.rpy")
    selected = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in
                ("SPEAKER_TAGS", "PORTRAIT_VARIANTS", "CG_CAST") for t in node.targets):
            ast.literal_eval(node.value)
            selected.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name == "dialogue_portrait":
            selected.append(node)
    namespace = {}
    exec(compile(ast.Module(body=selected, type_ignores=[]), "portrait inventory", "exec"), namespace)
    visible = {}
    namespace["renpy"] = SimpleNamespace(
        showing=lambda tag: tag in visible,
        get_attributes=lambda tag: tuple(visible[tag].split()[1:]) if tag in visible else (),
    )
    namespace.update(joren_lost=False, childhood_stage="early", scene_key="first_memory")
    lines, labels = {}, {}
    for name in STORY:
        lines[name] = (ROOT / name).read_text().splitlines()
        for index, line in enumerate(lines[name]):
            found = re.match(r"label (\w+):", line)
            if found:
                labels[found[1]] = (name, index + 1)
    uses = {name: {} for name in assets}
    file, index = labels["start"]
    stack, entered = [], []
    steps = 0
    while index < len(lines[file]):
        steps += 1
        if steps > 10000:
            raise ValueError("Story inventory exceeded its bounded linear traversal")
        line = lines[file][index].strip()
        number = index + 1
        index += 1
        if line.startswith("call screen book_afterword"):
            break
        if re.match(r"(if |elif |else:|menu:)", line):
            raise ValueError(f"New story branch requires explicit inventory support: {file}:{number}")
        found = re.match(r"(call|jump) (\w+)\s*$", line)
        if found:
            if found[2] not in labels:
                raise ValueError(f"Unknown story target: {found[2]}")
            if found[1] == "call":
                stack.append((file, index))
            file, index = labels[found[2]]
            continue
        if line == "return":
            if not stack:
                break
            file, index = stack.pop()
            continue
        found = re.match(r'\$ enter_scene\("([^\"]+)"\)', line)
        if found:
            namespace["scene_key"] = found[1]
            entered.append(found[1])
        found = re.match(r"\$ (childhood_stage|joren_lost) = (.+)", line)
        if found:
            namespace[found[1]] = ast.literal_eval(found[2])
        found = re.match(r"(scene|show|hide) (.+)", line)
        if found:
            command, rest = found.groups()
            if command == "scene":
                visible.clear()
            if command == "hide":
                visible.pop(rest.split()[0], None)
            else:
                alias = next((a for a in sorted(aliases, key=len, reverse=True)
                              if rest == a or rest.startswith(a + " ")), None)
                if alias:
                    visible[alias.split()[0]] = alias
        dialogue = re.match(r'(\w+) "', line)
        if not dialogue:
            continue
        active = [(alias, "staged") for alias in visible.values()]
        who = speakers.get(dialogue[1])
        portrait = namespace["dialogue_portrait"](who) if who else None
        if portrait:
            active.append((portrait, "speaker_portrait"))
        for alias, mode in active:
            if alias not in aliases:
                raise ValueError(f"Unknown portrait/image alias: {alias}")
            name = aliases[alias]
            key = (namespace["scene_key"], mode, alias)
            uses[name].setdefault(key, {"scene": namespace["scene_key"], "mode": mode,
                "image_alias": alias, "script": file, "first_dialogue_line": number,
                "childhood_stage_state": namespace["childhood_stage"]})
    expected = [s["key"] for s in read("docs/release-matrix.json")["scenes"]]
    if entered != expected:
        raise ValueError(f"Story traversal no longer matches all 32 scene entries: {entered}")
    for name in uses:
        uses[name] = list(uses[name].values())
    ui = {name: [] for name in assets}
    current_screen = None
    for number, line in enumerate((ROOT / "game/screens.rpy").read_text().splitlines(), 1):
        found = re.match(r"screen (\w+)", line)
        if found:
            current_screen = found[1]
        found = re.search(r'add "([^\"]+)"', line)
        if found and found[1] in aliases:
            ui[aliases[found[1]]].append({"screen": current_screen, "file": "game/screens.rpy", "line": number})
    for name in assets:
        if name.startswith("game/images/familiars/"):
            ui[name].append({"screen": "people", "file": "game/screens.rpy", "resolver": "person.lower() / familiar_portrait"})
    return aliases, definitions, uses, ui


def inventory():
    assets = {}
    for manifest in MANIFESTS:
        for item in read("docs/" + manifest)["assets"]:
            if item["file"] in assets:
                raise ValueError("Duplicate selected image: " + item["file"])
            assets[item["file"]] = dict(item, manifest="docs/" + manifest)
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / "game/images").rglob("*") if p.is_file()}
    if set(assets) != actual:
        raise ValueError(f"Selected/runtime image inventory differs: {set(assets) ^ actual}")
    aliases, definitions, uses, ui = runtime_uses(assets)
    cg_data = read("docs/cg-character-review.json")
    cg = {a["file"]: a for a in cg_data["assets"]}
    characters = {a["id"]: a for a in cg_data["characters"]}
    location_data = read("docs/location-continuity.json")
    locations = {a["id"]: a for a in location_data["locations"]}
    located = {a["file"]: a for a in location_data["assets"]}
    layout = read("game/character_layout.json")
    theme = read("game/closing_theme.json")
    output = {}
    common = ["docs/ART_DIRECTION.md", "docs/CHARACTER_CONTINUITY.md", "../revision/latest.md"]
    for name, item in assets.items():
        refs = set(common)
        contracts = {}
        cast = cg.get(name, {}).get("cast", [])
        sprite = layout["actors"].get(name.removeprefix("game/"))
        if sprite:
            contracts["sprite_layout"] = dict(sprite, target_height=layout["heights"][sprite["group"]], foot_y=layout["foot_y"])
            actor = Path(name).stem.split("-")[0].capitalize()
            cast = [{"character": actor, "stage": sprite["group"], "reference_kind": "sprite layout group"}]
        for actor in cast:
            character = characters.get(actor["character"])
            if not character:
                continue
            refs.add(character["wiki"])
            contracts.setdefault("characters", {})[character["id"]] = {"specs": character["specs"], "stage": actor["stage"]}
            if actor["stage"] in character["stage_references"]:
                refs.update(character["stage_references"][actor["stage"]])
            else:
                refs.update(r for stage in character["stage_references"].values() for r in stage)
        if name in cg:
            refs.update(cg[name].get("face_review", {}).get("reference_files", []))
        location = located.get(name)
        if location:
            details = locations[location["location_id"]]
            contracts["location"] = {"id": location["location_id"], "view": location["view_id"],
                "required_invariants": [i for i in details["invariants"] if i["id"] in location["required_invariants"]]}
            refs.update(r["file"] for r in details["canonical_references"] + details["source_facts"])
        if name.startswith("game/images/familiars/"):
            refs.update(["game/familiars.rpy", "game/people.rpy", "../wiki/worldbuilding/Familiars.md"])
        refs.update(u["script"] for u in uses[name])
        refs.update(["game/visuals.rpy", "game/characters_book_one.rpy", "game/speaker_portraits.rpy"])
        shots = [{"index": index, "at": shot["at"], "label": shot["label"], "cast": shot.get("cast", [])}
                 for index, shot in enumerate(theme["shots"]) if "game/" + shot["image"] == name]
        if shots:
            refs.update(["game/closing_theme.json", "game/closing_theme.rpy"])
        ref_hashes = {p: digest(ROOT / p) for p in sorted(refs) if p != name}
        output[name] = {
            "file": name, "kind": name.split("/")[2], "manifest": item["manifest"],
            "manifest_sha256": item["sha256"], "current_sha256": digest(ROOT / name),
            "size": item["size"], "mode": item["mode"],
            "definitions": [dict(image_alias=a, **definitions[a]) for a in aliases if aliases[a] == name],
            "story_uses": uses[name], "theme_uses": shots, "ui_uses": ui[name], "cast": cast,
            "contract_references": contracts, "reference_sha256": ref_hashes,
            "edit_provenance": edit_provenance(item),
        }
        output[name]["context_signature"] = fingerprint({k: output[name][k] for k in
            ("story_uses", "theme_uses", "ui_uses", "cast", "contract_references", "reference_sha256", "edit_provenance")})
        if not (uses[name] or shots or ui[name]):
            raise ValueError("Selected image has no identified runtime use: " + name)
    return output


def save(data):
    LEDGER.write_text(json.dumps(data, indent=2) + "\n")


def review_context_signature(item, dimension):
    if dimension == "runtime_compositing":
        return item["context_signature"]
    # A shader/player implementation change requires a new runtime inspection,
    # but does not invalidate a source painting's already inspected face/room.
    # Actual use, dialogue/source, cast, references and edit provenance stay bound.
    rendering = {"game/visuals.rpy", "game/characters_book_one.rpy",
                 "game/speaker_portraits.rpy", "game/closing_theme.rpy",
                 "game/closing_theme.json", "game/screens.rpy"}
    context = {key: item[key] for key in
        ("story_uses", "theme_uses", "ui_uses", "cast", "contract_references", "edit_provenance")}
    context["reference_sha256"] = {name: sha for name, sha in item["reference_sha256"].items()
                                    if name not in rendering}
    return fingerprint(context)


def sync():
    live = inventory()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    tree = subprocess.check_output(["git", "ls-tree", "-r", commit, "--", "visual-novel/game/images"], cwd=ROOT.parent, text=True)
    blobs = {line.split("\t", 1)[1].removeprefix("visual-novel/"): line.split()[2] for line in tree.splitlines()}
    data = read("../development/visual-novel/reviews/graphics/ledger.json") if LEDGER.exists() else {
        "schema_version": 1, "scope": "All selected runtime images; graphics production polish",
        "authority": ["Author direction and manuscript/wiki facts", "Existing character, stature and location contracts", "Deliberately selected visual comparison references"],
        "policy": ["Every artistic dimension begins pending. Prior matrix/registry acceptance is not renewed approval.",
            "A hash proves which bytes were reviewed, not their quality. Sync and manifest refresh cannot pass art.",
            "Changed images, relevant references or evidence invalidate accepted reviews.",
            "Reject cumulative losses in face anatomy, composition, illumination and painterly detail even when individual color/geometry checks pass."],
        "usage_method": "Static linear story traversal through all 32 enter_scene calls, using the actual dialogue_portrait function plus staged-image state; theme JSON and UI declarations are separate uses. This is an inventory, not a live Ren'Py capture.",
        "dimensions": DIMENSIONS, "assets": [],
    }
    existing = {a["file"]: a for a in data["assets"]}
    data["assets"] = []
    for name, item in sorted(live.items()):
        old = existing.get(name, {})
        item["baseline_sha256"] = old.get("baseline_sha256", item["manifest_sha256"])
        item["baseline_git_commit"] = old.get("baseline_git_commit", commit)
        item["baseline_git_blob"] = old.get("baseline_git_blob", blobs.get(name))
        item["comparison_reference"] = old.get("comparison_reference")
        if "editorial_role" in old:
            item["editorial_role"] = old["editorial_role"]
        if "runtime_coverage" in old:
            item["runtime_coverage"] = old["runtime_coverage"]
        item["reviews"] = old.get("reviews", {key: {"outcome": "pending"} for key in DIMENSIONS})
        item["findings"] = old.get("findings", [])
        data["assets"].append(item)
    data["synced_at_utc"] = datetime.now(timezone.utc).isoformat()
    data["selected_count"] = len(live)
    archive = ROOT / "../development/visual-novel/archive/local/design-proof/ARCHIVE.json"
    if archive.is_file():
        data["archive"] = json.loads(archive.read_text())
    else:
        data["archive"] = {"available": False,
            "note": "Optional ignored design experiments are absent from this checkout; selected production inputs are checked separately.",
            "recovery_record": "../development/visual-novel/archive/recovered-proof.json"}
    save(data)
    print(f"Synced {len(live)} images; no artistic outcomes changed.")


def review_status(item, live):
    if set(item["reviews"]) != set(DIMENSIONS):
        raise ValueError("Missing or unknown review dimensions: " + item["file"])
    counts = Counter()
    for dimension, review in item["reviews"].items():
        outcome = review["outcome"]
        if outcome not in ("pending", "partial", "accepted", "needs_rework", "not_applicable"):
            raise ValueError("Unknown artistic outcome: " + outcome)
        if outcome != "pending":
            unchanged = review.get("image_sha256") == live["current_sha256"] and review.get("context_signature") == review_context_signature(live, dimension)
            unchanged = unchanged and all(review.get(k) for k in ("reviewer", "notes", "comparison_reference", "evidence_sha256"))
            unchanged = unchanged and all((ROOT / p).is_file() and digest(ROOT / p) == sha for p, sha in review.get("evidence_sha256", {}).items())
            if not unchanged:
                outcome = "stale"
        counts[outcome] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("sync", help="Refresh inventory/usages while preserving pending or recorded reviews")
    status = commands.add_parser("status")
    status.add_argument("--strict", action="store_true")
    record = commands.add_parser("record", help="Record one actual reviewer finding; never infers an artistic result")
    record.add_argument("file")
    record.add_argument("--dimension", choices=DIMENSIONS, required=True)
    record.add_argument("--outcome", choices=("partial", "accepted", "needs_rework", "not_applicable"), required=True)
    record.add_argument("--reviewer", required=True)
    record.add_argument("--notes", required=True)
    record.add_argument("--evidence", action="append", required=True)
    record.add_argument("--comparison-reference", required=True, help="Deliberately chosen Git blob/reference; not automatically the newest image")
    args = parser.parse_args()
    if args.command == "sync":
        sync()
        return 0
    data, live = read("../development/visual-novel/reviews/graphics/ledger.json"), inventory()
    if {a["file"] for a in data["assets"]} != set(live):
        parser.error("Selected image set changed; run sync first")
    if args.command == "record":
        item = next((a for a in data["assets"] if a["file"] == args.file), None)
        if item is None:
            parser.error("Unknown selected image")
        evidence = {}
        for name in args.evidence:
            path = (ROOT / name).resolve()
            if not path.is_relative_to(ROOT.parent) or not path.is_file():
                parser.error("Evidence must be a real repository file: " + name)
            evidence[name] = digest(path)
        item["comparison_reference"] = args.comparison_reference
        item.update(live[args.file])
        item["reviews"][args.dimension] = {"outcome": args.outcome, "reviewer": args.reviewer,
            "notes": args.notes, "reviewed_at_utc": datetime.now(timezone.utc).isoformat(),
            "image_sha256": live[args.file]["current_sha256"], "context_signature": review_context_signature(live[args.file], args.dimension),
            "comparison_reference": args.comparison_reference, "evidence_sha256": evidence}
        if digest(ROOT / args.file) != live[args.file]["current_sha256"]:
            parser.error("Image changed during recording; review the new bytes before recording")
        save(data)
        print(f"Recorded {args.outcome}: {args.file} / {args.dimension}")
        return 0
    counts = Counter()
    changed = []
    for item in data["assets"]:
        counts.update(review_status(item, live[item["file"]]))
        if live[item["file"]]["current_sha256"] != live[item["file"]]["manifest_sha256"]:
            changed.append(item["file"])
    print(json.dumps({"images": len(live), "dimension_reviews": dict(counts), "manifest_hash_mismatches": changed}, indent=2))
    return int(args.strict and (bool(changed) or any(counts[k] for k in ("pending", "partial", "needs_rework", "stale"))))


if __name__ == "__main__":
    raise SystemExit(main())
