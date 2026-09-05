"""Stage two source-backed work-surface state variants from immutable sources.

The original room stays pixel-identical outside explicit material masks. No runtime
asset is changed by this command. See docs/environment-state-spec.json.
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


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build/graphics-polish/environment-state")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    specs = json.loads((ROOT / "docs/environment-state-spec.json").read_text())
    records = []
    for spec in specs["assets"]:
        original = subprocess.check_output(["git", "cat-file", "blob", spec["source_git_blob"]], cwd=ROOT)
        assert hashlib.sha256(original).hexdigest() == spec["source_sha256"]
        base = Image.open(io.BytesIO(original))
        assert base.mode == "RGB"
        material_path = ROOT / spec["material_file"]
        assert sha(material_path) == spec["material_sha256"]
        material = Image.open(material_path).convert("RGB")
        left, top, right, bottom = spec["material_target_box"]
        material = material.resize((right-left, bottom-top), Image.Resampling.LANCZOS)
        donor = base.copy()
        donor.paste(material, (left, top))
        mask = Image.new("L", base.size)
        ImageDraw.Draw(mask).polygon(spec["polygon"], fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(spec["feather_pixels"]))
        mask_array = np.asarray(mask).copy()
        inside = np.zeros(mask_array.shape, dtype=bool)
        inside[top:bottom, left:right] = True
        mask_array[~inside] = 0
        mask = Image.fromarray(mask_array)
        result = Image.composite(donor, base, mask)
        changed = np.any(np.asarray(result) != np.asarray(base), axis=2)
        assert not np.any(changed & (mask_array == 0))
        ys, xs = np.where(changed)
        out = args.output / (spec["id"] + ".png")
        mask_path = args.output / (spec["id"] + "-mask.png")
        result.save(out)
        mask.save(mask_path)
        record = {**spec, "script_file": "scripts/render_environment_states.py",
                  "script_sha256": sha(Path(__file__)), "output_sha256": sha(out),
                  "mask_sha256": sha(mask_path), "size": list(base.size), "mode": base.mode,
                  "verification": {"changed_pixels": int(changed.sum()),
                    "outside_mask_pixels_changed": 0, "canvas_and_mode_unchanged": True,
                    "change_bbox": [int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1]}}
        records.append(record)
        print(spec["id"], record["output_sha256"], record["verification"])
    (args.output / "recipes.json").write_text(json.dumps({"schema_version": 1, "edits": records}, indent=2)+"\n")


if __name__ == "__main__":
    main()
