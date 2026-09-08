"""Refine the small wheel state without changing the pond or its low feed."""

import json
import math

import bmesh
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree


SCALE = 0.82
TURN = math.radians(-25)


def _ground_sampler(model, bed_only=False):
    vertices, triangles = [], []
    deps = bpy.context.evaluated_depsgraph_get()
    for obj in model.GROUPS['Ground'].objects:
        if obj.type != 'MESH' or bed_only and not obj.name.startswith('Shallow sloped pond bed'):
            continue
        evaluated = obj.evaluated_get(deps)
        data = evaluated.to_mesh()
        try:
            data.calc_loop_triangles()
            offset = len(vertices)
            vertices.extend(tuple(evaluated.matrix_world @ v.co) for v in data.vertices)
            triangles.extend(tuple(offset + i for i in tri.vertices) for tri in data.loop_triangles)
        finally:
            evaluated.to_mesh_clear()
    tree = BVHTree.FromPolygons(vertices, triangles, all_triangles=True)

    def height(point):
        hit, _, _, _ = tree.ray_cast(Vector((point.x, point.y, 3)), Vector((0, 0, -1)), 6)
        if hit is None:
            raise ValueError('Wheel fitting has no modeled supporting ground at ' + str(tuple(point)))
        return hit.z

    return height


def _annulus(model, name, point, local_y, outer, inner, depth):
    """A flat wooden band with a real open center and rectangular section."""
    count = 64
    vertices = []
    for y, radius in [(local_y - depth / 2, outer), (local_y - depth / 2, inner),
                      (local_y + depth / 2, outer), (local_y + depth / 2, inner)]:
        vertices.extend(tuple(point((radius * math.cos(i * math.tau / count), y,
                                     radius * math.sin(i * math.tau / count)))) for i in range(count))
    faces = []
    for i in range(count):
        j = (i + 1) % count
        faces.extend([(i, j, count + j, count + i),
                      (2 * count + j, 2 * count + i, 3 * count + i, 3 * count + j),
                      (j, i, 2 * count + i, 2 * count + j),
                      (count + i, count + j, 3 * count + j, 3 * count + i)])
    obj = model.mesh(name, vertices, faces, 'wood', 'Wheel')
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(obj.data)
    bm.free()
    bevel = obj.modifiers.new('Small worn board edges', 'BEVEL')
    bevel.width = 0.0012
    bevel.segments = 2
    obj['construction'] = 'Flat annular wooden band with open center'
    return obj


def _beam(model, name, start, end, width, depth):
    direction = (end - start).normalized()
    reference = Vector((0, 0, 1)) if abs(direction.z) < 0.95 else Vector((1, 0, 0))
    side = direction.cross(reference).normalized() * width / 2
    up = side.normalized().cross(direction).normalized() * depth / 2
    vertices = [tuple(p + a * side + b * up) for p in (start, end)
                for a, b in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
    return model.mesh(name, vertices, [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4),
                                     (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)], 'wood', 'Wheel')


def apply(model):
    """Run after fittings and the ground surface finish; return connection checks."""
    group = model.GROUPS['Wheel']
    if group.get('wheel_detail_version') == 1:
        return json.loads(group['wheel_detail_report'])
    center = model.unproject((0.262, 0.510), 0.14)
    rotation = Matrix.Rotation(TURN, 3, 'Z')

    def point(local):
        return center + rotation @ Vector(local) * SCALE

    def transform(obj):
        inverse = obj.matrix_world.inverted()
        for vertex in obj.data.vertices:
            world = obj.matrix_world @ vertex.co
            vertex.co = inverse @ (center + rotation @ (world - center) * SCALE)
        for modifier in obj.modifiers:
            if modifier.type == 'BEVEL':
                modifier.width *= SCALE
        obj.data.update()

    bpy.context.view_layer.update()
    bed_height = _ground_sampler(model, bed_only=True)
    ground_height = _ground_sampler(model)
    remove = ('Small wheel rim', 'Wheel support leg', 'Wheel support foot', 'Wheel support crossbar',
              'Raised feed for installed wheel', 'Feed prop', 'Stream onto small paddles')
    for obj in list(group.objects):
        if obj.name.startswith(remove):
            bpy.data.objects.remove(obj, do_unlink=True)
        elif obj.name.startswith(('Wheel axle', 'Small wheel spoke', 'Wheel paddle')):
            transform(obj)

    radius = 0.255
    for side in (-1, 1):
        _annulus(model, 'Flat wheel rim', point, side * 0.13, radius * 0.86,
                 radius * 0.66, 0.024)
        _annulus(model, 'Open axle bearing', point, side * 0.21, 0.046, 0.0255, 0.04)
        for i in range(8):
            angle = i * math.tau / 8
            r = radius * 0.76
            a = point((r * math.cos(angle), side * 0.138, r * math.sin(angle)))
            b = point((r * math.cos(angle), side * 0.153, r * math.sin(angle)))
            model.tube('Wooden rim peg', [tuple(a), tuple(b)], 0.005, 'wood', 'Wheel', 8)

    foot_contacts = []
    # Each bearing sits on one upright and a low foot. Keep the wheel's face
    # open, as in the VN, instead of enclosing it in a four-post frame.
    for y in (-0.21, 0.21):
        a, b = point((-0.27, y, 0)), point((0.27, y, 0))
        za, zb = bed_height(a), bed_height(b)
        a.z, b.z = za + 0.021, zb + 0.021
        _beam(model, 'Bed-seated wheel foot', a, b, 0.042, 0.042)
        foot_contacts.extend([dict(x=a.x, y=a.y, bed_z=za), dict(x=b.x, y=b.y, bed_z=zb)])
        top = point((0, y, -0.0425))
        bottom = Vector((top.x, top.y, bed_height(top) + 0.025))
        _beam(model, 'Bearing upright', bottom, top, 0.029, 0.034)

    # The wheel has ten paddles. The upper one at 72 degrees has an actual
    # outward board face; put the stream on that face rather than empty space.
    angle = 2 * math.tau / 10
    strike = point(((radius + 0.065 / 2) * math.cos(angle), 0,
                    (radius + 0.065 / 2) * math.sin(angle)))
    outlet = model.unproject((0.239, 0.383), strike.z + 0.14)
    start = model.unproject((0.178, 0.350), outlet.z + 0.025)
    supply = start - (outlet - start).normalized() * 0.25
    model.tube('Raised feed for installed wheel', [tuple(supply), tuple(start), tuple(outlet)],
               0.027, 'bamboo', 'Wheel', 12)
    prop = start.lerp(outlet, 0.28)
    model.tube('Connected raised-feed prop', [(prop.x, prop.y, ground_height(prop)), tuple(prop)],
               0.020, 'wood', 'Wheel', 8)
    stream_material = model.MATERIALS['stream'].copy()
    stream_material.name = 'Clear falling wheel stream'
    shader = stream_material.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (0.96, 0.99, 1.0, 1)
    shader.inputs['Alpha'].default_value = 1
    shader.inputs['Transmission Weight'].default_value = 0.80
    shader.inputs['IOR'].default_value = 1.333
    shader.inputs['Roughness'].default_value = 0.045
    model.MATERIALS[stream_material.name] = stream_material
    stream_path = []
    for i in range(9):
        t = i / 8
        p = outlet.lerp(strike, t)
        p.z = outlet.z + (strike.z - outlet.z) * t * t
        stream_path.append(tuple(p))
    model.tube('Stream onto small paddle face', stream_path,
               0.006, stream_material.name, 'Wheel', 10)

    # The tray is a separate object on the dry paving, not part of the mechanism.
    tray = model.unproject((0.10, 0.757), 0.08)
    original_bottom = 0.08 - 0.025 / 2
    support_points = [tray + Vector((x, y, 0)) for x, y in
                      [(0, 0), (-0.16, -0.112), (-0.16, 0.112), (0.16, -0.112), (0.16, 0.112)]]
    tray_bottom = max(ground_height(p) for p in support_points) + 0.004
    for obj in group.objects:
        if not obj.name.startswith(('Tool tray', 'Loose project piece')):
            continue
        inverse = obj.matrix_world.inverted()
        for vertex in obj.data.vertices:
            p = obj.matrix_world @ vertex.co
            p.x = tray.x + (p.x - tray.x) * 0.80
            p.y = tray.y + (p.y - tray.y) * 0.80
            p.z = tray_bottom + (p.z - original_bottom) * 0.60
            vertex.co = inverse @ p
        for modifier in obj.modifiers:
            if modifier.type == 'BEVEL':
                modifier.width *= 0.65
        obj.data.update()

    report = dict(scale=SCALE, clockwise_turn_degrees=25, flat_rims=2, open_axle_bearings=2,
                  rim_pegs=16, foot_contacts=foot_contacts,
                  stream_end=list(strike), feed_outlet=list(outlet),
                  tray_width_scale=0.80, tray_height_scale=0.60, tray_bottom_m=tray_bottom,
                  low_pond_feed_unchanged=True)
    group['wheel_detail_version'] = 1
    group['wheel_detail_report'] = json.dumps(report)
    return report
