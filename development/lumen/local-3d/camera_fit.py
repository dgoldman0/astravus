#!/usr/bin/env python3
"""Suggest bounded camera poses for reviewed VN landmarks, without changing geometry.

Run with a Python environment containing NumPy and SciPy after build_model.py.
The output is a proposal for visual inspection, not an automatic camera edit.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares


HERE = Path(__file__).resolve().parent
ASPECT = 1280 / 720
# Positions stay near the room or garden approach. Interior heights are relative
# to their modeled floors; the treehouse floor is at z=4.8 m. These bounds are
# candidate production choices and do not establish the source camera's height.
BOUNDS = {
    "home": ([[-0.8, 1.8], [-5.4, -4.0], [1.4, 1.9]], [70, 96]),
    "garden": ([[17, 43], [-35, -19], [1.45, 2.1]], [48, 78]),
    "treehouse": ([[29, 34], [-2.2, -0.7], [6.15, 6.7]], [65, 96]),
    "pond": ([[17.5, 20.5], [-17.5, -14], [1.5, 2.1]], [58, 88]),
}


def pose(camera):
    position = np.array(camera["position"], dtype=float)
    forward = np.array(camera["target"], dtype=float) - position
    forward /= np.linalg.norm(forward)
    yaw = math.atan2(forward[1], forward[0])
    pitch = math.asin(forward[2])
    hfov = math.degrees(2 * math.atan(math.tan(math.radians(camera["fov"]) / 2) * ASPECT))
    return np.array([*position, yaw, pitch, hfov])


def axes(parameters):
    yaw, pitch = parameters[3:5]
    forward = np.array([math.cos(pitch) * math.cos(yaw),
                        math.cos(pitch) * math.sin(yaw), math.sin(pitch)])
    right = np.cross(forward, np.array([0.0, 0.0, 1.0]))
    right /= np.linalg.norm(right)
    up = np.cross(right, forward)
    return forward, right, up


def project(parameters, points):
    forward, right, up = axes(parameters)
    relative = points - parameters[:3]
    depth = relative @ forward
    denominator = np.maximum(depth, 0.01) * 2 * math.tan(math.radians(parameters[5]) / 2)
    uv = np.column_stack((0.5 + relative @ right / denominator,
                          0.5 - (relative @ up) * ASPECT / denominator))
    return uv, depth


def fit(view, camera):
    initial = pose(camera)
    points = np.array([m["world"] for m in view["landmarks"]])
    reference = np.array([m["reference_uv"] for m in view["landmarks"]])
    current = np.array([m["model_uv"] for m in view["landmarks"]])
    projected, _ = project(initial, points)
    if np.max(np.abs(current - projected)) > 0.001:
        raise ValueError(f"{view['id']}: projection inputs are inconsistent; rebuild model-review.json and camera-projections.json together")
    positions, lenses = BOUNDS[view["id"]]
    yaw_allowance = math.radians(65 if view["id"] == "garden" else 35)
    lower = np.array([*(v[0] for v in positions), initial[3] - yaw_allowance, math.radians(-38), lenses[0]])
    upper = np.array([*(v[1] for v in positions), initial[3] + yaw_allowance, math.radians(10), lenses[1]])
    initial_in_bounds = np.clip(initial, lower + 1e-6, upper - 1e-6)

    def residual(parameters):
        uv, depth = project(parameters, points)
        # A small preference for the existing view avoids unnecessary movement.
        restraint = (parameters - initial) * np.array([0.002, 0.002, 0.01, 0.015, 0.015, 0.0003])
        return np.concatenate(((uv - reference).ravel(), restraint, np.minimum(depth - 0.15, 0)))

    result = least_squares(residual, initial_in_bounds, bounds=(lower, upper),
                           x_scale=[2, 2, 0.3, 0.2, 0.2, 10],
                           loss="soft_l1", f_scale=0.05, max_nfev=1500,
                           ftol=1e-11, xtol=1e-11, gtol=1e-11)
    fitted = result.x
    uv, depth = project(fitted, points)
    forward, _, _ = axes(fitted)
    distance = np.linalg.norm(np.array(camera["target"]) - np.array(camera["position"]))
    target = fitted[:3] + forward * distance
    errors = np.linalg.norm(uv - reference, axis=1)
    active = [label for label, value, lo, hi in zip(
        ["x", "y", "z", "yaw", "pitch", "horizontal_fov"], fitted, lower, upper)
        if min(abs(value - lo), abs(value - hi)) < 0.001]
    return {
        "id": view["id"],
        "position": np.round(fitted[:3], 5).tolist(),
        "target": np.round(target, 5).tolist(),
        "horizontal_fov_degrees": round(float(fitted[5]), 5),
        "roll_degrees": 0,
        "original_rms": view["rms"],
        "proposed_rms": round(float(np.sqrt(np.mean(errors ** 2))), 5),
        "at_search_bounds": active,
        "all_landmarks_in_front": bool(np.all(depth > 0)),
        "landmarks": [dict(id=m["id"], proposed_uv=np.round(p, 5).tolist(),
                           error=round(float(error), 5))
                      for m, p, error in zip(view["landmarks"], uv, errors)],
    }


def main():
    projection_path = HERE / "camera-projections.json"
    review_path = HERE / "model-review.json"
    constraints_path = HERE / "camera-constraints.json"
    projections = json.loads(projection_path.read_text())
    cameras = {c["id"]: c for c in json.loads(review_path.read_text())["cameras"]}
    report = {
        "schema_version": 1,
        "status": "Camera proposals requiring rendered visual review",
        "notes": [
            "Only camera position, aim and horizontal field of view are fitted. Geometry and source art are unchanged.",
            "The fit uses approximate source landmarks and keeps the camera upright within declared position and lens bounds. It does not recover the illustration's original camera.",
            "Low residuals do not establish visibility. A marker can project correctly while a trunk, wall or furnishing hides it.",
            "Inspect the proposed renders for recognizable features, clear routes, sensible perspective and a coherent shared environment before accepting a pose.",
            "A result at a search bound may indicate a geometry mismatch. Do not automatically widen bounds or distort the model to erase residuals.",
        ],
        "input_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in [projection_path, review_path, constraints_path]},
        "search_bounds": BOUNDS,
        "views": [fit(view, cameras[view["id"]]) for view in projections],
    }
    (HERE / "camera-fit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    for view in report["views"]:
        print(f"{view['id']}: {view['original_rms']:.4f} -> {view['proposed_rms']:.4f}; bounds: {', '.join(view['at_search_bounds']) or 'none'}")


if __name__ == "__main__":
    main()
