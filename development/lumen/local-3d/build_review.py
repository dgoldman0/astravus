#!/usr/bin/env python3
"""Embed the exported Blender geometry and checks in a portable offline review.

Run after the model builder has written model-review.json and validation.json.
The page uses no external libraries. Original VN images and Blender renders stay
linked beside the page or elsewhere in the repository; geometry is embedded.
"""

import argparse
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def vector(value, length, label):
    if not isinstance(value, list) or len(value) != length:
        raise ValueError(f"{label}: expected {length} numbers")
    if not all(isinstance(n, (int, float)) and not isinstance(n, bool) and math.isfinite(n) for n in value):
        raise ValueError(f"{label}: coordinates must be finite numbers")


def validate(model, validation):
    """Check the viewer input contract, not the architectural design."""
    if model.get("units") != "metres":
        raise ValueError("The model must explicitly use metres")
    vector(model["bounds"]["min"], 3, "bounds.min")
    vector(model["bounds"]["max"], 3, "bounds.max")
    if not all(a < b for a, b in zip(model["bounds"]["min"], model["bounds"]["max"])):
        raise ValueError("Model bounds must have positive width, depth and height")
    groups = [g["id"] for g in model["groups"]]
    if len(groups) != len(set(groups)):
        raise ValueError("Group IDs must be unique")
    if not model["meshes"] or not model["cameras"]:
        raise ValueError("The review needs geometry and at least one saved camera")
    for mesh in model["meshes"]:
        label = mesh["name"]
        if mesh["group"] not in groups:
            raise ValueError(f"{label}: unknown group")
        vertices, triangles = mesh["vertices"], mesh["triangles"]
        if not vertices or len(vertices) % 3 or not triangles or len(triangles) % 3:
            raise ValueError(f"{label}: incomplete vertices or triangles")
        vector(vertices, len(vertices), f"{label} vertices")
        vector(mesh["color"], 3, f"{label} color")
        if any(c < 0 or c > 1 for c in mesh["color"]):
            raise ValueError(f"{label}: RGB values must be between zero and one")
        if any(not isinstance(i, int) or isinstance(i, bool) or i < 0 or i >= len(vertices) // 3 for i in triangles):
            raise ValueError(f"{label}: triangle index outside vertex array")
    camera_ids = []
    for camera in model["cameras"]:
        camera_ids.append(camera["id"])
        vector(camera["position"], 3, f"{camera['id']} position")
        vector(camera["target"], 3, f"{camera['id']} target")
        if sum((a - b) ** 2 for a, b in zip(camera["position"], camera["target"])) < 1e-8:
            raise ValueError(f"{camera['id']}: camera and target coincide")
        if not isinstance(camera["fov"], (int, float)) or not 1 < camera["fov"] < 175:
            raise ValueError(f"{camera['id']}: field of view must be between 1 and 175 degrees")
        if any(group not in groups for group in camera.get("hide_groups", [])):
            raise ValueError(f"{camera['id']}: unknown hidden group")
        for key in ("render", "reference"):
            path = camera.get(key)
            if path and (not isinstance(path, str) or ":" in path or path.startswith("/")):
                raise ValueError(f"{camera['id']}: {key} must be a relative file path")
    if len(camera_ids) != len(set(camera_ids)):
        raise ValueError("Camera IDs must be unique")
    for label in model.get("labels", []):
        vector(label["position"], 3, f"{label['text']} label")
        if label["group"] not in groups:
            raise ValueError(f"{label['text']}: unknown label group")
    for check in validation["checks"]:
        if check["status"] not in ("pass", "fail", "open"):
            raise ValueError(f"{check['id']}: unknown check status")
        if not isinstance(check["title"], str) or not isinstance(check["detail"], str):
            raise ValueError(f"{check['id']}: check title and detail must be readable text")


def build(directory=HERE, check=False):
    directory = Path(directory)
    model = json.loads((directory / "model-review.json").read_text())
    validation = json.loads((directory / "validation.json").read_text())
    validate(model, validation)
    page = (directory / "review.template.html").read_text()
    for token, value in (("__MODEL_JSON__", model), ("__VALIDATION_JSON__", validation)):
        if page.count(token) != 1:
            raise ValueError(f"Template must contain exactly one {token} placeholder")
        page = page.replace(token, json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).replace("<", "\\u003c"))
    output = directory / "review.html"
    if check:
        if not output.is_file() or output.read_text() != page:
            raise ValueError("review.html is stale; run build_review.py after rebuilding the model")
    else:
        output.write_text(page)
    return f"{'Checked' if check else 'Built'} offline review: {len(model['meshes'])} meshes, {len(model['cameras'])} cameras and {len(validation['checks'])} checks."


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify the generated page without writing")
    args = parser.parse_args()
    try:
        print(build(check=args.check))
    except (KeyError, TypeError, ValueError, OSError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
