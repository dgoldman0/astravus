"""Analyze native GIMP output; this script does not create or edit image pixels."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
KEYS = ROOT / "../development/visual-novel/art/characters"
AUDIT = Path(sys.argv[1])

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def pixels(path):
    with Image.open(path) as image:
        assert image.mode in ("RGB", "L"), (path, image.mode)
        return np.asarray(image).copy()

records = []
for name in ("lyra", "thalia"):
    folder = KEYS / name
    original = pixels(folder / "sprite-original.png")
    final = pixels(folder / "sprite-refined.png")
    assert original.shape == final.shape
    union = np.zeros(original.shape[:2], dtype=bool)
    masks = []
    for path in sorted(folder.glob("mask-*.png")):
        values = pixels(path)
        assert values.shape == original.shape[:2]
        support = values > 0
        union |= support
        ys, xs = np.where(support)
        masks.append({"file": str(path.relative_to(ROOT)), "sha256": sha(path),
                      "support_bbox": [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1],
                      "nonzero_pixels": int(support.sum())})
    changed = np.any(original != final, axis=2)
    outside = int((changed & ~union).sum())
    reopened = pixels(AUDIT / f"{name}-reopened.png")
    restored = pixels(AUDIT / f"{name}-restored.png")
    assert outside == 0, (name, outside)
    assert np.array_equal(final, reopened), name
    assert np.array_equal(original, restored), name
    # Every confidently green source pixel is preserved by these face-only edits.
    green = (original[:, :, 1].astype(int) > original[:, :, 0].astype(int) + 55) & (original[:, :, 1].astype(int) > original[:, :, 2].astype(int) + 55)
    assert not np.any(changed & green), name
    records.append({"character": name, "source_file": str((folder / "sprite-original.png").relative_to(ROOT)),
                    "source_sha256": sha(folder / "sprite-original.png"),
                    "final_file": str((folder / "sprite-refined.png").relative_to(ROOT)),
                    "final_sha256": sha(folder / "sprite-refined.png"),
                    "xcf_file": str((folder / "sprite-refined.xcf").relative_to(ROOT)),
                    "xcf_sha256": sha(folder / "sprite-refined.xcf"),
                    "size": [original.shape[1], original.shape[0]], "mode": "RGB", "masks": masks,
                    "changed_pixels": int(changed.sum()), "outside_mask_changed_pixels": outside,
                    "chroma_backing_unchanged": True, "xcf_reopened_matches_final": True,
                    "hidden_layers_restore_original": True})

report = {"schema_version": 1, "tool": "GIMP 2.10.36 Script-Fu",
          "script_file": "scripts/refine_supporting_sprites.scm",
          "script_sha256": sha(ROOT / "scripts/refine_supporting_sprites.scm"),
          "status": "passed", "assets": records,
          "limitation": "Checks establish bounded native edits and editability, not artistic approval."}
(KEYS / "supporting-verification.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"status": "passed", "assets": [{"name": r["character"], "changed_pixels": r["changed_pixels"], "outside_mask_changed_pixels": 0} for r in records]}, indent=2))
