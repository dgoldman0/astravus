"""Reproduce the author's approved, tightly bounded sprite iris correction.

Requires the original generated PNG identified by the recipe's source hash.
Only the selected pigment changes; pupil, catchlight and outside pixels must
remain identical. Source paintings are kept in generation/Git history, not
duplicated in the game distribution.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def retouch(source, recipe, output):
    assert hashlib.sha256(source.read_bytes()).hexdigest() == recipe["source_sha256"], "Wrong source painting"
    with Image.open(source) as picture:
        original = np.array(picture)
        mode, size = picture.mode, picture.size
    rgb = original[:, :, :3].astype(np.float64)
    coefficients = np.array([.2126, .7152, .0722])
    luma = rgb @ coefficients
    geometry = Image.new("L", size, 0)
    protect = Image.new("L", size, 0)
    gd, pd = ImageDraw.Draw(geometry), ImageDraw.Draw(protect)
    for eye in recipe["mask_geometry"]:
        gd.polygon([tuple(p) for p in eye["ring"]], fill=255)
        pd.polygon([tuple(p) for p in eye["pupil"]], fill=255)
        pd.ellipse(eye["highlight"], fill=255)
    geo, protected = np.array(geometry) > 0, np.array(protect) > 0
    weight = (np.clip((rgb[:, :, 1] - rgb[:, :, 0] - 2.) / 12., 0., 1.)
              * np.clip((luma - 18.) / 12., 0., 1.) * geo * ~protected * (luma < 155.))
    chromaticity = np.array(recipe["operation"]["target_chromaticity_rgb"])
    target = (luma[:, :, None] * recipe["operation"]["luminance_multiplier"]
              * chromaticity / (chromaticity @ coefficients))
    result = original.copy()
    result[:, :, :3] = np.rint(np.clip(rgb * (1. - weight[:, :, None])
                                      + target * weight[:, :, None], 0, 255)).astype(np.uint8)
    changed = np.any(result != original, axis=2)
    assert np.array_equal(original[weight == 0], result[weight == 0]), "Outside-mask pixels changed"
    assert np.array_equal(original[protected], result[protected]), "Protected pixels changed"
    assert int(changed.sum()) == recipe["verification"]["changed_pixels"], "Changed-pixel count differs"
    Image.fromarray(result, mode).save(output)
    assert hashlib.sha256(output.read_bytes()).hexdigest() == recipe["output_sha256"], "Output differs from reviewed correction"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("id", help="Entry in docs/iris-retouches.json")
    parser.add_argument("source", type=Path, help="Original generated PNG")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    register = Path(__file__).resolve().parents[1] / "docs/iris-retouches.json"
    recipe = next(r for r in json.loads(register.read_text())["retouches"] if r["id"] == args.id)
    retouch(args.source, recipe, args.output)
    print("Verified exact reproduction; all outside-mask, pupil and catchlight pixels unchanged.")
