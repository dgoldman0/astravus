#!/usr/bin/env python3
"""Capture the real opening and say screen in isolated Ren'Py projects.

Only this review directory receives outputs. Shipped sources, image assets,
compiled scripts, caches and user saves are never modified by this runner.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


REVIEW = Path(__file__).resolve().parent
PROJECT = REVIEW.parents[3] / "visual-novel"
SOURCE = REVIEW / "opening-original.png"
FINAL = REVIEW / "opening-refined-v1.png"
SDK = Path(os.environ.get("ASTRAVUS_RENPY_SDK", PROJECT / ".cache/renpy-8.5.3-sdk"))
TEXT = "They told me about the Sanctuary. About my First Breath, and the five pairs of hands waiting to hold me."
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".ogg", ".mp3", ".wav", ".ttf", ".otf", ".svg"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_snapshot() -> dict[str, str]:
    paths = [*PROJECT.glob("game/*.rpy"), SOURCE]
    return {os.path.relpath(path, PROJECT): digest(path) for path in paths}


def copy_source(src: str, dst: str) -> str:
    if Path(src).suffix.lower() in ASSET_SUFFIXES:
        os.symlink(Path(src).resolve(), dst)
        return dst
    return shutil.copy2(src, dst)


def capture(variant: str, image: Path) -> dict:
    if not image.is_file():
        raise SystemExit(f"Missing final input: {image}")
    snapshot = source_snapshot()
    with tempfile.TemporaryDirectory(prefix=f"astravus-opening-{variant}-") as temp_name:
        temp = Path(temp_name)
        root = temp / "project"
        root.mkdir()
        shutil.copytree(
            PROJECT / "game", root / "game", copy_function=copy_source,
            ignore=shutil.ignore_patterns("saves", "cache", "__pycache__", "*.rpyc", "*.pyc"),
        )
        target = root / "game/images/cg/first-memory-young.png"
        target.unlink()
        target.symlink_to(image.resolve())
        output = temp / "captures"
        output.mkdir()
        metadata = output / "runtime.json"
        test = f'''testcase opening_character_refinement_capture:
    $ _test.force = True
    $ _test.screenshot_directory = {str(output)!r}
    $ preferences.fullscreen = True
    $ preferences.text_cps = 0
    assert screen "main_menu"
    click "Begin Book I"
    assert screen "chapter_card" timeout 4.0
    click "Enter the memory"
    assert eval (renpy.showing("cg first_memory") and not renpy.showing("calista")) timeout 4.0
    advance until eval (_history_list[-1].what == {TEXT!r})
    assert screen "say"
    assert eval ({TEXT!r} in _test_screen_text("say"))
    assert eval (scene_key == "first_memory" and renpy.showing("cg first_memory"))
    pause .5
    screenshot "runtime"
    $ __import__("json").dump({{"engine": renpy.version(), "renderer": renpy.get_renderer_info(), "scene": scene_key, "say_text": _history_list[-1].what, "say_screen_present": bool(renpy.get_screen("say")), "logical_size": [config.screen_width, config.screen_height], "screen_size": list(renpy.get_physical_size()), "image_attributes": list(renpy.get_attributes("cg"))}}, open({str(metadata)!r}, "w"), indent=2)
'''
        (root / "game/_opening_refinement_capture.rpy").write_text(test)
        env = dict(os.environ, RENPY_PATH_TO_SAVES=str(temp / "saves"), SDL_AUDIODRIVER="dummy")
        command = ["xvfb-run", "-a", "-s", "-screen 0 1920x1080x24", str(SDK / "renpy.sh"),
                   str(root), "test", "opening_character_refinement_capture", "--overwrite-screenshots",
                   "--hide-execution", "hooks"]
        run = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=90)
        log = run.stdout + run.stderr
        (REVIEW / f"runtime-{variant}-capture.log").write_text(log)
        if run.returncode:
            raise RuntimeError(f"Ren'Py capture failed ({run.returncode}):\n{log[-10000:]}")
        shots = list(output.rglob("*.png"))
        if len(shots) != 1:
            raise RuntimeError(f"Expected one actual screenshot, found {shots}")
        shot = REVIEW / f"runtime-{variant}.png"
        shutil.copy2(shots[0], shot)
        details = json.loads(metadata.read_text())
        details.update({
            "variant": variant,
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "input": os.path.relpath(image, PROJECT),
            "input_sha256": digest(image),
            "screenshot": shot.name,
            "screenshot_sha256": digest(shot),
            "dialogue_id": "opening_003",
            "testcase": "opening_character_refinement_capture",
            "scope": "Actual opening only, entered from the real main menu and chapter card",
            "isolation": "Temporary source copy, symlinked assets, separate temporary saves; removed after capture",
            "source_unchanged": snapshot == source_snapshot(),
            "source_hashes": snapshot,
            "test_exit_code": run.returncode,
            "log": f"runtime-{variant}-capture.log",
        })
        if not details["source_unchanged"]:
            raise RuntimeError("Shipping source snapshot changed during capture; inspect concurrent edits")
        return details


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=("before", "after", "both"), default="both")
    args = parser.parse_args()
    notes = REVIEW / "runtime-capture-notes.json"
    results = json.loads(notes.read_text()) if notes.exists() else {}
    for variant, path in (("before", SOURCE), ("after", FINAL)):
        if args.variant in (variant, "both"):
            results[variant] = capture(variant, path)
            notes.write_text(json.dumps(results, indent=2) + "\n")
            print(f"Captured {results[variant]['screenshot']} with {results[variant]['engine']}", flush=True)


if __name__ == "__main__":
    main()
