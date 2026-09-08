"""Editable lily pads and a raised flower for the pond's existing composition.

Call apply(model_module) after ground(), before leaf batches are materialized.
The existing eight image anchors are retained; dimensions remain proposals.
"""

import math
import random

import bpy
from mathutils import Vector


PAD_ANCHORS = (
    (.647, .559, .15), (.695, .571, .16), (.743, .602, .14),
    (.719, .626, .16), (.672, .610, .13), (.778, .638, .12),
    (.689, .667, .13), (.632, .580, .11),
)


def _materials(m):
    palette = ((.16, .225, .025), (.20, .27, .035), (.13, .19, .026))
    for index, color in enumerate(palette):
        material = m.material('Lily pad wax ' + str(index), color, .38)
        nodes, links = material.node_tree.nodes, material.node_tree.links
        shader = nodes.get('Principled BSDF')
        shader.inputs['IOR'].default_value = 1.43
        shader.inputs['Specular IOR Level'].default_value = .27
        shader.inputs['Coat Weight'].default_value = .10
        shader.inputs['Coat Roughness'].default_value = .32
        coordinates = nodes.new('ShaderNodeNewGeometry')
        noise = nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = 45
        noise.inputs['Detail'].default_value = 3
        links.new(coordinates.outputs['Position'], noise.inputs['Vector'])
        ramp = nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].position = .2
        ramp.color_ramp.elements[0].color = (*(c * .87 for c in color), 1)
        ramp.color_ramp.elements[1].position = .8
        ramp.color_ramp.elements[1].color = (*(c * 1.08 for c in color), 1)
        links.new(noise.outputs['Fac'], ramp.inputs[0])
        links.new(ramp.outputs[0], shader.inputs['Base Color'])
        bump = nodes.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = .22
        bump.inputs['Distance'].default_value = .00025
        links.new(noise.outputs['Fac'], bump.inputs['Height'])
        links.new(bump.outputs[0], shader.inputs['Normal'])
        m.material('Lily pad vein ' + str(index), tuple(c * 1.08 for c in color), .48)
    m.material('Lily ivory petal', (.83, .85, .70), .34)
    m.material('Lily inner petal', (.90, .88, .69), .38)
    m.material('Lily gold heart', (.62, .38, .025), .49)
    m.material('Lily green sepal', (.095, .15, .022), .48)


def _pad_point(center, radius, angle, phase, fraction):
    """A shallow dish, with a gently uneven round perimeter."""
    shape = 1 + .018 * math.cos(3 * angle + phase) + .009 * math.sin(5 * angle)
    radial = radius * fraction * shape
    return center + Vector((
        radial * math.cos(angle + phase),
        radial * math.sin(angle + phase) * .95,
        .0009 * fraction ** 2 + .0003 * math.sin(2 * angle + phase) * fraction ** 3,
    ))


def _pad(m, index, anchor, level, rng):
    u, v, source_radius = anchor
    radius = source_radius * .78
    center = m.unproject((u, v), m.WATER_Z + .0045)
    center.z = m.WATER_Z + .002 + level * .0018
    phase = rng.uniform(0, math.tau)
    half_notch = rng.uniform(.025, .045)
    segments, rings = 48, 6
    angles = [half_notch + (math.tau - 2 * half_notch) * j / segments for j in range(segments + 1)]
    vertices = [tuple(center)]
    for ring in range(1, rings + 1):
        vertices.extend(tuple(_pad_point(center, radius, angle, phase, ring / rings)) for angle in angles)
    faces = [(0, 1 + j, 2 + j) for j in range(segments)]
    stride = segments + 1
    for ring in range(rings - 1):
        start = 1 + ring * stride
        faces.extend((start + j, start + stride + j, start + stride + j + 1, start + j + 1) for j in range(segments))
    # Native underside and edge faces give the open notch actual thickness.
    top_count = len(vertices)
    vertices.extend((x, y, z - .0005) for x, y, z in list(vertices))
    faces.extend(tuple(i + top_count for i in reversed(face)) for face in list(faces))
    boundary = [0] + [1 + ring * stride for ring in range(rings)]
    boundary += [1 + (rings - 1) * stride + j for j in range(1, stride)]
    boundary += [1 + ring * stride + segments for ring in reversed(range(rings - 1))]
    for a, b in zip(boundary, boundary[1:] + boundary[:1]):
        faces.append((a, a + top_count, b + top_count, b))
    ob = m.mesh('Rounded lily pad ' + str(index + 1), vertices, faces,
                'Lily pad wax ' + str(index % 3), 'Water', True)
    # Splitting the rim normals avoids a falsely inflated, rounded slab edge.
    rim_edges = {tuple(sorted((a, b))) for a, b in zip(boundary, boundary[1:] + boundary[:1])}
    rim_edges |= {tuple(i + top_count for i in edge) for edge in list(rim_edges)}
    for edge in ob.data.edges:
        if tuple(sorted(edge.vertices)) in rim_edges:
            edge.use_edge_sharp = True
    if hasattr(ob.data, 'use_auto_smooth'):
        ob.data.use_auto_smooth = True
        ob.data.auto_smooth_angle = math.pi
    ob['source_image_anchor_uv'] = (u, v)
    ob['proposed_radius_m'] = radius
    ob['water_offset_m'] = center.z - m.WATER_Z
    ob['aquatic_detail'] = True
    # These ridges are deliberately much finer than the pad edge or notch.
    for vein in range(10):
        angle = .22 + vein * (math.tau - .44) / 9 + rng.uniform(-.065, .065)
        curve = rng.uniform(-.09, .09)
        points = []
        for step in range(7):
            fraction = .07 + step * .14
            p = _pad_point(center, radius, angle + curve * fraction, phase, fraction)
            p.z += .00004
            points.append(tuple(p))
        ridge = m.tube('Lily pad vein ' + str(index + 1), points,
                       [.00016 - step * .000018 for step in range(7)],
                       'Lily pad vein ' + str(index % 3), 'Water', sides=4)
        ridge['aquatic_detail'] = True


def _petal(m, name, center, angle, reach, rise, width, material):
    """A narrow boat-shaped petal, rising from the flower's central cup."""
    radial = Vector((math.cos(angle), math.sin(angle), 0))
    sideways = Vector((-math.sin(angle), math.cos(angle), 0))
    vertices = []
    along, across = 9, 6
    for i in range(along + 1):
        t = i / along
        mid = center + radial * (.009 + reach * t)
        mid.z += rise * t - .012 * math.sin(math.pi * t)
        half_width = width * math.sin(math.pi * t) ** .72
        for j in range(across + 1):
            side = -1 + 2 * j / across
            p = mid + sideways * half_width * side
            p.z += .004 * side * side * math.sin(math.pi * t)
            vertices.append(tuple(p))
    stride = across + 1
    faces = [(i * stride + j, (i + 1) * stride + j,
              (i + 1) * stride + j + 1, i * stride + j + 1)
             for i in range(along) for j in range(across)]
    ob = m.mesh(name, vertices, faces, material, 'Water', True)
    thickness = ob.modifiers.new('Petal thickness', 'SOLIDIFY')
    thickness.thickness = .00035
    thickness.offset = 0
    ob['aquatic_detail'] = True


def _flower(m):
    center = m.unproject((.696, .555), m.WATER_Z + .027)
    # Outer petals spread less than the former flat flower; inner layers rise.
    for layer, (count, reach, rise, width, offset) in enumerate((
        (8, .068, .025, .019, 0),
        (7, .049, .048, .016, .006),
        (6, .027, .060, .012, .012),
    )):
        base = center + Vector((0, 0, offset))
        for index in range(count):
            angle = index * math.tau / count + layer * .39
            _petal(m, 'Water lily petal ' + str(layer + 1), base, angle,
                   reach, rise, width, 'Lily ivory petal' if layer == 0 else 'Lily inner petal')
    for index in range(5):
        _petal(m, 'Water lily supporting sepal', center - Vector((0, 0, .005)),
               index * math.tau / 5 + .18, .046, .004, .015, 'Lily green sepal')
    heart = m.sphere('Water lily gold heart', center + Vector((0, 0, .030)),
                     (.012, .012, .013), 'Lily gold heart', 'Water', segments=16, rings=8)
    heart['aquatic_detail'] = True


def apply(m):
    """Replace only the existing aquatic leaves and flower, in their own group."""
    for ob in list(m.GROUPS['Water'].objects):
        if (ob.name.startswith('Floating lily leaf') or ob.name == 'Water lily center'
                or ob.get('aquatic_detail')):
            bpy.data.objects.remove(ob, do_unlink=True)
    # The old flat petals have not yet been converted to their shared mesh.
    m.LEAF_BATCHES.pop(('Water', 'petal'), None)
    rng = random.Random(70809)
    _materials(m)
    centers = [m.unproject((u, v), m.WATER_Z + .0045) for u, v, _radius in PAD_ANCHORS]
    levels = []
    for index, anchor in enumerate(PAD_ANCHORS):
        # Keep overlapping leaves just millimetres apart, preserving their
        # existing image anchors without interpenetration or elevated stems.
        used = {levels[other] for other in range(index)
                if (centers[index] - centers[other]).length < (anchor[2] + PAD_ANCHORS[other][2]) * .80 + .004}
        level = 0
        while level in used:
            level += 1
        levels.append(level)
        _pad(m, index, anchor, level, rng)
    _flower(m)
