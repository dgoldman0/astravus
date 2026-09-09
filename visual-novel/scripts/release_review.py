#!/usr/bin/env python3
"""Record reproducible release evidence without turning file hashes into visual approval."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

PROJECT = Path(__file__).resolve().parents[1]
MATRIX = PROJECT / "docs/release-matrix.json"
EVIDENCE = PROJECT / "docs/release-evidence.json"
PHASES = {"content": 0, "runtime": 1, "exports": 2}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read_matrix():
    data = json.loads(MATRIX.read_text())
    if data["schema_version"] != 1:
        raise ValueError("Unsupported release matrix schema")
    rows = data["checks"]
    ids = {row["id"] for row in rows}
    if len(ids) != len(rows):
        raise ValueError("Duplicate release check ID")
    for row in rows:
        if row["phase"] not in PHASES or row["method"] not in ("automated", "manual", "limitation"):
            raise ValueError(f"Invalid phase/method: {row['id']}")
        if not row["acceptance"] or not row["authority"]:
            raise ValueError(f"Missing acceptance or authority: {row['id']}")
        if set(row.get("requires", [])) - ids:
            raise ValueError(f"Unknown dependency: {row['id']}")
    scenes = re.findall(r'^\s*\("([a-z_]+)", "([^"]+)"\),$',
                        (PROJECT / "game/book_structure.rpy").read_text(), re.M)
    if [(row["key"], row["title"]) for row in data["scenes"]] != scenes:
        raise ValueError("Matrix must cover every story scene in runtime order")
    for scene in data["scenes"]:
        if not set(scene["checks"]) <= ids or not scene["checks"]:
            raise ValueError(f"Missing scene checks: {scene['key']}")
    return data


def snapshot(matrix, row):
    """Hash selected files, missing patterns, and this row's exact acceptance contract."""
    patterns = list(row.get("inputs", []))
    for group in row.get("input_groups", []):
        patterns.extend(matrix["input_groups"][group])
    files = {}
    missing = []
    for pattern in sorted(set(patterns)):
        matches = sorted(path for path in PROJECT.glob(pattern) if path.is_file())
        if not matches:
            missing.append(pattern)
        for path in matches:
            if not path.resolve().is_relative_to(PROJECT.parent):
                raise ValueError(f"Input outside repository: {pattern}")
            files[path.relative_to(PROJECT).as_posix()] = file_digest(path)
    result = {"files": files, "missing_patterns": missing, "contract": row}
    # Changing receipt plumbing is not a change to a manually reviewed scene.
    # Automated evidence also depends on the runner that executes its checks.
    if row["method"] == "automated":
        result["tool_sha256"] = file_digest(Path(__file__))
    return result


def review_file(name):
    """Allow production files and the dedicated sibling development workspace."""
    path = (PROJECT / name).resolve()
    roots = (PROJECT.resolve(), (PROJECT.parent / "development/visual-novel").resolve())
    if not any(path.is_relative_to(root) for root in roots) or not path.is_file():
        raise ValueError(f"Review file must be in the project or its development workspace: {name}")
    return path


def evidence_hashes(paths):
    result = {}
    for name in paths:
        path = review_file(name)
        result[Path(os.path.relpath(path, PROJECT)).as_posix()] = file_digest(path)
    return result


def load_receipts():
    return json.loads(EVIDENCE.read_text()) if EVIDENCE.exists() else {"schema_version": 1, "receipts": {}}


def comparison_signature(reference):
    """Resolve an actual immutable Git blob, recorded generation, or current local reference."""
    kind, separator, value = reference.partition(":")
    if not separator:
        raise ValueError("Comparison must use git:BLOB, generation:ID or file:PROJECT_PATH")
    if kind == "git":
        if not re.fullmatch(r"[0-9a-f]{40}", value):
            raise ValueError("Git comparison needs the full immutable blob ID")
        result = subprocess.run(["git", "cat-file", "-t", value], cwd=PROJECT,
                                capture_output=True, text=True)
        if result.returncode or result.stdout.strip() != "blob":
            raise ValueError("Comparison Git blob is unavailable")
        return value
    if kind == "generation":
        for path in sorted((PROJECT / "docs").glob("*assets.json")):
            for generation in json.loads(path.read_text()).get("generations", []):
                if generation["id"] == value:
                    return digest(generation)
        raise ValueError("Comparison generation is not in the asset manifests")
    if kind == "file":
        return file_digest(review_file(value))
    raise ValueError("Comparison must use git:BLOB, generation:ID or file:PROJECT_PATH")


def save_receipt(row, before, outcome, reviewer, notes, artifacts, command=None, returncode=None,
                 comparison_reference=None):
    receipt = {
        "outcome": outcome, "method": row["method"], "reviewer": reviewer,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "input_sha256": digest(before), "input_file_count": len(before["files"]),
        "input_files": before["files"],
        "notes": notes, "evidence": evidence_hashes(artifacts),
        **({"comparison_reference": comparison_reference,
            "comparison_signature": comparison_signature(comparison_reference)} if comparison_reference else {}),
        **({"command": command, "returncode": returncode} if command else {}),
    }
    # Independent reviewers may finish together. Preserve both receipts atomically.
    lock = PROJECT / "test-results/release-matrix/evidence.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    with lock.open("w") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        data = load_receipts()
        data["receipts"][row["id"]] = receipt
        # One current receipt per check; obsolete snapshots are not retained.
        temporary = EVIDENCE.with_suffix(".tmp")
        temporary.write_text(json.dumps(data, indent=2) + "\n")
        temporary.replace(EVIDENCE)


def check_status(matrix, row, receipts):
    receipt = receipts.get(row["id"])
    if receipt is None:
        return "PENDING", row.get("open_note", "No current evidence recorded")
    current = snapshot(matrix, row)
    if receipt.get("method") != row["method"] or receipt.get("input_sha256") != digest(current):
        previous = receipt.get("input_files", {})
        changed = [name for name in sorted(set(previous) | set(current["files"]))
                   if previous.get(name) != current["files"].get(name)] if previous else []
        suffix = ": " + ", ".join(changed[:4]) + (" …" if len(changed) > 4 else "") if changed else ""
        return "STALE", "Relevant inputs or acceptance criteria changed after the review" + suffix
    for name, expected in receipt.get("evidence", {}).items():
        path = PROJECT / name
        if not path.is_file() or file_digest(path) != expected:
            return "STALE", f"Evidence missing or changed: {name}"
    outcome = receipt.get("outcome")
    if outcome == "pass" and row["method"] != "limitation":
        if not receipt.get("evidence") or not receipt.get("notes"):
            return "PENDING", "Passing evidence and review notes are required"
        if row["method"] == "automated" and receipt.get("returncode") != 0:
            return "FAIL", "Automated command did not pass"
        if row.get("quality_dimensions") and not receipt.get("comparison_reference"):
            return "PENDING", "Image quality review needs an explicitly chosen comparison reference"
        if receipt.get("comparison_reference"):
            try:
                current_comparison = comparison_signature(receipt["comparison_reference"])
            except ValueError as error:
                return "STALE", str(error)
            if current_comparison != receipt.get("comparison_signature"):
                return "STALE", "Selected quality comparison changed after the review"
        return "PASS", receipt["notes"]
    if outcome == "limited" and row["method"] == "limitation":
        return "LIMITED", receipt["notes"]
    if outcome == "review":
        return "REVIEW", receipt["notes"]
    return "FAIL", receipt.get("notes", "Review failed")


def candidate_builds_ready(row):
    requested = row.get("candidate_builds", [])
    if not requested:
        return True
    path = PROJECT / "build/release-builds.json"
    builds = json.loads(path.read_text()).get("builds", {}) if path.exists() else {}
    for name in requested:
        build = builds.get(name, {})
        if build.get("kind") != "candidate" or not build.get("files"):
            return False
        for artifact, expected in build["files"].items():
            path = PROJECT / artifact
            if not path.is_file() or file_digest(path) != expected:
                return False
    return True


def status(matrix, phase="exports"):
    receipts = load_receipts()["receipts"]
    states = {row["id"]: check_status(matrix, row, receipts) for row in matrix["checks"]}
    # Dependency failures cannot be hidden by an otherwise current receipt.
    for _ in matrix["checks"]:
        changed = False
        for row in matrix["checks"]:
            dependencies = [name for name in row.get("requires", []) if states[name][0] != "PASS"]
            if states[row["id"]][0] == "PASS" and dependencies:
                states[row["id"]] = ("BLOCKED", "Dependencies need review: " + ", ".join(dependencies))
                changed = True
        if not changed:
            break
    selected = [row for row in matrix["checks"] if PHASES[row["phase"]] <= PHASES[phase]]
    lines = [f"Release {matrix['release_version']} — evidence status ({phase})"]
    for row in selected:
        state, reason = states[row["id"]]
        lines.append(f"{state:8} {row['id']:25} {row['title']}")
        if state not in ("PASS", "LIMITED"):
            lines.append("         " + reason)
    counts = {name: sum(states[row["id"]][0] == name for row in selected)
              for name in ("PASS", "PENDING", "STALE", "BLOCKED", "FAIL", "REVIEW", "LIMITED")}
    lines.append("; ".join(f"{number} {name.lower()}" for name, number in counts.items() if number))
    lines.append("REVIEW is temporary-build evidence; LIMITED is unverified. Neither counts as a final pass.")
    print("\n".join(lines))
    report = PROJECT / "test-results/release-matrix-status.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps({"release_version": matrix["release_version"], "phase": phase,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "checks": {row["id"]: {"status": states[row["id"]][0], "reason": states[row["id"]][1]}
                   for row in selected}, "counts": counts}, indent=2) + "\n")
    markdown = [f"# Release {matrix['release_version']} review matrix", "",
                "Generated from current files; REVIEW and LIMITED never count as final passes.", "",
                "| Check | Status | Acceptance / reference | Evidence date and input hash |",
                "| --- | --- | --- | --- |"]
    for row in selected:
        receipt = receipts.get(row["id"], {})
        reference = "; ".join(row["authority"])
        checked = receipt.get("checked_at_utc", "Not reviewed")
        signature = receipt.get("input_sha256", "")
        details = " ".join(row["acceptance"]) + " Reference: " + reference
        markdown.append(f"| {row['id']} | {states[row['id']][0]} | {details.replace('|', '/')} | {checked}<br>{signature} |")
    report.with_suffix(".md").write_text("\n".join(markdown) + "\n")
    return any(states[row["id"]][0] != "PASS" for row in selected if row.get("required", True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    report = commands.add_parser("status")
    report.add_argument("--phase", choices=PHASES, default="exports")
    report.add_argument("--strict", action="store_true")
    run = commands.add_parser("run")
    run.add_argument("check")
    record = commands.add_parser("record")
    record.add_argument("check")
    record.add_argument("--outcome", choices=("pass", "fail", "limited"), required=True)
    record.add_argument("--reviewer", required=True)
    record.add_argument("--notes", required=True)
    record.add_argument("--evidence", action="append", default=[])
    record.add_argument("--comparison-reference", help="Chosen prior Git blob/generation or approved image for quality review")
    args = parser.parse_args()
    matrix = read_matrix()
    if args.action == "status":
        failed = status(matrix, args.phase)
        return int(args.strict and failed)
    row = next((row for row in matrix["checks"] if row["id"] == args.check), None)
    if row is None:
        parser.error("Unknown check ID")
    before = snapshot(matrix, row)
    if args.action == "record":
        if row["method"] == "automated":
            parser.error("Automated checks must be executed with run; old logs cannot be promoted to a pass")
        if args.outcome == "limited" and row["method"] != "limitation":
            parser.error("Required checks cannot be waived as limited")
        if args.outcome == "pass" and (row["method"] != "manual" or not args.evidence):
            parser.error("Manual passing review requires concrete evidence")
        if args.outcome == "pass" and row.get("quality_dimensions") and not args.comparison_reference:
            parser.error("Per-image quality review requires a deliberately selected comparison reference")
        save_receipt(row, before, args.outcome, args.reviewer, args.notes, args.evidence,
                     comparison_reference=args.comparison_reference)
    else:
        if row["method"] != "automated" or not row.get("command"):
            parser.error("This check requires explicit review; no automated command can approve it")
        log = PROJECT / "test-results/release-matrix" / (row["id"] + ".log")
        log.parent.mkdir(parents=True, exist_ok=True)
        command = [sys.executable if part == "{python}" else part for part in row["command"]]
        print("Running " + " ".join(command), flush=True)
        with log.open("w") as stream:
            stream.write("Command: " + json.dumps(command) + "\n")
            stream.flush()
            result = subprocess.run(command, cwd=PROJECT, stdout=stream, stderr=subprocess.STDOUT)
        unchanged = before == snapshot(matrix, row)
        outcome = "pass" if result.returncode == 0 and unchanged else "fail"
        notes = ("Command passed on unchanged inputs." if outcome == "pass" else
                 "Inputs changed while the command ran." if not unchanged else f"Command exited {result.returncode}.")
        if outcome == "pass" and not candidate_builds_ready(row):
            outcome = "review"
            notes = "Command passed for temporary/unapproved artifacts; a current candidate build is required for final signoff."
        artifacts = [log.relative_to(PROJECT).as_posix()]
        artifacts.extend(row.get("generated_evidence", []))
        artifacts = [name for name in artifacts if (PROJECT / name).is_file()]
        save_receipt(row, before, outcome, "release_review command runner", notes,
                     artifacts, command, result.returncode)
        print(f"{outcome.upper()}: {notes} Evidence: {log.relative_to(PROJECT)}")
        return int(outcome != "pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
