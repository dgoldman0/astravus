"""Verify the native Sage iris edit without changing artwork."""
from pathlib import Path
import hashlib
import json
import sys

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = next(parent for parent in HERE.parents if (parent / "visual-novel/game").is_dir())
sys.path.insert(0, str(ROOT / "visual-novel/scripts"))
from character_layout import measure


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pixels(name, mode="RGB"):
    return np.asarray(Image.open(HERE / name).convert(mode))


def bounds(mask):
    yy, xx = np.where(mask)
    return [int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1] if len(xx) else None


def linear_luminance(rgb):
    value = rgb.astype(float) / 255
    value = np.where(value <= .04045, value / 12.92, ((value + .055) / 1.055) ** 2.4)
    return value @ np.array([.2126, .7152, .0722])


before = pixels("sprite-before.png")
after = pixels("sprite-refined.png")
mask = pixels("mask-irises.png", "L") > 0
protected = pixels("mask-protected-pupils-highlights.png", "L") > 0
changed = np.any(before != after, axis=2)
assert before.shape == after.shape == (1537, 1023, 3)
assert int(changed.sum()) == 77
assert not np.any(changed & ~mask)
assert not np.any(changed & protected)
assert np.array_equal(pixels("prior-xcf-flattened.png"), before)
assert np.array_equal(pixels("prior-restored.png"), before)
assert np.array_equal(pixels("xcf-reopened.png"), after)
assert measure(HERE / "sprite-before.png") == measure(HERE / "sprite-refined.png")

old_native = pixels("native-sage-before.png", "RGBA")
new_native = pixels("native-sage-after.png", "RGBA")
native_changed = np.any(old_native != new_native, axis=2)
assert np.array_equal(old_native[:, :, 3], new_native[:, :, 3])
assert 0 < native_changed.sum() < 200
native_bounds = bounds(native_changed)
assert 900 < native_bounds[0] < native_bounds[2] < 1020
assert 240 < native_bounds[1] < native_bounds[3] < 330
selected = ROOT / "visual-novel/game/images/characters/book-one/sage-everyday.png"
assert sha(selected) == sha(HERE / "sprite-refined.png")

files = sorted(path for path in HERE.iterdir() if path.is_file() and path.name != "verification.json")
report = {
    "status": "passed",
    "method": "GIMP 2.10.36 luminance desaturation on existing pigment at 80% layer opacity; two feathered iris masks; exact pupil/catchlight exclusion",
    "selected_file": selected.relative_to(ROOT).as_posix(),
    "source_sha256": sha(HERE / "sprite-before.png"),
    "selected_sha256": sha(selected),
    "mode": Image.open(selected).mode,
    "size": measure(selected)[0],
    "foreground_bounds": measure(selected)[1],
    "changed_pixels": int(changed.sum()),
    "changed_bounds": bounds(changed),
    "mask_nonzero_pixels": int(mask.sum()),
    "outside_mask_changed_pixels": int((changed & ~mask).sum()),
    "protected_pupil_catchlight_pixels": int(protected.sum()),
    "protected_changed_pixels": int((changed & protected).sum()),
    "all_other_pixels_exact": bool(np.array_equal(before[~mask], after[~mask])),
    "prior_xcf_flatten_matches_source": True,
    "new_xcf_reopening_matches_export": True,
    "hiding_new_layer_restores_source": True,
    "max_linear_luminance_delta_0_to_1": float(np.max(np.abs(linear_luminance(before)[changed] - linear_luminance(after)[changed]))),
    "native": {
        "suite": "global::character_framing_review",
        "runs": "fresh before and after, each passed 2 assertions",
        "capture_size": list(Image.open(HERE / "native-sage-after.png").size),
        "changed_pixels": int(native_changed.sum()),
        "changed_bounds": native_bounds,
        "alpha_exact": True,
        "review": "Both actual Ren'Py full-body renders inspected. Iris change is subtle at stage size; no luminous eyes, face/pose shift, or matte change. Enlarged GIMP source details establish the pigment correction more clearly."
    },
    "reproduction_script": "visual-novel/scripts/refine_sage_irises.scm",
    "reproduction_script_sha256": sha(ROOT / "visual-novel/scripts/refine_sage_irises.scm"),
    "prior_editable_source": "development/visual-novel/art/characters/sage/sprite-refined.xcf",
    "prior_editable_source_sha256": sha(HERE.parent / "sprite-refined.xcf"),
    "files": {path.name: sha(path) for path in files},
}
(HERE / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({key: report[key] for key in ("status", "selected_sha256", "size", "foreground_bounds", "changed_pixels", "outside_mask_changed_pixels", "protected_changed_pixels", "max_linear_luminance_delta_0_to_1", "native")}, indent=2))
