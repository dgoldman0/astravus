"""Reproduce the bounded pond-bank correction without repainting the cast."""
import hashlib
import io
import json
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    spec = json.loads((ROOT / "docs/pond-comfort-grade.json").read_text())
    original = subprocess.check_output(
        ["git", "cat-file", "blob", spec["source_git_blob"]], cwd=ROOT
    )
    assert digest(original) == spec["source_sha256"]
    material_bytes = (ROOT / spec["material_file"]).read_bytes()
    assert digest(material_bytes) == spec["material_sha256"]
    base = Image.open(io.BytesIO(original)).convert("RGB")
    layer = Image.open(io.BytesIO(material_bytes)).convert("RGBA")
    assert layer.size == base.size == (1672, 941)
    alpha = layer.getchannel("A")
    result = Image.composite(layer.convert("RGB"), base, alpha)
    changed = np.any(np.asarray(result) != np.asarray(base), axis=2)
    assert not np.any(changed & (np.asarray(alpha) == 0))
    # Heads/faces and the full foreground remain the exact accepted painting.
    for box in [(285, 154, 514, 701), (592, 147, 805, 337),
                (744, 325, 927, 493), (1085, 154, 1214, 336),
                (1301, 392, 1498, 747), (0, 425, 1672, 941)]:
        assert np.array_equal(np.asarray(base.crop(box)), np.asarray(result.crop(box))), box
    out = ROOT / "../development/visual-novel/archive/local/graphics-workspace/pond"
    out.mkdir(parents=True, exist_ok=True)
    target = out / "pond-comfort.png"
    result.save(target)
    alpha.save(out / "pond-comfort-mask.png")
    ys, xs = np.where(changed)
    report = {**spec, "script_file": "scripts/repair_pond_comfort_grade.py",
              "script_sha256": digest(Path(__file__).read_bytes()),
              "output_sha256": digest(target.read_bytes()),
              "verification": {"changed_pixels": int(changed.sum()),
                               "outside_mask_pixels_changed": 0,
                               "protected_portrait_and_foreground_boxes_unchanged": True,
                               "canvas_size": list(base.size),
                               "change_bbox": [int(xs.min()), int(ys.min()),
                                               int(xs.max()) + 1, int(ys.max()) + 1]}}
    (out / "comfort-recipe.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report["verification"]))


if __name__ == "__main__":
    main()
