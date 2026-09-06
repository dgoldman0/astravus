#!/usr/bin/env python3
"""Build the portable wiki review and atlas; --check verifies source freshness.

Run from any directory. Python standard library only. Runtime VN files are read,
never modified or copied. Edit the SVGs directly; this script does not redraw them.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify fingerprints and generated pages without writing")
    args = parser.parse_args()
    references = json.loads((HERE / "references.json").read_text())
    study = json.loads((HERE / "study-data.json").read_text())
    stale = []
    for item in references["source_files"] + references["references"]:
        source = ROOT / item["path"]
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != item["sha256"]:
            stale.append(item["path"])
    if stale:
        raise SystemExit("Inspected sources changed; review evidence before updating fingerprints:\n" + "\n".join(stale))
    template = (HERE / "review.template.html").read_text()
    page = template.replace("__REFERENCES_JSON__", json.dumps(references, ensure_ascii=False).replace("<", "\\u003c"))
    page = page.replace("__STUDY_JSON__", json.dumps(study, ensure_ascii=False).replace("<", "\\u003c"))
    atlas = [
        "# Lumen: current VN reference atlas", "",
        "**Inspected 6 September 2026 · observations and proposed interpretations, not new canon**", "",
        "[Design study](../Lumen-Design-Study.md) · [Interactive annotated plates](review.html#references)", "",
        "The primary visual sources are the image files actually named in the current VN runtime definitions, read together with their scene code and action staging. Older outside illustrations are not core references. The runtime uses a 1920 × 1080 cover fit; the review follows that image framing without simulating actors, dialogue or interface overlays.", "",
        "The numbered observations correspond to separate markers in the browser review. Original art is linked directly and remains unchanged. Exact SHA-256 fingerprints and additional inspected source files are in [references.json](references.json). They identify the inspected revision, not design approval or calibrated geometry.", "",
    ]
    for ref in references["references"]:
        atlas.extend([
            f"## {ref['title']}", "",
            f"![{ref['title']}](../../../{ref['path']})", "",
            f"**Runtime:** {ref['runtime']}. [Original image](../../../{ref['path']}).", "",
            f"**Story locator:** {ref['story']}.", "",
            f"**Visible evidence:** {ref['observed']}", "",
        ])
        atlas.extend(f"{i}. {pin['text']}" for i, pin in enumerate(ref["pins"], 1))
        atlas.extend(["", f"**Proposed interpretation:** {ref['proposal']}", "", f"**Not established:** {ref['unknown']}", ""])
    atlas.extend([
        "## Narrative and production scope", "",
        "Read the plates alongside [script.rpy](../../../visual-novel/game/script.rpy), [family_book_one.rpy](../../../visual-novel/game/family_book_one.rpy), [friendships_book_one.rpy](../../../visual-novel/game/friendships_book_one.rpy), [visuals.rpy](../../../visual-novel/game/visuals.rpy) and [environments_book_one.rpy](../../../visual-novel/game/environments_book_one.rpy). The source locators refer to the recorded revision and may move in later edits.", "",
        "The full-life checks use [latest.md](../../../revision/latest.md) and the [timeline](../../TIMELINE.md), not just the adapted childhood scenes. The [adaptation guide](../../../visual-novel/docs/ADAPTATION.md), [art direction](../../../visual-novel/docs/ART_DIRECTION.md) and [location continuity record](../../../visual-novel/docs/location-continuity.json) supply production context. For this redesign, the author's current VN-first instruction supersedes the older external-reference ranking in the art guide.", "",
        "Later comparison should also include the pond background, rain and later treehouse states, memorial versions of the plaza, and home painting/grief states. This selected atlas is a first spatial study, not a claim that every VN frame has been reconciled into one measured environment. Dream scenes are not measurements of physical Lumen.", "",
    ])
    outputs = {"review.html": page, "Reference-Atlas.md": "\n".join(atlas)}
    for filename, content in outputs.items():
        target = HERE / filename
        if args.check:
            if not target.is_file() or target.read_text() != content:
                raise SystemExit(f"Generated file differs: {filename}; run build_review.py")
        else:
            target.write_text(content)
    print(f"{'Checked' if args.check else 'Built'} review and atlas; {len(references['references'])} VN plates and {len(references['source_files'])} context files match the inspected sources.")


if __name__ == "__main__":
    main()
