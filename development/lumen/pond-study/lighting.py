"""Cycles lighting and shallow-water shading for the standalone pond study.

Call apply(build_pond_module) after the scene geometry and materials exist.
The sun relies on actual canopy geometry for its shadows. No source image is
projected onto the water or used as an environment texture.
"""

import math

import bpy
from mathutils import Vector, noise


def _close_water(surface, level):
    """Build small native ripples and a bounded medium inside the same shoreline."""
    if surface.get("lighting_ripple_mesh_version") == 3:
        return
    original = surface.data
    top_faces = [face for face in original.polygons
                 if face.normal.z > 0.9 and all(abs(original.vertices[i].co.z - level) < 0.0001 for i in face.vertices)]
    if surface.get('lighting_original_boundary'):
        values = list(surface['lighting_original_boundary'])
        boundary = [Vector((values[i], values[i + 1], level)) for i in range(0, len(values), 2)]
    elif len(top_faces) == 1:
        boundary = [original.vertices[i].co.copy() for i in top_faces[0].vertices]
    elif surface.get('lighting_closed_water'):
        # Early private ripple previews predate the stored boundary. Their
        # closing bottom face retains the original outline without wave motion.
        bottom_face = max((face for face in original.polygons if face.normal.z < -0.9),
                          key=lambda face: len(face.vertices))
        boundary = [Vector((original.vertices[i].co.x, original.vertices[i].co.y, level))
                    for i in bottom_face.vertices]
    else:
        raise ValueError("Expected the original or previously closed single-face pond surface")
    if any(abs(p.z - level) > 0.0001 for p in boundary):
        raise ValueError("Water surface height differs from the study's WATER_Z")
    area = sum(a.x * b.y - b.x * a.y for a, b in zip(boundary, boundary[1:] + boundary[:1]))
    if area < 0:
        boundary.reverse()
    surface['lighting_original_boundary'] = [value for p in boundary for value in (p.x, p.y)]
    boundary = [a.lerp(b, i / 4) for a, b in zip(boundary, boundary[1:] + boundary[:1]) for i in range(4)]
    count = len(boundary)
    # The closing face lies below the opaque pond bed. It supplies a finite
    # optical medium; it is not a newly modeled excavation depth.
    bottom = min(level - 0.6, -0.6)
    center = sum(boundary, Vector()) / count
    rings = 80

    def ripple(p, fraction):
        # Irregular low swells break reflected light into small highlights.
        # There is no repeated band texture or painted reflection on the water.
        # The outer shoreline is pinned exactly to the declared level.
        fade = min(1.0, (1.0 - fraction) / 0.06)
        height = (0.0045 * noise.noise(Vector((p.x * 10, p.y * 7, 0.32)))
                  + 0.0014 * noise.noise(Vector((p.x * 23 + 8, p.y * 16, 2.17)))
                  + 0.0004 * math.sin(math.tau * (p.x / 0.3 + p.y / 0.5)))
        return (p.x, p.y, level + height * max(0.0, fade))

    vertices = [ripple(center, 0)]
    for ring in range(1, rings + 1):
        fraction = ring / rings
        vertices.extend(ripple(center.lerp(p, fraction), fraction) for p in boundary)
    faces = [(0, 1 + i, 1 + (i + 1) % count) for i in range(count)]
    for ring in range(rings - 1):
        a = 1 + ring * count
        b = a + count
        faces.extend((a + i, b + i, b + (i + 1) % count, a + (i + 1) % count) for i in range(count))
    rim = 1 + (rings - 1) * count
    lower = len(vertices)
    vertices.extend((p.x, p.y, bottom) for p in boundary)
    faces.append(tuple(reversed(range(lower, lower + count))))
    faces.extend((rim + i, lower + i, lower + (i + 1) % count, rim + (i + 1) % count) for i in range(count))
    data = bpy.data.meshes.new("Small water ripples with pinned shoreline")
    data.from_pydata(vertices, [], faces)
    data.update()
    data.materials.append(original.materials[0])
    for face in data.polygons[:rings * count]:
        face.use_smooth = True
    surface.data = data
    surface["lighting_closed_water"] = True
    surface["lighting_ripple_mesh_version"] = 3
    surface["ripple_note"] = "Native water surface with small irregular swells; boundary vertices remain exactly at WATER_Z. A static appearance study, not a fluid simulation."
    surface["optical_bottom_note"] = "Closing face below the opaque bed bounds absorption; it does not define pond depth."


def _water_material(material):
    material.use_nodes = True
    material.diffuse_color = (0.16, 0.27, 0.22, 1)
    material.blend_method = 'OPAQUE'
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (750, 100)
    water = nodes.new('ShaderNodeBsdfRefraction')
    water.label = 'Clear transmission, IOR 1.333'
    water.location = (280, 140)
    water.inputs['Color'].default_value = (0.985, 0.995, 0.990, 1)
    water.inputs['IOR'].default_value = 1.333
    water.inputs['Roughness'].default_value = 0.025

    position = nodes.new('ShaderNodeNewGeometry')
    position.location = (-730, 50)
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 9
    noise.inputs['Detail'].default_value = 2.5
    noise.inputs['Roughness'].default_value = 0.6
    noise.location = (-510, -90)
    links.new(position.outputs['Position'], noise.inputs['Vector'])
    variation = nodes.new('ShaderNodeBump')
    variation.inputs['Strength'].default_value = 0.10
    variation.inputs['Distance'].default_value = 0.0003
    variation.location = (0, 150)
    links.new(noise.outputs['Fac'], variation.inputs['Height'])
    links.new(variation.outputs['Normal'], water.inputs['Normal'])

    reflection = nodes.new('ShaderNodeBsdfGlossy')
    reflection.label = 'Reflections of the actual garden'
    reflection.inputs['Color'].default_value = (1, 1, 1, 1)
    reflection.inputs['Roughness'].default_value = 0.055
    reflection.location = (280, 430)
    links.new(variation.outputs['Normal'], reflection.inputs['Normal'])
    fresnel = nodes.new('ShaderNodeFresnel')
    fresnel.inputs['IOR'].default_value = 1.333
    fresnel.location = (-10, 430)
    links.new(variation.outputs['Normal'], fresnel.inputs['Normal'])
    # Fine reflected ripples soften broad highlights while the transmitted
    # bed keeps its existing, restrained surface distortion. This separate
    # reflection normal is an illustration shading approximation.
    fine = nodes.new('ShaderNodeTexNoise')
    fine.name = 'Fine reflected surface ripples'
    fine.inputs['Scale'].default_value = 85
    fine.inputs['Detail'].default_value = 2
    fine.inputs['Roughness'].default_value = 0.55
    links.new(position.outputs['Position'], fine.inputs['Vector'])
    fine_bump = nodes.new('ShaderNodeBump')
    fine_bump.name = 'Fine reflection breakup'
    fine_bump.inputs['Strength'].default_value = 0.24
    fine_bump.inputs['Distance'].default_value = 0.004
    links.new(fine.outputs['Fac'], fine_bump.inputs['Height'])
    links.new(variation.outputs['Normal'], fine_bump.inputs['Normal'])
    links.new(fine_bump.outputs['Normal'], reflection.inputs['Normal'])
    links.new(fine_bump.outputs['Normal'], fresnel.inputs['Normal'])
    contrast = nodes.new('ShaderNodeMath')
    contrast.operation = 'MULTIPLY_ADD'
    contrast.use_clamp = True
    contrast.inputs[1].default_value = 3.8
    contrast.inputs[2].default_value = 0.18
    contrast.label = 'Art-directed reflection contrast; transmission remains visible'
    contrast.location = (170, 620)
    links.new(fresnel.outputs[0], contrast.inputs[0])
    surface = nodes.new('ShaderNodeMixShader')
    surface.location = (510, 370)
    links.new(contrast.outputs[0], surface.inputs[0])
    links.new(water.outputs[0], surface.inputs[1])
    links.new(reflection.outputs[0], surface.inputs[2])

    # Shadow rays pass through the surface so the shallow bed receives direct
    # sunlight without expensive refractive caustics. Camera and reflection
    # rays still use refractive water. This is an explicit shading approximation.
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    transparent.location = (290, -100)
    path = nodes.new('ShaderNodeLightPath')
    path.location = (280, -310)
    shadow = nodes.new('ShaderNodeMixShader')
    shadow.label = 'Approximate direct transmission for shadow rays'
    shadow.location = (530, 120)
    links.new(path.outputs['Is Shadow Ray'], shadow.inputs[0])
    links.new(surface.outputs[0], shadow.inputs[1])
    links.new(transparent.outputs['BSDF'], shadow.inputs[2])
    links.new(shadow.outputs[0], output.inputs['Surface'])
    absorption = nodes.new('ShaderNodeVolumeAbsorption')
    absorption.inputs['Color'].default_value = (0.64, 0.82, 0.72, 1)
    absorption.inputs['Density'].default_value = 1.5
    absorption.location = (520, -190)
    links.new(absorption.outputs[0], output.inputs['Volume'])
    material['shadow_treatment'] = 'Transparent shadow rays approximate shallow transmitted sunlight; refractive caustics are not simulated.'
    material['reflection_treatment'] = 'Angle-dependent reflection contrast is increased for the illustration study. This is art direction, not a calibrated optical simulation; the bed remains visible through refractive transmission.'


def _wet_bed():
    """Darken submerged mineral albedo while retaining the actual pebble forms."""
    for material in bpy.data.materials:
        if not material.name.startswith(('bed', 'pebble')) or not material.use_nodes:
            continue
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        principled = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if principled is None or nodes.get('Submerged mineral albedo'):
            continue
        color = principled.inputs['Base Color']
        source = color.links[0].from_socket if color.is_linked else None
        multiply = nodes.new('ShaderNodeMixRGB')
        multiply.name = 'Submerged mineral albedo'
        multiply.blend_type = 'MULTIPLY'
        multiply.inputs[0].default_value = 1
        multiply.inputs[2].default_value = (0.60, 0.64, 0.58, 1)
        if source:
            links.new(source, multiply.inputs[1])
        else:
            multiply.inputs[1].default_value = color.default_value
        links.new(multiply.outputs[0], color)
        principled.inputs['Roughness'].default_value = 0.36


def _light(name, kind, position, target, color, energy, size=None):
    data = bpy.data.lights.new(name, kind)
    data.color = color
    data.energy = energy
    if kind == 'SUN':
        data.angle = math.radians(1.5)
    elif size is not None:
        data.shape = 'DISK'
        data.size = size
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = position
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()
    return obj


def apply(model_module):
    """Install review lighting and water in the existing editable scene."""
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 8
    scene.cycles.samples = 384
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.02
    scene.cycles.adaptive_min_samples = 48
    scene.cycles.use_denoising = False
    scene.cycles.use_preview_denoising = False
    scene.cycles.max_bounces = 10
    scene.cycles.diffuse_bounces = 4
    scene.cycles.glossy_bounces = 4
    scene.cycles.transmission_bounces = 8
    scene.cycles.transparent_max_bounces = 12
    scene.cycles.volume_bounces = 0
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
    scene.cycles.sample_clamp_indirect = 3
    scene.cycles.seed = 91027
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Medium High Contrast'
    scene.view_settings.exposure = 0.25
    scene.view_settings.gamma = 1

    water_objects = [ob for ob in model_module.GROUPS['Water'].objects
                     if ob.type == 'MESH' and ob.name.startswith('Water surface')]
    if len(water_objects) != 1:
        raise ValueError('Expected one original pond water surface')
    surface = water_objects[0]
    _close_water(surface, model_module.WATER_Z)
    _water_material(surface.data.materials[0])
    _wet_bed()

    for obj in list(bpy.data.objects):
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj, do_unlink=True)
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get('Background')
    background.inputs['Color'].default_value = (0.17, 0.24, 0.32, 1)
    background.inputs['Strength'].default_value = 0.34
    _light('Warm light through the actual canopy', 'SUN', (-3.5, -4.5, 7),
           (0, -1.4, 0), (1.0, 0.83, 0.59), 0.85)
    _light('Cool open-garden fill', 'AREA', (1.0, -4.2, 4.8),
           (0, -1.3, 0.15), (0.66, 0.81, 1), 45, 5.5)
    _light('Warm garden bounce', 'AREA', (-3.2, -2.0, 2.6),
           (0, -0.5, 0.3), (1, 0.83, 0.61), 26, 3)
    opening = _light('Daylight opening reflected in the pond', 'AREA', (0.0, 0.4, 2.9),
                     (0, -2.6, 0), (0.70, 0.85, 1.0), 9, 4.5)
    opening.data.shape = 'RECTANGLE'
    opening.data.size_y = 1.1
    patch = _light('Warm opening across the near bank', 'SPOT', (-2.5, -3.5, 4.4),
                   (-0.3, -2.7, 0), (1, 0.87, 0.67), 1400)
    patch.data.spot_size = math.radians(38)
    patch.data.spot_blend = 0.6
    patch.data.shadow_soft_size = 0.25
    _light('Warm light within the rear planting', 'AREA', (-2.6, -0.1, 3.5),
           (-1.2, 0.4, 0.8), (1, 0.86, 0.61), 180, 2.0)
    scene['water_shading_note'] = 'IOR 1.333 refractive transmission with art-directed reflection contrast, shallow absorption and native millimetre ripples. Transparent shadow rays approximate direct sunlight. This is not a calibrated optical or fluid simulation.'
    scene['lighting_note'] = 'Warm directional light and cool ambient fill use modeled canopy for dappled shadows. No painted source is projected into the render.'
