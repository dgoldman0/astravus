#!/usr/bin/env python3
"""Compose selected treehouse backgrounds from one immutable painted room.

No synthesis or image resampling is used. Existing painted paper details are
copied at their original coordinates; weather is clipped to exterior openings.
Source paintings live in Git, not duplicated runtime assets. Default writes
review candidates; --install also updates the three owned runtime backgrounds.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import random
import subprocess
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
SIZE = (1672, 941)
SOURCES = {
    "room": {"file": "game/images/backgrounds/treehouse-shaded.png", "git_blob": "2f20bf3619bbc3c7548a118b0f6399ede8207edd", "sha256": "9dcbc10785238d2c964cbc32b24451e63f8228173270c052394d8fe8bc74dda9"},
    "papers": {"file": "game/images/backgrounds/book-one/treehouse-memory.png", "git_blob": "6a25df91b9207d27b863976baf0313c2152f9289", "sha256": "f90215045bf2a4c2262f9f18cda26b3cd98a4e5ad02ee2c668975e19c4802913"},
}

# Coordinates follow the painted paper edges, including their existing tiny
# contact shadows. These drawings depict generic people / imaginary adventures.
# The later waterwheel drawing is deliberately not in EARLY_PAPERS.
EARLY_PAPERS = [
    [[9, 73], [96, 84], [109, 187], [24, 194]],
    [[18, 211], [151, 210], [155, 298], [30, 306]],
    [[187, 148], [276, 169], [278, 245], [179, 225]],
    [[311, 141], [377, 141], [379, 223], [314, 224]],
    [[458, 196], [518, 189], [527, 246], [448, 251]],
]
LATER_PAPERS = [
    [[40, 323], [164, 313], [177, 395], [48, 407]],
    [[175, 292], [209, 294], [210, 355], [176, 358]],
    [[201, 250], [270, 248], [271, 320], [213, 327]],
    [[280, 179], [312, 176], [312, 226], [278, 231]],
    [[292, 228], [334, 222], [339, 300], [290, 301]],
    [[338, 223], [383, 220], [391, 310], [340, 315]],
    [[378, 179], [403, 180], [402, 264], [383, 262]],
    [[304, 300], [339, 301], [337, 371], [311, 377]],
    [[82, 430], [204, 413], [217, 507], [91, 527]],
    [[226, 340], [312, 340], [320, 443], [229, 451]],
    [[805, 157], [876, 151], [876, 209], [808, 216]],
    [[817, 217], [874, 212], [878, 262], [818, 266]],
]
# The table's surface receives remembrance drawings. Its edge, legs, cups and
# surrounding cushions remain the selected room. Cups are restored explicitly.
TABLE_PAPERS = [[[865, 659], [914, 638], [1006, 632], [1141, 660], [1219, 701], [1326, 736], [1287, 796], [1102, 809], [901, 772], [856, 708]]]
CUPS = [[[1026, 610], [1077, 612], [1077, 657], [1032, 656]], [[1081, 619], [1131, 620], [1131, 667], [1083, 666]], [[1035, 740], [1090, 741], [1093, 796], [1040, 796]]]

# Open-air regions only: inside edges of curtains, door frame, rail top and
# individual railing gaps. The protected posts/rails/curtains are never weathered.
OPENINGS = [
    [[583, 258], [594, 240], [610, 237], [630, 251], [634, 337], [584, 335]],
    [[720, 247], [745, 211], [759, 245], [776, 278], [806, 322], [823, 343], [700, 341]],
    [[952, 199], [981, 177], [1037, 160], [1114, 153], [1232, 140], [1324, 129], [1328, 194], [1330, 279], [1329, 355], [1302, 373], [1260, 383], [966, 360], [936, 346], [936, 220]],
    [[1418, 212], [1450, 161], [1495, 121], [1554, 96], [1671, 68], [1671, 402], [1400, 378], [1407, 299]],
    [[702, 360], [735, 361], [739, 414], [714, 421]],
    [[755, 364], [795, 366], [793, 429], [769, 427], [763, 408]],
    [[810, 369], [822, 368], [814, 436], [806, 433]],
    [[944, 377], [983, 381], [981, 463], [962, 457], [947, 442]],
    [[1006, 386], [1039, 388], [1049, 481], [1004, 474]],
    [[1076, 391], [1114, 394], [1108, 483], [1081, 482]],
    [[1134, 397], [1182, 401], [1172, 495], [1136, 491]],
    [[1203, 401], [1244, 401], [1242, 506], [1196, 501]],
    [[1265, 402], [1302, 391], [1299, 438], [1270, 489], [1261, 491]],
    [[1402, 406], [1438, 409], [1417, 486], [1400, 482]],
    [[1463, 414], [1484, 416], [1494, 518], [1440, 511]],
    [[1503, 417], [1540, 420], [1550, 534], [1516, 528]],
    [[1573, 423], [1611, 426], [1598, 548], [1573, 542]],
    [[1643, 429], [1671, 430], [1671, 500], [1632, 554], [1623, 551]],
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source_images():
    result = {}
    for name, spec in SOURCES.items():
        raw = subprocess.check_output(["git", "cat-file", "blob", spec["git_blob"]], cwd=REPO)
        assert sha(raw) == spec["sha256"], f"Immutable source mismatch: {name}"
        result[name] = Image.open(io.BytesIO(raw)).convert("RGB")
        assert result[name].size == SIZE
    return result


def mask(polygons, feather=1.0):
    result = Image.new("L", SIZE)
    draw = ImageDraw.Draw(result)
    for polygon in polygons:
        draw.polygon([tuple(point) for point in polygon], fill=255)
    return result.filter(ImageFilter.GaussianBlur(feather)) if feather else result


def rgba(source, alpha):
    result = source.convert("RGBA")
    result.putalpha(alpha)
    return result


def compose(base, *layers):
    result = base.convert("RGBA")
    for layer in layers:
        result = Image.alpha_composite(result, layer)
    return result.convert("RGB")


def rain_layer(openings):
    # Fixed-seed, antialiased streaks have varied lengths, depths and opacity;
    # existing canopy pixels remain behind them. No fake pane or interior rain.
    scale = 3
    rain = Image.new("RGBA", (SIZE[0] * scale, SIZE[1] * scale))
    draw = ImageDraw.Draw(rain)
    rng = random.Random(260905)
    for _ in range(4400):
        x, y = rng.uniform(570, SIZE[0]), rng.uniform(55, 574)
        length = rng.uniform(5.0, 22.0)
        opacity = rng.randrange(9, 41)
        draw.line((int(x*scale), int(y*scale), int((x-1.5)*scale), int((y+length)*scale)), fill=(160, 187, 192, opacity), width=scale if length > 17 else 2)
    rain = rain.resize(SIZE, Image.Resampling.LANCZOS)
    rain.putalpha(Image.fromarray((np.asarray(rain.getchannel("A"), dtype=np.float32) * np.asarray(openings, dtype=np.float32)/255).astype(np.uint8)))
    return rain


def save_xcf(layer_dir, out):
    """Use installed GIMP to preserve the five actual editable layers."""
    base = str(layer_dir / "01-selected-room.png")
    lines = [f'(let* ((img (car (gimp-file-load RUN-NONINTERACTIVE {json.dumps(base)} {json.dumps(base)}))) (base (car (gimp-image-get-active-layer img))))', '(gimp-item-set-name base "01 Selected dry room — immutable painting")']
    for name in ["02-early-drawings", "03-exterior-rain", "04-remembrance-wall-drawings", "05-remembrance-table-drawings"]:
        file = json.dumps(str(layer_dir / (name + ".png")))
        lines.append(f'(let ((layer (car (gimp-file-load-layer RUN-NONINTERACTIVE img {file})))) (gimp-image-insert-layer img layer 0 0) (gimp-item-set-name layer {json.dumps(name)}))')
    destination = json.dumps(str(out / "treehouse-room.xcf"))
    lines.extend([f'(gimp-xcf-save RUN-NONINTERACTIVE img (car (gimp-image-get-active-layer img)) {destination} {destination})', '(gimp-image-delete img))', '(gimp-quit 0)'])
    import os
    with tempfile.TemporaryDirectory(prefix="astravus-environment-gimp-") as temporary:
        scheme = Path(temporary) / "layers.scm"
        scheme.write_text("\n".join(lines) + "\n")
        env = dict(os.environ, GIMP2_DIRECTORY=str(Path(temporary) / "gimp-profile"))
        subprocess.run(["gimp", "--no-interface", "--new-instance", "--no-data", "--no-fonts", "--no-splash", "--no-shm", "--console-messages", "--batch-interpreter=plug-in-script-fu-eval", "--batch", f'(load {json.dumps(str(scheme))})'], env=env, check=True, timeout=90)
    assert (out / "treehouse-room.xcf").is_file()


def run(install, xcf):
    sources = source_images()
    room, papers = sources["room"], sources["papers"]
    early_mask = mask(EARLY_PAPERS, .7)
    late_mask = mask(LATER_PAPERS, .7)
    table_mask = mask(TABLE_PAPERS, 1.0)
    cup_mask = mask(CUPS, 1.4)
    table_mask = Image.fromarray((np.asarray(table_mask, dtype=np.float32)*(1-np.asarray(cup_mask, dtype=np.float32)/255)).astype(np.uint8))
    # Keep rain well inside architectural silhouettes; no feather beyond frame.
    openings = mask(OPENINGS, 0).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.5))
    early = rgba(papers, early_mask)
    late = rgba(papers, late_mask)
    table = rgba(papers, table_mask)
    rain = rain_layer(openings)
    dry = compose(room, early)
    wet = compose(room, early, rain)
    memory = compose(room, early, rain, late, table)
    out = PROJECT / "build/graphics/environments"
    out.mkdir(parents=True, exist_ok=True)
    layers = {"01-selected-room": room, "02-early-drawings": early, "03-exterior-rain": rain, "04-remembrance-wall-drawings": late, "05-remembrance-table-drawings": table}
    layer_dir = out / "layers"
    layer_dir.mkdir(exist_ok=True)
    for name, picture in layers.items():
        picture.save(layer_dir / (name + ".png"))
    if xcf:
        save_xcf(layer_dir, out)
    outputs = [
        ("treehouse-early-drawings", "game/images/backgrounds/treehouse-shaded.png", "treehouse-shaded-v1", dry, [early_mask], ["same-coordinate existing early wall drawings"]),
        ("treehouse-rain-shared-room", "game/images/backgrounds/treehouse-rain.png", "treehouse-rain-v1", wet, [early_mask, rain.getchannel("A")], ["same-coordinate existing early wall drawings", "seeded exterior rain through explicit openings"]),
        ("treehouse-memory-shared-room", "game/images/backgrounds/book-one/treehouse-memory.png", "book-one-treehouse-memory-v1", memory, [early_mask, rain.getchannel("A"), late_mask, table_mask], ["same-coordinate existing early wall drawings", "same exterior rain", "existing later wall and table drawings; cups protected"]),
    ]
    recipes = []
    for id_, file, generation, picture, masks, operations in outputs:
        destination = out / Path(file).name
        picture.save(destination)
        if install:
            (PROJECT / file).write_bytes(destination.read_bytes())
        union = np.maximum.reduce([np.asarray(item) for item in masks]) > 0
        changed = np.any(np.asarray(room) != np.asarray(picture), axis=2)
        outside = int(np.count_nonzero(changed & ~union))
        assert outside == 0
        recipe = {
            "id": id_, "file": file, "source_generation": generation,
            "sources": list(SOURCES.values()),
            "base_source": "room", "sources_by_name": SOURCES,
            "operations": operations,
            "mask_geometry": {"early_papers": EARLY_PAPERS, "later_papers": LATER_PAPERS if id_.endswith("shared-room") and "memory" in id_ else [], "table_papers": TABLE_PAPERS if "memory" in id_ else [], "protected_cups": CUPS if "memory" in id_ else [], "exterior_openings": OPENINGS if "rain" in id_ or "memory" in id_ else [], "paper_feather_px": .7, "rain_seed": 260905},
            "output_sha256": sha(destination.read_bytes()), "dimensions": list(SIZE), "mode": "RGB",
            "script_file": "scripts/repair_treehouse_environments.py", "script_sha256": sha(Path(__file__).read_bytes()),
            "verification": {"baseline": SOURCES["room"]["sha256"], "changed_pixels": int(np.count_nonzero(changed)), "outside_mask_pixels_changed": outside, "outside_mask_identical": outside == 0, "canvas_and_mode_unchanged": picture.size == room.size and picture.mode == room.mode, "geometry_resampled": False, "dry_vs_rain_outside_weather_identical": bool(np.array_equal(np.asarray(dry)[np.asarray(rain.getchannel('A'))==0], np.asarray(wet)[np.asarray(rain.getchannel('A'))==0]))},
        }
        recipes.append(recipe)
    register_path = PROJECT / "docs/environment-edits.json"
    owned = {recipe["id"] for recipe in recipes}
    prior = json.loads(register_path.read_text()).get("edits", []) if register_path.exists() else []
    register = {"schema_version": 1, "method": "Deterministic masked composition from immutable selected paintings; human appearance review separate from pixel checks.", "edits": recipes + [recipe for recipe in prior if recipe["id"] not in owned]}
    register_path.write_text(json.dumps(register, indent=2) + "\n")
    print(json.dumps({"installed": install, "outputs": [{"file": r["file"], "sha256": r["output_sha256"], "changed_pixels": r["verification"]["changed_pixels"]} for r in recipes]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--xcf", action="store_true", help="Also save a five-layer editable GIMP project")
    arguments = parser.parse_args()
    run(arguments.install, arguments.xcf)
