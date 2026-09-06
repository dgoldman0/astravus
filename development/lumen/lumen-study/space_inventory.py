#!/usr/bin/env python3
"""Query the Lumen space register, verify its coverage, or render its reference page.

Standard library only; no server, embeddings, uploads or persistent database.
The curated JSON is the source for both queries and the generated reference page.
Checks detect stale evidence and unmapped scene/art identifiers, not semantic
completeness or plausible geometry. Updating a fingerprint requires re-review.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "space-inventory.json"
PAGE = HERE.parent / "Lumen-Space-Inventory.md"
NARRATIVE = tuple("visual-novel/game/" + p for p in (
    "script.rpy", "family_book_one.rpy", "friendships_book_one.rpy"))
DEFINITIONS = tuple("visual-novel/game/" + p for p in (
    "visuals.rpy", "environments_book_one.rpy"))


def digest(content):
    return hashlib.sha256(content).hexdigest()


def read(root, path):
    return (root / path).read_text(encoding="utf-8")


def line_of(root, src):
    text = read(root, src["path"])
    return text[:text.index(src["anchor"])].count("\n") + 1


def evidence(data):
    for section in ("spaces", "relations"):
        for item in data[section]:
            yield from item["sources"]
    for scene in data["scenes"]:
        yield scene["source"]


def check(data, root=ROOT):
    errors = []
    if data.get("schema_version") != 1:
        return ["Unsupported inventory schema"]
    ids = [s["id"] for s in data["spaces"]]
    known = set(ids)
    if len(known) != len(ids):
        errors.append("Duplicate space identifiers")
    pinned = {s["path"] for s in data["sources"]}
    for pin in data["sources"]:
        try:
            content = read(root, pin["path"])
            if "before" in pin:
                if content.count(pin["before"]) != 1:
                    errors.append(f"Source boundary missing/ambiguous: {pin['path']}")
                content = content.split(pin["before"])[0]
            if digest(content.encode()) != pin["sha256"]:
                errors.append(f"Re-read changed source before refreshing its pin: {pin['path']}")
        except OSError:
            errors.append(f"Missing source: {pin['path']}")
    for src in evidence(data):
        if src["path"] not in pinned:
            errors.append(f"Unpinned evidence source: {src['path']}")
        try:
            if src["anchor"] not in read(root, src["path"]):
                errors.append(f"Missing anchor in {src['path']}: {src['anchor']}")
        except OSError:
            errors.append(f"Missing evidence file: {src['path']}")
    for item in data["spaces"]:
        for field in ("name", "group", "basis", "access", "facts", "placement", "unresolved", "model_status", "sources"):
            if not item.get(field):
                errors.append(f"{item['id']} has no {field}")
        if item["model_status"] not in {"unplaced", "modeled", "not-physical"}:
            errors.append(f"Invalid model status: {item['id']}")

    registry = re.findall(r'^        \("([^"]+)", "([^"]+)"\),',
                          read(root, "visual-novel/game/book_structure.rpy"), re.M)
    if [(s["id"], s["title"]) for s in data["scenes"]] != registry:
        errors.append("Scene coverage/order/titles differ from BOOK_SCENES")
    reached = set()
    used_art = set()
    for path in NARRATIVE:
        text = read(root, path)
        reached.update(re.findall(r'enter_scene\("([^"]+)"\)', text))
        used_art.update(re.findall(r'^\s*(?:scene|show) ((?:bg|cg) \w+)', text, re.M))
    if reached != {s["id"] for s in data["scenes"]}:
        errors.append("Narrative scene calls differ from inventory coverage")
    for scene in data["scenes"]:
        if not scene["spaces"]:
            errors.append(f"Scene has no spatial coverage: {scene['id']}")
        for id in scene["spaces"]:
            if id not in known:
                errors.append(f"Scene {scene['id']} refers to missing space {id}")
    for rel in data["relations"]:
        for field in ("from_id", "to_id"):
            if rel[field] not in known:
                errors.append(f"Connection refers to missing space {rel[field]}")

    definitions = {}
    for path in DEFINITIONS:
        definitions.update((alias, "visual-novel/game/" + image) for alias, image in
            re.findall(r'^image ((?:bg|cg) \w+) = Transform\("([^"]+)"', read(root, path), re.M))
    aliases = {}
    art_paths = set()
    for asset in data["assets"]:
        if asset["path"] in art_paths:
            errors.append(f"Duplicate asset: {asset['path']}")
        art_paths.add(asset["path"])
        for alias in asset["aliases"]:
            if alias in aliases:
                errors.append(f"Duplicate image alias: {alias}")
            aliases[alias] = asset["path"]
        if not asset["spaces"] or not asset.get("observation"):
            errors.append(f"Image has no spatial observation/mapping: {asset['path']}")
        for id in asset["spaces"]:
            if id not in known:
                errors.append(f"Image refers to missing space {id}: {asset['path']}")
        try:
            if digest((root / asset["path"]).read_bytes()) != asset["sha256"]:
                errors.append(f"Reinspect changed image: {asset['path']}")
        except OSError:
            errors.append(f"Missing image: {asset['path']}")
        if asset["review"] != "visually-inspected":
            errors.append(f"Image awaits visual inspection: {asset['path']}")
    if aliases != definitions:
        errors.append("Image definitions changed or include an unregistered background/CG")
    if used_art - aliases.keys():
        errors.append("Unmapped narrative images: " + ", ".join(sorted(used_art - aliases.keys())))
    theme = json.loads(read(root, "visual-novel/game/closing_theme.json"))
    theme_paths = {"visual-novel/game/" + shot["image"] for shot in theme["shots"]}
    if theme_paths - art_paths:
        errors.append("Unmapped closing-theme images: " + ", ".join(sorted(theme_paths - art_paths)))
    return list(dict.fromkeys(errors))


def source_link(src, root=ROOT):
    line = line_of(root, src)
    label = {
        "revision/latest.md": "Book I",
        "visual-novel/game/script.rpy": "VN opening and friendships",
        "visual-novel/game/family_book_one.rpy": "VN family scenes",
        "visual-novel/game/friendships_book_one.rpy": "VN later friendships",
        "visual-novel/docs/LOCATION_CONTINUITY.md": "VN continuity notes",
        "visual-novel/docs/location-continuity.json": "VN continuity register",
    }.get(src["path"], Path(src["path"]).stem)
    return f"[{label}, line {line}](../../{src['path']}#L{line})"


def links(ids, lookup):
    return "; ".join(f"[{lookup[id]['name']}](#{id})" for id in ids)


INTRO = """# Lumen: Book I spaces and connections

**Reference inventory · 6 September 2026**

This reference records the places and practical needs described in Book I and the current visual novel. It links each record to the relevant passages and images, and identifies what the sources leave open. The [Lumen article](../../wiki/worldbuilding/Lumen.md) is the canon overview; the [local connection proposal](Lumen-Local-Connections.md) explores one possible arrangement.

The home includes gathering and cooking, Arin’s workshop, Selene’s music room, Dorian’s library, Sage’s room, each resident’s privacy, art and household support. Its outdoor life includes Maia’s ordinary household garden and the oak’s upper and lower refuges, with shared landscape beyond. Some uses occupy the same room, and some records describe several related places. **The 45 records are not a room count.** All physical spaces still need a measured layout.

## Scope and authority

The audit covers a complete read of Book I in [latest.md](../../revision/latest.md), all three current VN narrative scripts, and inspection of 49 location, scene and closing-theme images. It accounts for all 32 VN scenes and checks them against the scene registry, glossary, Book I coverage notes and production continuity records. Character sprite libraries, marketing, audio and full runtime playback are outside this spatial audit.

Books II–IV still need a full spatial audit. Selected facilities from the supporting wiki are included below, but their presence in a general article does not establish their childhood extent. The Sanctuary’s earlier room suggestions are retained among the [open facility ideas](../ideas/Open-Mechanisms.md#sanctuary-spaces).

Current author direction governs the design. The VN images are the primary visual guides, while both narrative versions establish activities and relationships that must fit. Each record identifies whether it comes from the story, an image, author direction, the supporting wiki or a design inference. Illustrations and inferences do not automatically establish new canon. The incomplete household and neighborhood sketches remain withdrawn; their history is in the [design register](Lumen-Design-Study.md#compatibility-and-adjustment-register).

## Finding a detail

Browse the spaces below or use the local query tool from the repository root:

```sh
python3 development/lumen/lumen-study/space_inventory.py --group Household
python3 development/lumen/lumen-study/space_inventory.py workshop
python3 development/lumen/lumen-study/space_inventory.py --id sage_room
python3 development/lumen/lumen-study/space_inventory.py --check
```

Queries return the recorded details, source passages, images and connections. This is keyword and identifier search; a missing match is a reason to search the original sources too. The checker flags changed evidence and gaps in scene or image coverage. It cannot determine whether every implication was understood or whether a proposed room fits.

The records are maintained in [space-inventory.json](lumen-study/space-inventory.json), and this reference is rendered by [space_inventory.py](lumen-study/space_inventory.py). Generated wording and presentation require editorial review. After changing a source, review the affected records before renewing their fingerprints; `--write` regenerates the page without renewing evidence. Only the Book I portion of the manuscript is checked here.

## Current author decisions
"""


def render(data, root=ROOT):
    lookup = {s["id"]: s for s in data["spaces"]}
    basis_labels = {
        "story": "Manuscript and VN narrative",
        "story-and-author": "Story and author direction",
        "story-and-vn": "Story and VN images",
        "vn": "Visual novel",
        "author": "Author direction",
        "inference": "Design need inferred from described activities",
        "wiki": "Supporting wiki",
        "story-and-wiki": "Story and supporting wiki",
        "wiki-and-inference": "Wiki roles; spatial needs inferred",
        "remote": "Story: destination away from Lumen",
        "represented-settings": "Narrated or depicted settings",
    }
    out = [INTRO.rstrip(), ""]
    out.extend("- " + decision for decision in data["author_decisions"])
    out.extend(["", "## Complete scene coverage", "",
        "All 32 scenes are accounted for. The table includes settings that are narrated, remembered or depicted as well as places visited. Different image states can show the same location.", "",
        "<details>", "<summary>Show the complete scene-to-space table</summary>", "",
        "| # | Scene | Spaces and requirements |", "|---|---|---|"])
    for i, scene in enumerate(data["scenes"], 1):
        line = line_of(root, scene["source"])
        title = f"[{scene['title']}](../../{scene['source']['path']}#L{line}) (`{scene['id']}`)"
        out.append(f"| {i} | {title} | {links(scene['spaces'], lookup)} |")
    out.extend(["", "</details>", "", "## Spaces and functions", "",
        "Each entry separates the described space, its use, known connections and open questions. Expand its evidence to see the source passages, scene identifiers and original images.", ""])
    groups = list(dict.fromkeys(s["group"] for s in data["spaces"]))
    for group in groups:
        out.extend([f"### {group}", ""])
        for item in data["spaces"]:
            if item["group"] != group:
                continue
            out.extend([f'<a id="{item["id"]}"></a>', f"#### {item['name']}", "",
                f"*Basis: {basis_labels[item['basis']]}.*", "",
                item["facts"], "", f"**Use and privacy:** {item['access']}.", "",
                f"**Location and connection status:** {item['placement']}", "",
                f"**Still to resolve:** {item['unresolved']}", "",
                "<details>", "<summary>Source passages, scenes and VN images</summary>", "",
                "**Passages:** " + "; ".join(dict.fromkeys(source_link(src, root) for src in item["sources"])) + ".", ""])
            scene_ids = [f"`{s['id']}`" for s in data["scenes"] if item["id"] in s["spaces"]]
            if scene_ids:
                out.extend(["**Scene links:** " + ", ".join(scene_ids) + ".", ""])
            assets = [a for a in data["assets"] if item["id"] in a["spaces"]]
            if assets:
                out.extend(["**VN images:** " + "; ".join(
                    f"[{Path(a['path']).name}](../../{a['path']})" for a in assets) + ".", ""])
            out.extend(["</details>", ""])
    out.extend(["## Connections to preserve or resolve", "",
        "Explicit text, audible relationships, visual observations and open attachments are labeled separately. A hearing relationship is not proof of a shared wall; successive scene backgrounds are not proof of an immediate connecting door.", "",
        "| From / to | Basis | Constraint |", "|---|---|---|"])
    for rel in data["relations"]:
        cites = "; ".join(source_link(s, root) for s in rel["sources"])
        kind = {"attachment-open": "Attachment unresolved", "author": "Author direction",
                "carried-project": "Carried project", "audible": "Sound"}.get(rel["kind"], rel["kind"].capitalize())
        out.append(f"| {links([rel['from_id'], rel['to_id']], lookup)} | {kind} | {rel['description']} {cites}. |")
    out.extend(["", "## VN image register", "",
        "All background/CG definitions and all closing-theme images are assigned. The observations record what was inspected; camera limits and production choices remain distinct from textual canon. Existing detailed visual-continuity rules remain in the [production register](../../visual-novel/docs/location-continuity.json). The [annotated atlas](lumen-study/Reference-Atlas.md) presents a selection of these images.", "",
        "<details>", "<summary>Show all 49 inspected images and their spatial observations</summary>", "",
        "| Image / runtime name | Space | Inspected spatial evidence |", "|---|---|---|"])
    for asset in data["assets"]:
        aliases = ", ".join(f"`{s}`" for s in asset["aliases"]) or "Closing theme"
        image = f"[{Path(asset['path']).name}](../../{asset['path']}) · {aliases}"
        out.append(f"| {image} | {links(asset['spaces'], lookup)} | {asset['observation']} |")
    out.extend(["", "</details>"])
    return "\n".join(out) + "\n"


def select(data, query="", group=None, id=None, scene=None, unplaced=False):
    chosen = set(next(s["spaces"] for s in data["scenes"] if s["id"] == scene)) if scene else None
    terms = re.findall(r"\w+", query.casefold())
    result = []
    for item in data["spaces"]:
        if id and item["id"] != id:
            continue
        if group and item["group"].casefold() != group.casefold():
            continue
        if chosen is not None and item["id"] not in chosen:
            continue
        if unplaced and item["model_status"] != "unplaced":
            continue
        searchable = json.dumps(item, ensure_ascii=False).casefold()
        if all(term in searchable for term in terms):
            result.append(item)
    return result


def describe(item, data, root=ROOT):
    print(f"{item['id']} — {item['name']} [{item['basis']}; {item['model_status']}]")
    for label, field in (("Requirement", "facts"), ("Use", "access"),
                         ("Placement", "placement"), ("Open", "unresolved")):
        print(f"  {label}: {item[field]}")
    for src in item["sources"]:
        print(f"  Source: {src['path']}:{line_of(root, src)} — {src['anchor']}")
    for asset in data["assets"]:
        if item["id"] in asset["spaces"]:
            print(f"  Image: {asset['path']} — {asset['observation']}")
    for rel in data["relations"]:
        if item["id"] in (rel["from_id"], rel["to_id"]):
            print(f"  Connection ({rel['kind']}): {rel['from_id']} → {rel['to_id']}: {rel['description']}")
    scene_ids = [s["id"] for s in data["scenes"] if item["id"] in s["spaces"]]
    print("  Scenes: " + (", ".join(scene_ids) or "Supporting provision; no direct Book I scene"))
    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="keyword terms; all must occur in a record")
    parser.add_argument("--group", help="exact group name, e.g. Household")
    parser.add_argument("--id", help="exact space identifier")
    parser.add_argument("--scene", help="exact VN scene identifier")
    parser.add_argument("--unplaced", action="store_true")
    parser.add_argument("--brief", action="store_true", help="one line per matching record")
    parser.add_argument("--json", action="store_true", help="machine-readable matching records")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--check", action="store_true", help="verify sources, mappings and generated page")
    output.add_argument("--write", action="store_true", help="regenerate reference page after verifying evidence")
    args = parser.parse_args()
    data = json.loads(DATA.read_text(encoding="utf-8"))
    errors = check(data)
    if errors:
        print("Inventory needs review:\n" + "\n".join("- " + e for e in errors), file=sys.stderr)
        return 1
    if args.check or args.write:
        page = render(data)
        if args.write:
            PAGE.write_text(page, encoding="utf-8")
        elif not PAGE.is_file() or PAGE.read_text(encoding="utf-8") != page:
            print("Generated reference page differs; run --write after reviewing the register.", file=sys.stderr)
            return 1
        print(f"{'Wrote' if args.write else 'Checked'} {len(data['spaces'])} records, "
              f"{len(data['scenes'])} scenes, {len(data['assets'])} inspected images, "
              f"{len(data['relations'])} connections. No layout validation implied.")
        return 0
    if args.scene and args.scene not in {s["id"] for s in data["scenes"]}:
        parser.error("unknown scene; use an identifier from BOOK_SCENES")
    matches = select(data, " ".join(args.query), args.group, args.id, args.scene, args.unplaced)
    if args.json:
        print(json.dumps(matches, ensure_ascii=False, indent=2))
    elif args.brief:
        for item in matches:
            print(f"{item['id']}: {item['name']} [{item['basis']}; {item['model_status']}]")
    else:
        for item in matches:
            describe(item, data)
    if not matches:
        print("No registered match. Search the original sources; absence here is not a canon finding.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
