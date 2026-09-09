"""Restore Shadow's small ear notch using only adjacent source-background pixels.

No image model, whole-image filter, or runtime asset mutation is involved. Masks,
donor offsets and source hashes are explicit in docs/graphics-shadow-notch-spec.json.
Outputs and reproducible recipes are staged under ../development/visual-novel/archive/local/graphics-workspace/shadow.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/graphics-shadow-notch-spec.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def retouch(source, spec):
    rgb = np.asarray(source).copy()
    if source.mode != "RGB":
        raise ValueError("The reviewed source must remain RGB")
    scale = spec["supersample"]
    points = np.asarray(spec["polygon"], dtype=np.float64)
    left, top = np.floor(points.min(axis=0) - 2).astype(int)
    right, bottom = np.ceil(points.max(axis=0) + 2).astype(int) + 1
    width, height = right - left, bottom - top
    mask = Image.new("L", (width * scale, height * scale), 0)
    ImageDraw.Draw(mask).polygon(
        [((x - left) * scale, (y - top) * scale) for x, y in points],
        fill=255,
    )
    mask = mask.filter(ImageFilter.GaussianBlur(spec["feather_pixels"] * scale))
    mask = mask.resize((width, height), Image.Resampling.BOX)
    weight = np.asarray(mask, dtype=np.float64) / 255
    dx, dy = spec["donor_offset"]
    donor_box = (left + dx, top + dy, right + dx, bottom + dy)
    donor = np.asarray(source.crop(donor_box), dtype=np.float64)
    original = rgb[top:bottom, left:right].astype(np.float64)
    mixed = np.rint(original * (1 - weight[..., None]) + donor * weight[..., None])
    rgb[top:bottom, left:right] = mixed.astype(np.uint8)
    full_mask = np.zeros(rgb.shape[:2], dtype=np.uint8)
    full_mask[top:bottom, left:right] = np.asarray(mask)
    changed = np.any(rgb != np.asarray(source), axis=2)
    assert not np.any(changed & (full_mask == 0))
    ys, xs = np.where(changed)
    return Image.fromarray(rgb), Image.fromarray(full_mask), {
        "changed_pixels": int(changed.sum()),
        "outside_mask_pixels_changed": 0,
        "outside_mask_identical": True,
        "canvas_and_mode_unchanged": True,
        "change_bbox": [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1],
        "donor_box": [int(v) for v in donor_box],
        "operation_scope": "Adjacent source background sampled through a small antialiased ear-notch mask; all other pixels preserved exactly.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "../development/visual-novel/archive/local/graphics-workspace/shadow")
    args = parser.parse_args()
    data = json.loads(SPEC.read_text())
    reference = ROOT / data["reference_file"]
    assert sha256(reference) == data["reference_sha256"], "Reference changed; inspect the anatomical side again"
    args.output.mkdir(parents=True, exist_ok=True)
    records = []
    for spec in data["assets"]:
        source = ROOT / spec["file"]
        original = subprocess.check_output(
            ["git", "cat-file", "blob", spec["source_git_blob"]], cwd=ROOT
        )
        assert hashlib.sha256(original).hexdigest() == spec["source_sha256"], f"Source blob changed: {source}"
        image = Image.open(io.BytesIO(original))
        result, mask, proof = retouch(image, spec)
        output = args.output / source.name
        mask_path = args.output / (source.stem + "-mask.png")
        result.save(output)
        mask.save(mask_path)
        records.append({
            **spec,
            "reference_file": data["reference_file"],
            "reference_sha256": data["reference_sha256"],
            "script_file": "scripts/polish_shadow_notches.py",
            "script_sha256": sha256(Path(__file__)),
            "output_sha256": sha256(output),
            "mask_file": str(mask_path.relative_to(ROOT)) if mask_path.is_relative_to(ROOT) else str(mask_path),
            "mask_sha256": sha256(mask_path),
            "size": list(image.size),
            "mode": image.mode,
            "verification": proof,
        })
        print(spec["id"], proof["changed_pixels"], sha256(output))
    (args.output / "recipes.json").write_text(json.dumps({"schema_version": 1, "edits": records}, indent=2) + "\n")


if __name__ == "__main__":
    main()
