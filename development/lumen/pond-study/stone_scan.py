"""Photographed CC0 rock surfaces on the editable flagstone geometry."""
from pathlib import Path
import bpy


def apply(m):
    folder=Path(__file__).with_name('textures')
    images={}
    for kind in ('diff','disp','rough'):
        im=bpy.data.images.load(str(folder/('rock_boulder_dry_'+kind+'_2k.jpg')),check_existing=True)
        im.colorspace_settings.name='sRGB' if kind=='diff' else 'Non-Color'
        im.pack();images[kind]=im
    for index in range(5):
        mat=m.MATERIALS['stone'+str(index)];nodes=mat.node_tree.nodes;links=mat.node_tree.links;nodes.clear()
        output=nodes.new('ShaderNodeOutputMaterial');shader=nodes.new('ShaderNodeBsdfPrincipled')
        links.new(shader.outputs[0],output.inputs['Surface'])
        shader.inputs['Specular IOR Level'].default_value=.25
        geom=nodes.new('ShaderNodeNewGeometry')
        mapping=nodes.new('ShaderNodeVectorMath');mapping.operation='SCALE'
        mapping.inputs[3].default_value=1/1.8
        links.new(geom.outputs['Position'],mapping.inputs[0])
        offset=nodes.new('ShaderNodeVectorMath');offset.operation='ADD'
        offset.inputs[1].default_value=(index*.373,index*.651,index*.19)
        links.new(mapping.outputs[0],offset.inputs[0])
        textures={}
        for kind,im in images.items():
            node=nodes.new('ShaderNodeTexImage');node.image=im;node.projection='BOX';node.projection_blend=.2
            links.new(offset.outputs[0],node.inputs['Vector']);textures[kind]=node
        color=nodes.new('ShaderNodeMixRGB');color.blend_type='MULTIPLY';color.inputs[0].default_value=1
        palette=[(.63,.59,.50),(.88,.70,.45),(.58,.61,.58),(.86,.72,.53),(.56,.49,.37)]
        color.inputs[2].default_value=(*palette[index],1)
        links.new(textures['diff'].outputs['Color'],color.inputs[1])
        xyz=nodes.new('ShaderNodeSeparateXYZ');links.new(geom.outputs['Position'],xyz.inputs[0])
        wet=nodes.new('ShaderNodeMapRange');wet.clamp=True
        wet.inputs['From Min'].default_value=-.075;wet.inputs['From Max'].default_value=-.040
        wet.inputs['To Min'].default_value=.43;wet.inputs['To Max'].default_value=1
        links.new(xyz.outputs['Z'],wet.inputs['Value'])
        darken=nodes.new('ShaderNodeMixRGB');darken.blend_type='MULTIPLY';darken.inputs[0].default_value=1
        links.new(color.outputs[0],darken.inputs[1]);links.new(wet.outputs[0],darken.inputs[2])
        links.new(darken.outputs[0],shader.inputs['Base Color'])
        links.new(textures['rough'].outputs[0],shader.inputs['Roughness'])
        bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.85;bump.inputs['Distance'].default_value=.065
        links.new(textures['disp'].outputs[0],bump.inputs['Height']);links.new(bump.outputs[0],shader.inputs['Normal'])
        mat['texture_source']='Rock Boulder Dry / Poly Haven / CC0'
