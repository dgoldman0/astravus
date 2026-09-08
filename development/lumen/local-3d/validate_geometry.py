"""Measure proposed scene routes against evaluated Blender mesh geometry.

Run inside Blender, or import ``validate(scene, spec)`` from the model builder.
CLI: blender --background --python validate_geometry.py -- model.blend spec.json report.json

Collision checks sample an upright body envelope; they are not a dynamics,
structural, accessibility-code, or acoustic certification. Hidden geometry still
participates when tagged collision=True or walk_surface=True.
"""

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


STEP = 0.18
HEIGHT_STEP = 0.20
RADIAL_RAYS = 24
EPSILON = 0.0001


def _number(value, name, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    value = float(value)
    if not math.isfinite(value) or (positive and value <= 0):
        raise ValueError(f"{name} must be {'positive and ' if positive else ''}finite")
    return value


def _point(value, name):
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        raise ValueError(f"{name} must have three coordinates")
    return Vector(tuple(_number(v, name) for v in value))


def _coords(point):
    return [round(float(v), 5) for v in point]


class MeshIndex:
    """World-space BVHs of the actual evaluated, triangulated tagged meshes."""

    def __init__(self, scene, tag, depsgraph):
        self.parts = []
        vertices, triangles, owners = [], [], []
        for obj in sorted(scene.objects, key=lambda item: item.name):
            if obj.type != "MESH" or not obj.get(tag, False):
                continue
            evaluated = obj.evaluated_get(depsgraph)
            mesh = evaluated.to_mesh()
            try:
                mesh.calc_loop_triangles()
                verts = [evaluated.matrix_world @ vertex.co for vertex in mesh.vertices]
                faces = [tuple(face.vertices) for face in mesh.loop_triangles]
                if not verts or not faces:
                    continue
                if not all(math.isfinite(component) for vertex in verts for component in vertex):
                    raise ValueError(f"{obj.name} contains non-finite evaluated geometry")
                edges = Counter(tuple(sorted((face[i], face[(i + 1) % 3])))
                                for face in faces for i in range(3))
                closed = all(count == 2 for count in edges.values())
                self.parts.append({
                    "name": obj.name,
                    "bvh": BVHTree.FromPolygons(verts, faces, all_triangles=True),
                    "low": Vector(tuple(min(v[i] for v in verts) for i in range(3))),
                    "high": Vector(tuple(max(v[i] for v in verts) for i in range(3))),
                    "closed": closed,
                })
                offset = len(vertices)
                vertices.extend(verts)
                triangles.extend(tuple(offset + v for v in face) for face in faces)
                owners.extend([obj.name] * len(faces))
            finally:
                evaluated.to_mesh_clear()
        self.owners = owners
        self.bvh = BVHTree.FromPolygons(vertices, triangles, all_triangles=True) if triangles else None

    def ray(self, origin, direction, distance):
        if self.bvh is None:
            return None
        hit, normal, face, length = self.bvh.ray_cast(origin, direction, distance)
        if hit is None:
            return None
        return {"object": self.owners[face], "point": _coords(hit),
                "distance": float(length), "normal_z": float(normal.z)}

    def inside(self, point):
        # A fully enclosing solid can evade short rays that never reach its
        # surface. Check odd/even crossings for closed meshes whose bounds contain
        # the body axis. Open architectural surfaces remain covered by short rays.
        direction = Vector((0.883, 0.319, 0.345)).normalized()
        for part in self.parts:
            if not part["closed"] or not all(part["low"][i] + EPSILON < point[i] <
                                            part["high"][i] - EPSILON for i in range(3)):
                continue
            distance = (part["high"] - part["low"]).length * 2 + 1
            cursor = point.copy()
            crossings = 0
            for _ in range(256):
                hit, _normal, _face, length = part["bvh"].ray_cast(cursor, direction, distance)
                if hit is None:
                    break
                crossings += 1
                cursor = hit + direction * EPSILON
                distance -= length + EPSILON
                if distance <= 0:
                    break
            else:
                raise ValueError(f"Cannot reliably classify interior of {part['name']}")
            if crossings % 2:
                return {"object": part["name"], "point": _coords(point), "inside_solid": True}
        return None


def _samples(points):
    result = [points[0]]
    for start, end in zip(points, points[1:]):
        count = max(1, math.ceil((end - start).length / STEP))
        if len(result) + count > 100000:
            raise ValueError("Route exceeds the 100,000-sample validation limit")
        result.extend(start.lerp(end, i / count) for i in range(1, count + 1))
    return result


def _collision(index, feet, radius, height):
    intervals = max(1, math.ceil(height / HEIGHT_STEP))
    for j in range(intervals + 1):
        level = EPSILON + (height - EPSILON) * j / intervals
        origin = feet + Vector((0, 0, level))
        enclosing = index.inside(origin)
        if enclosing:
            return enclosing
        for ray in range(RADIAL_RAYS):
            angle = 2 * math.pi * ray / RADIAL_RAYS
            direction = Vector((math.cos(angle), math.sin(angle), 0))
            hit = index.ray(origin, direction, radius)
            if hit:
                return hit
        # This additional nearest-surface probe catches small legs between rays
        # when their nearest point lies inside the vertical body envelope.
        if index.bvh:
            hit, _normal, face, _distance = index.bvh.find_nearest(origin, radius)
            if hit is not None and feet.z + EPSILON <= hit.z <= feet.z + height:
                if math.hypot(hit.x - feet.x, hit.y - feet.y) < radius - EPSILON:
                    return {"object": index.owners[face], "point": _coords(hit), "nearest_surface": True}
    return None


def _support(index, feet, radius, tolerance):
    # The whole useful path width must have ground, not just its centerline.
    offsets = [Vector((0, 0, 0))] + [
        Vector((math.cos(i * math.pi / 4) * radius,
                math.sin(i * math.pi / 4) * radius, 0)) for i in range(8)]
    for offset in offsets:
        probe = feet + offset
        hit = index.ray(probe + Vector((0, 0, tolerance)), Vector((0, 0, -1)), tolerance * 2)
        if hit is None or hit["normal_z"] < 0.25:
            return {"point": _coords(probe), "reason": "No upward supporting surface within tolerance",
                    "hit": hit}
    return None


def _identity(entry):
    if not isinstance(entry, dict):
        raise ValueError("Check entries must be objects")
    for key in ("id", "title"):
        if not isinstance(entry.get(key), str) or not entry[key].strip():
            raise ValueError(f"Each check requires a nonempty {key}")
    return {"id": entry["id"], "title": entry["title"]}


def validate(scene, spec):
    """Return geometric evidence without changing the scene or adopting canon."""
    if not isinstance(spec, dict):
        raise ValueError("Validation specification must be an object")
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    blockers = MeshIndex(scene, "collision", depsgraph)
    floors = MeshIndex(scene, "walk_surface", depsgraph)
    checks, ids = [], set()
    for kind in ("routes", "clearances", "sightlines", "open_checks"):
        entries = spec.get(kind, [])
        if not isinstance(entries, list):
            raise ValueError(f"{kind} must be a list")
        for entry in entries:
            result = _identity(entry)
            if result["id"] in ids:
                raise ValueError(f"Duplicate check identifier: {result['id']}")
            ids.add(result["id"])
            try:
                if kind == "open_checks":
                    if not isinstance(entry.get("detail"), str) or not entry["detail"].strip():
                        raise ValueError("Open checks require an explanation")
                    result.update(status="open", detail=entry["detail"])
                elif kind == "sightlines":
                    start, end = _point(entry.get("from"), "from"), _point(entry.get("to"), "to")
                    length = (end - start).length
                    if length <= 0.1:
                        raise ValueError("Sightline must exceed the 0.10 m target-surface allowance")
                    hit = blockers.inside(start) or blockers.ray(start, (end - start).normalized(), length - 0.1)
                    result.update(status="fail" if hit else "pass", detail=(
                        f"View is blocked by {hit['object']} at {hit['point']}." if hit else
                        "No tagged blocker intersects the sightline before its final 0.10 m."),
                        metrics={"length_m": round(length, 3), "from": _coords(start),
                                 "to": _coords(end), "obstruction": hit})
                else:
                    radius = _number(entry.get("radius", 0.35), "radius", True)
                    height = _number(entry.get("height", 1.9), "height", True)
                    tolerance = _number(entry.get("floor_tolerance", 0.25), "floor_tolerance", True)
                    if height < 0.1:
                        raise ValueError("Body height must be at least 0.10 m")
                    support_mode = entry.get("support", "all")
                    if support_mode not in ("all", "endpoint-only"):
                        raise ValueError("support must be all or endpoint-only")
                    if kind == "routes":
                        raw = entry.get("points")
                        if not isinstance(raw, list) or len(raw) < 2:
                            raise ValueError("A route requires at least two feet positions")
                        points = [_point(p, "route point") for p in raw]
                        positions = _samples(points)
                        length = sum((b - a).length for a, b in zip(points, points[1:]))
                    else:
                        positions = [_point(entry.get("center"), "center")]
                        length = 0.0
                    collision_failure = support_failure = None
                    for i, feet in enumerate(positions):
                        if collision_failure is None:
                            hit = _collision(blockers, feet, radius, height)
                            if hit:
                                collision_failure = {"sample": i, "feet": _coords(feet), **hit}
                        if support_failure is None and (support_mode == "all" or i in (0, len(positions)-1)):
                            hit = _support(floors, feet, radius, tolerance)
                            if hit:
                                support_failure = {"sample": i, "feet": _coords(feet), **hit}
                        if collision_failure and support_failure:
                            break
                    failed = collision_failure or support_failure
                    detail = ("Sampled body clearance and supporting surfaces are present." if not failed else
                              "The proposed envelope intersects geometry or lacks supporting ground.")
                    if collision_failure:
                        detail += f" First obstruction: {collision_failure['object']} near {collision_failure['feet']}."
                    if support_failure:
                        detail += f" First unsupported probe: {support_failure['point']}."
                    if support_mode == "endpoint-only":
                        detail += " Support was checked only at the endpoints; lift mechanism, operation and loads remain outside this check."
                    result.update(status="fail" if failed else "pass", detail=detail, metrics={
                        "route_length_m": round(length, 3), "samples": len(positions),
                        "radius_m": radius, "height_m": height, "floor_tolerance_m": tolerance,
                        "support": support_mode, "collision_failure": collision_failure,
                        "support_failure": support_failure,
                    })
            except (ValueError, TypeError, KeyError) as error:
                result.update(status="fail", detail=f"Invalid check data: {error}")
            checks.append(result)
    counts = Counter(check["status"] for check in checks)
    return {
        "summary": {"status": "fail" if counts["fail"] else ("pass-with-open-items" if counts["open"] else "pass"),
                    "pass": counts["pass"], "fail": counts["fail"], "open": counts["open"],
                    "blocker_objects": len(blockers.parts), "support_objects": len(floors.parts)},
        "method": {"route_sample_spacing_max_m": STEP, "body_height_spacing_max_m": HEIGHT_STEP,
                   "horizontal_rays_per_height": RADIAL_RAYS, "support_probes_per_position": 9,
                   "geometry": "Evaluated mesh triangles in world space, including tagged hidden objects",
                   "limits": "Sampled occupancy and visibility only; no dynamics, structural, acoustic or code-compliance claim."},
        "checks": checks,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("blend", type=Path)
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    bpy.ops.wm.open_mainfile(filepath=str(args.blend.resolve()))
    report = validate(bpy.context.scene, json.loads(args.spec.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps(report["summary"]))
    if report["summary"]["fail"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
