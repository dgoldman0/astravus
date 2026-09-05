"""Reproduce reviewed, author-authorized iris color edits without regeneration.

Each recipe binds an exact source PNG hash to manually reviewed iris polygons,
pupil/catchlight exclusions, and fixed color/luminance operations. Requires
Pillow and NumPy. No automatic eye detection or whole-picture correction occurs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def retouch(source, recipe, output, mask_output=None):
    source, output = Path(source), Path(output)
    if file_sha256(source) != recipe["source_sha256"]:
        raise ValueError("Source hash differs from the reviewed painting")
    with Image.open(source) as picture:
        original = np.array(picture)
        mode, size = picture.mode, picture.size
    if mode not in ("RGB", "RGBA"):
        raise ValueError("Only RGB/RGBA source PNGs are supported")
    rgb = original[:, :, :3].astype(np.float64)
    operation = recipe["operation"]
    coefficients = np.array(operation["luminance_coefficients"], dtype=np.float64)
    luma = rgb @ coefficients
    result_rgb = rgb.copy()
    support = np.zeros(original.shape[:2], dtype=bool)
    protected_all = np.zeros_like(support)
    total_weight = np.zeros_like(luma)
    eyes = []
    for eye in recipe["mask_geometry"]:
        geometry = Image.new("L", size, 0)
        protected_image = Image.new("L", size, 0)
        ImageDraw.Draw(geometry).polygon([tuple(p) for p in eye["ring"]], fill=255)
        pd = ImageDraw.Draw(protected_image)
        if eye.get("pupil"):
            pd.polygon([tuple(p) for p in eye["pupil"]], fill=255)
        for highlight in eye.get("highlights", []):
            pd.ellipse(highlight, fill=255)
        for shape in eye.get("protected_polygons", []):
            pd.polygon([tuple(p) for p in shape], fill=255)
        geo = np.array(geometry) > 0
        protected = np.array(protected_image) > 0
        palette = operation["palettes"][eye["palette"]]
        gate = palette["source_chroma_gate"]
        # Chroma gates exclude warm lids/skin at the edge of the hand mask.
        gate_signal = (rgb @ np.array(gate["rgb_coefficients"], dtype=np.float64)
                       - gate["offset"])
        color_weight = np.clip(gate_signal / gate["ramp"], 0., 1.)
        shadow = palette["shadow_gate"]
        shadow_weight = np.clip((luma - shadow["floor"]) / shadow["ramp"], 0., 1.)
        weight = (color_weight * shadow_weight * geo * ~protected
                  * (luma < palette["maximum_source_luminance"]))
        allowed = weight > 0
        if np.any(support & allowed):
            raise ValueError("Eye masks overlap; review geometry before retouching")
        chromaticity = np.array(palette["target_chromaticity_rgb"], dtype=np.float64)
        target = (luma[:, :, None] * palette["luminance_multiplier"]
                  * chromaticity / (chromaticity @ coefficients))
        result_rgb = np.where(allowed[:, :, None],
                              rgb * (1. - weight[:, :, None]) + target * weight[:, :, None],
                              result_rgb)
        support |= allowed
        total_weight = np.maximum(total_weight, weight)
        protected_all |= protected
        eyes.append({"character": eye["character"], "palette": eye["palette"],
                     "allowed_pixels": int(allowed.sum())})
    result = original.copy()
    result[:, :, :3] = np.rint(np.clip(result_rgb, 0, 255)).astype(np.uint8)
    changed = np.any(result != original, axis=2)
    if not np.array_equal(original[~support], result[~support]):
        raise ValueError("Pixels outside the reviewed mask changed")
    if not np.array_equal(original[protected_all], result[protected_all]):
        raise ValueError("Protected pupil/catchlight pixels changed")
    if int(changed.sum()) > original.shape[0] * original.shape[1] * .005:
        raise ValueError("Iris correction exceeded 0.5% of the image")
    output.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(result).save(output)
    output_sha256 = file_sha256(output)
    if recipe.get("output_sha256") and output_sha256 != recipe["output_sha256"]:
        raise ValueError("Output differs from the reviewed result")
    ys, xs = np.where(changed)
    change_bbox = ([int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
                   if len(xs) else None)
    verification = {
        "changed_pixels": int(changed.sum()), "change_bbox": change_bbox,
        "outside_mask_pixels_changed": 0,
        "protected_pupil_and_highlight_pixels_changed": 0,
        "outside_mask_identical": True, "canvas_and_mode_unchanged": True,
        "eyes": eyes,
    }
    expected = recipe.get("verification", {}).get("changed_pixels")
    if expected is not None and expected != verification["changed_pixels"]:
        raise ValueError("Changed-pixel count differs from the reviewed result")
    if mask_output:
        Image.fromarray(np.rint(total_weight * 255).astype(np.uint8)).save(mask_output)
    return {"output_sha256": output_sha256, "verification": verification,
            "mode": mode, "size": list(size)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("id", help="Retouch recipe ID")
    parser.add_argument("source", type=Path, help="Exact original generated PNG")
    parser.add_argument("output", type=Path)
    parser.add_argument("--recipes", type=Path,
                        default=Path(__file__).resolve().parents[1] / "docs/iris-retouches.json")
    parser.add_argument("--mask-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()
    register = json.loads(args.recipes.read_text())
    records = register["retouches"] if isinstance(register, dict) else register
    recipe = next(r for r in records if r["id"] == args.id)
    result = retouch(args.source, recipe, args.output, args.mask_output)
    if args.report_output:
        args.report_output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
