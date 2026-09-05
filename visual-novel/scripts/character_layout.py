"""Measure sprite silhouettes and check the reviewed standing-character scale."""
from pathlib import Path
import argparse
import hashlib
import json

from PIL import Image, ImageChops

PROJECT = Path(__file__).resolve().parents[1]


def measure(path):
    with Image.open(path) as image:
        if image.mode == "RGBA":
            mask = image.getchannel("A").point(lambda value: 255 if value >= 128 else 0)
        else:
            red, green, blue = image.convert("RGB").split()
            dominance = ImageChops.subtract(green, ImageChops.lighter(red, blue))
            mask = dominance.point(lambda value: 255 if value <= 38 else 0)
        bounds = mask.getbbox()
        assert bounds, f"Empty character silhouette: {path}"
        return list(image.size), list(bounds)


def check():
    data = json.loads((PROJECT / "game/character_layout.json").read_text())
    assert data["schema_version"] == 1
    actors = data["actors"]
    files = {path.relative_to(PROJECT / "game").as_posix()
             for path in (PROJECT / "game/images/characters").rglob("*.png")}
    assert set(actors) == files, "Every human sprite needs reviewed framing"
    for name, item in actors.items():
        path = PROJECT / "game" / name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"], f"Character framing needs review: {name}"
        size, bounds = measure(path)
        assert size == item["size"] and bounds == item["bounds"], f"Character silhouette changed: {name}"
        assert 0.99 <= item["sampling_scale"] <= 1.02, f"Unexpected sampling correction: {name}"
        assert item["group"] in data["heights"], f"Unknown character/age group: {name}"
    heights = data["heights"]
    for age in ("early", "later"):
        assert heights["lyra"] < heights[f"calista_{age}"] <= heights[f"cassia_{age}"] < heights[f"joren_{age}"]
        assert heights[f"cassia_{age}"] - heights[f"calista_{age}"] <= 15
    assert heights["joren_early"] < heights["kael"]
    for name in ("calista", "cassia", "joren"):
        assert heights[name + "_later"] > heights[name + "_early"]
    print(f"Character framing passed: {len(actors)} measured silhouettes; one height per character/age and a shared foot baseline.")


def check_renders(directory):
    data = json.loads((PROJECT / "game/character_layout.json").read_text())
    groups = {}
    measured = {}
    for name, item in data["actors"].items():
        path = directory / (Path(name).stem + ".png")
        with Image.open(path) as image:
            assert image.mode == "RGBA", f"Missing rendered alpha: {path}"
            bounds = image.getchannel("A").point(lambda value: 255 if value >= 128 else 0).getbbox()
        assert bounds, f"Missing rendered body: {path}"
        height = bounds[3] - bounds[1]
        assert abs(height - data["heights"][item["group"]]) <= 3, (name, bounds, "incorrect visible height")
        assert abs(bounds[3] - data["foot_y"]) <= 2, (name, bounds, "feet off baseline")
        groups.setdefault(item["group"], []).append(height)
        measured[name] = {"bounds": bounds, "visible_height": height, "feet_y": bounds[3]}
    for group, heights in groups.items():
        assert max(heights) - min(heights) <= 3, (group, heights, "wardrobe/pose changes body height")
    (directory / "measurements.json").write_text(json.dumps(measured, indent=2) + "\n")
    print(f"Rendered framing passed: {len(measured)} native silhouettes, wardrobe heights within 3px, feet within 2px of shared baseline.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--renders", type=Path)
    args = parser.parse_args()
    check()
    if args.renders:
        check_renders(args.renders)
