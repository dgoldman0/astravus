"""Apply explicitly bounded character geometry/color edits from original Git pixels.

The local inverse warp moves lid, sclera and iris together; it is not an iris-only
correction. It never scales a body, changes a silhouette or resamples a full frame.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/character-geometry-spec.json"
OUT = ROOT / "../development/visual-novel/archive/local/graphics-workspace/characters"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def edit(source, item):
    image = np.array(source.convert("RGB"))
    rgb = image.astype(np.float64)
    yy, xx = np.mgrid[:image.shape[0], :image.shape[1]]
    support = np.zeros(xx.shape, dtype=bool)
    for eye in item.get("iris_color", []):
        cx, cy = eye["center"]
        rx, ry = eye["radius"]
        ellipse = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1
        red, green, blue = rgb.transpose(2, 0, 1)
        luma = rgb @ np.array([.2126, .7152, .0722])
        weight = ellipse * np.clip((green - .60 * red) / 15, 0, 1)
        weight *= np.clip((green - blue - 6) / 15, 0, 1)
        weight *= np.clip((luma - 30) / 25, 0, 1) * (luma < 185)
        px, py, prx, pry = eye["pupil"]
        pupil = ((xx - px) / prx) ** 2 + ((yy - py) / pry) ** 2 <= 1
        weight[pupil] = 0
        chroma = np.array([.32, .57, .24])
        target = luma[..., None] * .79 * chroma / (chroma @ [.2126, .7152, .0722])
        rgb = rgb * (1 - weight[..., None]) + target * weight[..., None]
        support |= weight > 0
    colored = np.rint(np.clip(rgb, 0, 255)).astype(np.uint8)
    map_x, map_y = xx.astype(np.float32), yy.astype(np.float32)
    geometry_support = np.zeros(xx.shape, dtype=bool)
    for eye in item.get("eye_geometry", []):
        cx, cy = eye["center"]
        rx, ry = eye["radius"]
        sx, sy = eye["scale"]
        distance = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
        t = np.clip((distance - .62) / .38, 0, 1)
        weight = 1 - t * t * (3 - 2 * t)
        map_x += ((xx - cx) * (1 / sx - 1) * weight).astype(np.float32)
        map_y += ((yy - cy) * (1 / sy - 1) * weight).astype(np.float32)
        geometry_support |= distance < 1
    result = colored.copy()
    if geometry_support.any():
        sampled = cv2.remap(colored, map_x, map_y, cv2.INTER_LANCZOS4,
                            borderMode=cv2.BORDER_REFLECT_101)
        result[geometry_support] = sampled[geometry_support]
    support |= geometry_support
    changed = np.any(result != image, axis=2)
    assert not np.any(changed & ~support), "Pixels outside declared edit regions changed"
    y, x = np.where(changed)
    output = Image.fromarray(result)
    return output, {
        "changed_pixels": int(changed.sum()),
        "outside_mask_pixels_changed": 0,
        "outside_mask_identical": True,
        "canvas_and_mode_unchanged": source.size == output.size and source.mode == output.mode,
        "change_bbox": [int(x.min()), int(y.min()), int(x.max()) + 1, int(y.max()) + 1],
        "operation_scope": "Lid, iris and surrounding skin move together inside eye geometry regions; pigment masks do not move pixels.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="*")
    args = parser.parse_args()
    spec = json.loads(SPEC.read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for item in spec["assets"]:
        if args.ids and item["id"] not in args.ids:
            continue
        data = subprocess.check_output(["git", "cat-file", "blob", item["source_git_blob"]], cwd=ROOT)
        assert digest(data) == item["source_sha256"], item["id"]
        source = Image.open(io.BytesIO(data))
        output, verification = edit(source, item)
        path = OUT / Path(item["file"]).name
        output.save(path)
        record = {**item, "script_file": "scripts/polish_character_geometry.py",
                  "script_sha256": digest(Path(__file__).read_bytes()),
                  "output_sha256": digest(path.read_bytes()), "size": list(output.size),
                  "mode": output.mode, "verification": verification}
        records.append(record)
        print(item["id"], verification["changed_pixels"], record["output_sha256"])
    (OUT / "recipes.json").write_text(json.dumps({"schema_version": 1, "edits": records}, indent=2) + "\n")


if __name__ == "__main__":
    main()
