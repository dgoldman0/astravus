#!/usr/bin/env python3
"""Build the interactive local connection reference.

The main proposal article is edited separately and is never overwritten here.

--check verifies source freshness, allocation/scene coverage, declared routes
and generated output. These are topology checks, not physical validation.
"""
import argparse
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import space_inventory as inventory

HERE = Path(__file__).resolve().parent
DATA = HERE / "local-connections.json"
RESIDENTS = {"Cali", "Kael", "Lyra", "Maia", "Arin", "Selene", "Dorian", "Sage"}
PRIVATE = {"cali_room", "kael_room", "lyra_room", "adult_retreats", "sage_room"}


def validate(proposal, sources):
    errors = inventory.check(sources)
    if proposal.get("schema_version") != 1:
        return errors + ["Unsupported connection proposal schema"]
    if proposal["inventory_sha256"] != hashlib.sha256(inventory.DATA.read_bytes()).hexdigest():
        errors.append("Source inventory changed; review the connection choices before renewing its fingerprint")
    known = {s["id"] for s in sources["spaces"]}
    allocations = [a["space_id"] for a in proposal["allocations"]]
    if set(allocations) != known or len(allocations) != len(known):
        errors.append("Every inventory item must have exactly one connection disposition; "
                      f"missing: {sorted(known - set(allocations))}; "
                      f"unknown: {sorted(set(allocations) - known)}")
    for a in proposal["allocations"]:
        if not all(a.get(key) for key in ("zone", "treatment", "choice")):
            errors.append(f"Incomplete disposition: {a['space_id']}")
    scenes = [s["id"] for s in sources["scenes"]]
    if [w["scene_id"] for w in proposal["walkthroughs"]] != scenes:
        errors.append("Walkthrough coverage/order differs from the complete scene register")
    people = [p["resident"] for p in proposal["private_provision"]]
    if set(people) != RESIDENTS or any(n != 1 for n in Counter(people).values()):
        errors.append("Private provision must account for each of the eight residents exactly once")
    for p in proposal["private_provision"]:
        if p["space_id"] not in PRIVATE or not p.get("proposal"):
            errors.append(f"Invalid private provision: {p['resident']}")
    edges = set()
    for e in proposal["edges"]:
        if e["a"] not in known or e["b"] not in known or not e.get("note"):
            errors.append(f"Invalid connection: {e['a']} / {e['b']}")
        key = frozenset((e["a"], e["b"]))
        if len(key) != 2 or key in edges:
            errors.append(f"Duplicate/self connection: {e['a']} / {e['b']}")
        edges.add(key)
    for w in proposal["walkthroughs"]:
        path = w["path"]
        if not path or not w.get("assessment") or not set(path) <= known:
            errors.append(f"Incomplete/unknown walkthrough: {w['scene_id']}")
        for a, b in zip(path, path[1:]):
            if frozenset((a, b)) not in edges:
                errors.append(f"Undeclared route in {w['scene_id']}: {a} → {b}")
        if PRIVATE.intersection(path[1:-1]):
            errors.append(f"Walkthrough crosses a private room en route elsewhere: {w['scene_id']}")
    # A shared woodland route must remain possible without traversing the home,
    # household garden or either occupied oak refuge.
    shared = {"community_routes", "courtyard", "local_landscape", "echoes_grove", "central_plaza"}
    reached, pending = set(), ["courtyard"]
    while pending:
        node = pending.pop()
        if node in reached:
            continue
        reached.add(node)
        pending.extend(other for e in edges if node in e for other in e if other in shared - reached)
    if not shared <= reached:
        errors.append("Shared destinations lack a route bypassing household/private refuge space")
    return errors


def outputs(proposal, sources):
    sources = copy.deepcopy(sources)
    payload = dict(proposal=proposal, inventory=sources)
    # Add current source line locators without changing the source register.
    for space in sources["spaces"]:
        for src in space["sources"]:
            src["line"] = inventory.line_of(inventory.ROOT, src)
    for scene in sources["scenes"]:
        scene["source"]["line"] = inventory.line_of(inventory.ROOT, scene["source"])
        src = scene["source"]
        tail = inventory.read(inventory.ROOT, src["path"]).split(src["anchor"], 1)[1]
        first = re.search(r"^\s*scene ((?:bg|cg) \w+)", tail, re.M)
        if not first:
            raise ValueError(f"No opening image found for {scene['id']}")
        scene["opening_image"] = next(a["path"] for a in sources["assets"] if first[1] in a["aliases"])
    encoded = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    template = (HERE / "connections.template.html").read_text()
    return {HERE / "connections.html": template.replace("__CONNECTION_DATA__", encoded)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    proposal = json.loads(DATA.read_text())
    sources = json.loads(inventory.DATA.read_text())
    errors = validate(proposal, sources)
    if errors:
        raise SystemExit("Connection proposal needs review:\n" + "\n".join(errors))
    for target, content in outputs(proposal, sources).items():
        if args.check:
            if not target.is_file() or target.read_text() != content:
                raise SystemExit(f"Generated output differs: {target.name}; run build_connections.py")
        else:
            target.write_text(content)
    print(f"{'Checked' if args.check else 'Built'} connection review: "
          f"{len(proposal['allocations'])} dispositions, {len(proposal['walkthroughs'])} scenes, "
          f"{len(proposal['private_provision'])} residents. Geometry remains untested.")


if __name__ == "__main__":
    main()
