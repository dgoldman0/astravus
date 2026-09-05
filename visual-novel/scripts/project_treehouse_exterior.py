#!/usr/bin/env python3
"""Project a shared painted exterior rig into protected CG window openings.

Two nearby depth cards retain selected painted fork/trunk clusters while the
original CG's distant foliage remains untouched outside those local layers.
Coordinates are production assumptions, not measured architecture or lore.
Outputs are RGBA layers for final character composites; runtime CGs are untouched.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from repair_treehouse_environments import PROJECT, REPO, SIZE, SOURCES, OPENINGS, mask, source_images, sha

F = 1400.0
K = np.array([[F, 0, 836.0], [0, F, 470.5], [0, 0, 1]])

DEPTH_CARDS = [
    {"id": "central-fork-cluster", "depth": 7.0, "polygon": [[980, 216], [1041, 187], [1100, 163], [1256, 149], [1311, 218], [1300, 328], [1190, 370], [1042, 352], [972, 287]]},
    {"id": "right-fork-cluster", "depth": 8.5, "polygon": [[1441, 216], [1492, 177], [1572, 133], [1671, 107], [1671, 360], [1541, 367], [1430, 326]]},
]

VIEWS = {
    "treehouse-friends": {
        "lighting_source_blob": "a04d30ffc71701da7db81ec35a41c50bf2045eea",
        "production_camera_position": [-0.4423698224722742, 0.05749191486013303, 0.603102910125768],
        "lighting": "day",
        "room_anchors": [{"name": "main-bay inner upper edge", "master": [935, 215], "view": [1200, 105]}, {"name": "main-bay rail start", "master": [935, 355], "view": [1200, 317]}, {"name": "main-bay rail far end", "master": [1325, 385], "view": [1670, 334]}],
        "openings": [
            [[909, 99], [992, 78], [1007, 128], [1024, 182], [1048, 229], [1070, 266], [1065, 299], [961, 299], [951, 226], [933, 186], [910, 170]],
            [[1211, 99], [1261, 71], [1396, 24], [1461, 3], [1671, 3], [1671, 315], [1410, 314], [1403, 262], [1407, 211], [1382, 177], [1336, 145], [1274, 134], [1230, 141], [1200, 159]],
            [[1451, 350], [1506, 350], [1504, 438], [1475, 405]],
            [[1531, 350], [1579, 350], [1576, 491], [1538, 485]],
            [[1605, 351], [1671, 353], [1671, 500], [1600, 496]],
            [[1000, 330], [1048, 331], [1043, 366], [1020, 384], [1000, 359]],
        ],
    },
    "theme-treehouse-arrival": {
        "lighting_source_blob": "da135e66da1ce588a1ca2ed93f9614dde54851a3",
        "production_camera_position": [0.11311052538852173, 0.04214963014225322, 0.42430362207904226],
        "lighting": "day",
        "room_anchors": [{"name": "rear doorway crown (partly occluded)", "master": [602, 234], "view": [557, 143]}, {"name": "right post rail junction", "master": [1370, 392], "view": [1500, 393]}],
        "openings": [
            [[900, 119], [970, 113], [980, 163], [1001, 226], [1026, 272], [1049, 294], [1046, 338], [951, 336], [932, 283], [925, 230], [908, 188]],
            [[1356, 149], [1390, 119], [1480, 93], [1480, 387], [1395, 379], [1374, 329], [1346, 304], [1321, 280], [1311, 260], [1329, 213]],
            [[1605, 98], [1671, 95], [1671, 428], [1607, 409]],
            [[1620, 447], [1671, 460], [1671, 589], [1620, 579]],
            [[1432, 414], [1475, 417], [1475, 508], [1461, 505], [1446, 471]],
            [[983, 365], [1020, 366], [1018, 456], [983, 450]],
            [[548, 187], [568, 178], [587, 221], [590, 310], [558, 338], [548, 293]],
        ],
    },
    "cassia-comfort": {
        "lighting_source_blob": "a159574b0f1082369a9a447ef2dbd7b8db0c1349",
        "production_camera_position": [-0.780953050133706, 0.1916158690077558, 0.09432947247076875],
        "lighting": "shade",
        "room_anchors": [{"name": "main-bay inner upper edge", "master": [935, 215], "view": [1300, 65]}, {"name": "main-bay rail start", "master": [935, 355], "view": [1302, 297]}, {"name": "main-bay rail far end (crop)", "master": [1325, 385], "view": [1670, 320]}],
        "openings": [
            [[1012, 143], [1067, 131], [1083, 178], [1104, 218], [1141, 249], [1140, 275], [988, 273], [999, 199]],
            [[1307, 56], [1358, 22], [1404, 3], [1671, 3], [1671, 304], [1303, 286]],
            [[999, 301], [1026, 302], [1025, 398], [1000, 396]],
            [[1044, 303], [1076, 304], [1077, 405], [1048, 402]],
            [[1100, 305], [1132, 306], [1143, 413], [1120, 413]],
            [[1319, 318], [1365, 320], [1362, 437], [1320, 429]],
            [[1410, 323], [1451, 325], [1474, 458], [1406, 449]],
            [[1475, 327], [1497, 328], [1493, 441]],
            [[1540, 330], [1601, 334], [1621, 479], [1531, 468]],
            [[1628, 337], [1671, 340], [1671, 484], [1650, 481]],
        ],
    },
}


def masked_rgba(im, alpha):
    result = im.convert("RGBA")
    result.putalpha(alpha)
    return result


def camera_from_anchors(view):
    """Return the frozen production camera used by the accepted near layers.

    Visible room guides document approximation limits, not architectural proof.
    A mistaken arrival midpoint correspondence was removed after inspection;
    the accepted compositing camera stays fixed instead of changing the art.
    """
    src = np.array([a["master"] for a in view["room_anchors"]], dtype=float)
    dst = np.array([a["view"] for a in view["room_anchors"]], dtype=float)
    plane_z = 3.2
    camera_xy = np.array(view["production_camera_position"][:2])
    camera_z = view["production_camera_position"][2]
    scale = plane_z/(plane_z-camera_z)
    principal = np.array([836.0, 470.5])
    center_shift = -camera_xy*F/(plane_z-camera_z)
    translation = center_shift-(scale-1)*principal
    residual = np.linalg.norm(src*scale+translation-dst, axis=1)
    return {"position": [float(camera_xy[0]), float(camera_xy[1]), float(camera_z)], "rotation_degrees": [0, 0, 0], "focal_pixels": F, "anchor_plane_depth": plane_z, "assumption": "Explicit production camera for the accepted nearby fork layer. Guide reprojection is approximate; it does not establish the original room's geometry.", "guide_reprojection_error_pixels": [round(float(v), 2) for v in residual], "scale_at_opening_plane": float(scale)}


def plane_homography(depth, camera):
    t = -np.array(camera["position"], dtype=float)
    matrix = np.eye(3)+np.outer(t, np.array([0.0, 0.0, 1.0]))/depth
    return K@matrix@np.linalg.inv(K)


def exterior_layers(room):
    valid = np.array(mask(OPENINGS, 0))
    # Preserve complete painted fork clusters with their fine branch contours.
    # Soft edges fall in surrounding foliage, rather than cutting polygonal
    # branch silhouettes. These are explicit finite-parallax depth cards.
    distance = cv2.distanceTransform((valid>0).astype(np.uint8), cv2.DIST_L2, 5)
    interior = np.clip(distance/18.0, 0, 1)
    result = []
    for spec in DEPTH_CARDS:
        alpha = Image.fromarray((np.array(mask([spec["polygon"]], 14))*interior).astype(np.uint8))
        result.append(dict(spec, pixels=masked_rgba(room, alpha)))
    return result


def grade(image, lighting):
    a = np.array(image).astype(np.float32)
    if lighting == "day":
        # Near branches occupy olive-brown midtones, not the bright leaf/sky
        # highlights of the entire window. Preserve tonal brush detail while
        # removing blue/cyan spill inherited from the shaded source painting.
        lum = a[:, :, :3]@np.array([.2126, .7152, .0722])
        middle = np.clip(18+lum*1.20, 12, 125)
        a[:, :, 0] = middle*1.06
        a[:, :, 1] = middle*1.04
        a[:, :, 2] = middle*.76
    return Image.fromarray(np.uint8(np.clip(a, 0, 255)))


def match_existing_light(image, base, alpha, lighting):
    """Match foliage tonal range to the existing shot, without moving pixels."""
    src = np.array(image).astype(float)
    dst = np.array(base).astype(float)
    selected = alpha > 200
    curves = []
    for c in range(3):
        if lighting == "day":
            continue
        xp = np.percentile(src[:, :, c][selected], [0, 15, 50, 85, 100])
        yp = np.percentile(dst[:, :, c][selected], [0, 15, 50, 85, 100])
        # Exact black and highlight endpoints retain contrast latitude. The
        # internal monotonic points express the existing shot's illumination.
        xp[0], xp[-1], yp[0], yp[-1] = 0, 255, 0, 255
        src[:, :, c] = np.interp(src[:, :, c], xp, yp)
        curves.append({"input": xp.tolist(), "output": yp.tolist()})
    # Match broad, existing illumination variation without transferring target
    # leaf/branch geometry. Original detail is retained in the projected card.
    source_blur = cv2.GaussianBlur(src[:, :, :3].astype(np.float32), (0,0), 32)
    target_blur = cv2.GaussianBlur(dst[:, :, :3].astype(np.float32), (0,0), 32)
    envelope = np.clip((target_blur+12)/(source_blur+12), .65, 1.6)**.45
    src[:, :, :3] *= envelope
    return Image.fromarray(np.clip(src, 0, 255).astype(np.uint8)), curves


def run(install_comfort=False):
    out = PROJECT / "build/graphics/environments/exterior-rig"
    out.mkdir(parents=True, exist_ok=True)
    production = PROJECT / "art/production"
    production.mkdir(parents=True, exist_ok=True)
    room = source_images()["room"]
    planes = exterior_layers(room)
    rig = {"schema_version": 1, "coordinate_status": "Candidate production coordinates, not lore or reconstructed measurements.", "scope": "Nearby painted fork clusters only; retain each original CG's distant foliage and lighting structure. No full exterior-continuity claim.", "source": SOURCES["room"], "intrinsics": K.tolist(), "planes": [], "views": {}}
    for plane in planes:
        path = out / (plane["id"]+".png")
        plane["pixels"].save(path)
        rig["planes"].append({"id": plane["id"], "depth": plane["depth"], "texture_sha256": sha(path.read_bytes()), "texture": str(path.relative_to(PROJECT)), "mask_geometry": {"polygon": plane["polygon"], "foliage_edge_feather_pixels": 14, "distance_inside_source_opening_for_full_opacity": 18}})
    for name, view in VIEWS.items():
        file = "game/images/cg/book-one/"+name+".png"
        lighting_bytes = subprocess.check_output(["git", "cat-file", "blob", view["lighting_source_blob"]], cwd=REPO)
        lighting_base = Image.open(io.BytesIO(lighting_bytes)).convert("RGB")
        # Immutable preview base prevents applying the same layer twice after an
        # installation. The face producer applies the tracked layer to its own
        # latest accepted face composite for the two daylight scenes.
        base = lighting_base
        camera = camera_from_anchors(view)
        exterior = Image.new("RGBA", SIZE)
        projections = []
        for plane in planes:
            h = plane_homography(plane["depth"], camera)
            pixels = np.array(plane["pixels"])
            if view["lighting"] == "day":
                pigment = pixels[:, :, :3].astype(float)
                # The cool-gray branch paint has B near G; green/dark leaf
                # fringes have much less B. Reduce that coarse dark fringe
                # instead of pasting a opaque leaf mass into backlit foliage.
                branch_matte = np.clip((pigment[:, :, 2]/(pigment[:, :, 1]+1)-.60)/.36, .08, 1.0)
                branch_matte = cv2.GaussianBlur(branch_matte.astype(np.float32), (0,0), .6)
                pixels[:, :, 3] = (pixels[:, :, 3]*branch_matte).astype(np.uint8)
            projected = cv2.warpPerspective(pixels, h, SIZE, flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT)
            exterior = Image.alpha_composite(exterior, Image.fromarray(projected))
            projections.append({"plane": plane["id"], "homography": h.tolist()})
        exterior = grade(exterior, view["lighting"])
        hard = mask(view["openings"], 0)
        safe = hard.filter(ImageFilter.MinFilter(7))
        feather = safe.filter(ImageFilter.GaussianBlur(2.0))
        alpha = (np.minimum(np.array(hard), np.array(feather)).astype(float)*np.array(exterior.getchannel("A"))/255).astype(np.uint8)
        exterior, curves = match_existing_light(exterior, lighting_base, alpha, view["lighting"])
        if view["lighting"] == "day":
            exterior = exterior.filter(ImageFilter.GaussianBlur(.65))
            alpha = (alpha*.78).astype(np.uint8)
        exterior.putalpha(Image.fromarray(alpha))
        composite = Image.alpha_composite(base.convert("RGBA"), exterior).convert("RGB")
        overlay_file = production / (name+"-near-exterior.png")
        candidate_file = out / (name+"-near-candidate.png")
        exterior.save(overlay_file)
        # The ignored review path is a symlink, not a duplicate tracked bitmap.
        review_overlay = out / (name+"-near-exterior.png")
        if review_overlay.exists() or review_overlay.is_symlink():
            review_overlay.unlink()
        review_overlay.symlink_to(overlay_file)
        composite.save(candidate_file)
        Image.fromarray(alpha).save(out / (name+"-near-mask.png"))
        changes = np.any(np.array(base)!=np.array(composite), axis=2)
        outside = int(np.count_nonzero(changes & (alpha==0)))
        assert outside == 0
        rig["views"][name] = {"file": file, "source_sha256": sha(lighting_bytes), "lighting_source": {"file": file, "git_blob": view["lighting_source_blob"], "sha256": sha(lighting_bytes)}, "camera": camera, "anchors": view["room_anchors"], "openings": view["openings"], "lighting": view["lighting"], "tone_curves": curves, "daylight_matte_and_focus": {"blue_green_ratio_start": .60, "ratio_width": .36, "minimum_fringe_fraction": .08, "material_blur_pixels": .65, "opacity": .78} if view["lighting"]=="day" else None, "light_envelope": {"blur_sigma_pixels": 32, "ratio_limits": [.65, 1.6], "blend_power": .45}, "projections": projections, "overlay_file": str(overlay_file.relative_to(PROJECT)), "overlay_sha256": sha(overlay_file.read_bytes()), "candidate_sha256": sha(candidate_file.read_bytes()), "verification": {"outside_window_mask_pixels_changed": outside, "changed_pixels": int(changes.sum()), "foreground_pixel_protection": "Explicit conservative opening polygons; appearance review still required for hair and architecture edges."}}
    rig["script_file"] = "scripts/project_treehouse_exterior.py"
    rig["script_sha256"] = sha(Path(__file__).read_bytes())
    rig["dependencies"] = [{"file": "scripts/repair_treehouse_environments.py", "sha256": sha((PROJECT / "scripts/repair_treehouse_environments.py").read_bytes())}]
    (PROJECT / "docs/treehouse-exterior-rig.json").write_text(json.dumps(rig, indent=2)+"\n")
    if install_comfort:
        view = rig["views"]["cassia-comfort"]
        destination = PROJECT / view["file"]
        destination.write_bytes((out / "cassia-comfort-near-candidate.png").read_bytes())
        recipe = {
            "id": "treehouse-comfort-near-landmarks", "file": view["file"],
            "source_generation": "review-027-cassia-comfort",
            "sources": [view["lighting_source"], SOURCES["room"], {"file": view["overlay_file"], "sha256": view["overlay_sha256"]}],
            "operations": ["Project two original painted near-fork clusters at separate depths", "Match the existing CG's shade palette and broad illumination envelope", "Composite only through explicit open-air masks; preserve the original distant foliage"],
            "mask_geometry": {"window_openings": view["openings"], "depth_cards": DEPTH_CARDS, "opening_inset_pixels": 3, "opening_feather_pixels": 2, "overlay_alpha_file": view["overlay_file"]},
            "output_sha256": sha(destination.read_bytes()), "dimensions": list(SIZE), "mode": "RGB",
            "script_file": rig["script_file"], "script_sha256": rig["script_sha256"], "dependencies": rig["dependencies"],
            "camera": view["camera"], "tone_curves": view["tone_curves"], "light_envelope": view["light_envelope"],
            "verification": {"changed_pixels": view["verification"]["changed_pixels"], "outside_mask_pixels_changed": view["verification"]["outside_window_mask_pixels_changed"], "outside_mask_identical": True, "canvas_and_mode_unchanged": True, "foreground_preservation": "Bounded open-air masks; full and native appearance reviewed separately."},
        }
        register_path = PROJECT / "docs/environment-edits.json"
        register = json.loads(register_path.read_text())
        register["edits"] = [r for r in register["edits"] if r["id"] != recipe["id"]] + [recipe]
        register_path.write_text(json.dumps(register, indent=2)+"\n")
    print(json.dumps({name: v["camera"] for name,v in rig["views"].items()}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install-comfort", action="store_true")
    run(parser.parse_args().install_comfort)
