"""A section through the modeled paving and bed, at unchanged vertical scale."""
import math
import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def build(m):
    cy=m.CENTER.y
    mat=m.material('Section lettering',(.84,.90,.85),.6)
    node=mat.node_tree.nodes.get('Principled BSDF')
    node.inputs['Emission Color'].default_value=(.84,.90,.85,1)
    node.inputs['Emission Strength'].default_value=.8
    for name,color,emission in [('Section soil cut',(.11,.073,.038),.8),
                                ('Section stone cut',(.37,.29,.18),.8),
                                ('Section water line',(.20,.49,.59),1.0)]:
        material=m.material(name,color,.85)
        shader=material.node_tree.nodes.get('Principled BSDF')
        shader.inputs['Emission Color'].default_value=(*color,1)
        shader.inputs['Emission Strength'].default_value=emission
        nodes=material.node_tree.nodes;links=material.node_tree.links
        flat=nodes.new('ShaderNodeEmission');flat.inputs['Color'].default_value=(*color,1)
        flat.inputs['Strength'].default_value=emission
        links.new(flat.outputs[0],nodes.get('Material Output').inputs['Surface'])
    deps=bpy.context.evaluated_depsgraph_get()
    bed=bpy.data.objects['Shallow sloped pond bed']
    ev=bed.evaluated_get(deps);data=ev.to_mesh()
    tree=BVHTree.FromPolygons([ev.matrix_world@v.co for v in data.vertices],[tuple(p.vertices) for p in data.polygons])
    ev.to_mesh_clear()
    # Top profile is sampled from the actual bed mesh. Outside its footprint,
    # substrate continues under the actual paving stones copied below.
    profile=[];wet=[]
    dry_z=bpy.data.objects['Continuous garden ground around the water'].data.vertices[0].co.z
    for i in range(161):
        x=-3.2+i*.04
        hit,normal,index,distance=tree.ray_cast(Vector((x,cy,1)),Vector((0,0,-1)),2)
        z=hit.z if hit is not None else dry_z
        profile.append((x,z))
        if hit is not None:wet.append((x,z))
    outline=[(-3.2,-.78),(3.2,-.78)]+list(reversed(profile))
    # Put the diagram's soil face 1 mm behind the paving cut faces. Coincident
    # faces flicker into triangular patches even with an unlit cut material.
    verts=[(x,cy+dy,z) for dy in (-.079,.08) for x,z in outline]
    n=len(outline)
    faces=[tuple(reversed(range(n))),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    m.mesh('Substrate section from the actual bed profile',verts,faces,'Section soil cut','Section marks')
    copied=0
    for ob in list(m.GROUPS['Ground'].objects):
        if ob.get('surface')!='dry paving':continue
        corners=[ob.matrix_world@Vector(c) for c in ob.bound_box]
        if max(c.y for c in corners)<cy-.08 or min(c.y for c in corners)>cy+.08:continue
        ev=ob.evaluated_get(deps);data=ev.to_mesh();bm=bmesh.new();bm.from_mesh(data)
        bm.transform(ev.matrix_world)
        for y,normal in ((cy-.08,(0,-1,0)),(cy+.08,(0,1,0))):
            result=bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.000001,plane_co=(0,y,0),plane_no=normal,clear_outer=True)
            boundary=[e for e in bm.edges if e.is_boundary]
            if boundary:bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
        if bm.faces:
            output=bpy.data.meshes.new('Cut '+ob.name);bm.to_mesh(output)
            clone=bpy.data.objects.new('Cut '+ob.name,output);m.GROUPS['Section marks'].objects.link(clone)
            output.materials.append(m.MATERIALS['Section stone cut'])
            copied+=1
        bm.free();ev.to_mesh_clear()
    # Water is drawn to the same bed/shore intersection, with no vertical
    # exaggeration. A thin slab makes its level readable in the section.
    if wet:
        left,right=wet[0][0],wet[-1][0]
        m.box('Section water level',((left+right)/2,cy,m.WATER_Z),(right-left,.16,.012),'Section water line','Section marks')

    def text(body,x,z,size=.105):
        data=bpy.data.curves.new(body,'FONT');data.body=body;data.size=size
        data.align_x='CENTER';data.align_y='CENTER'
        ob=bpy.data.objects.new(body,data);m.GROUPS['Section marks'].objects.link(ob)
        data.materials.append(m.MATERIALS['Section lettering']);ob.location=(x,cy-.13,z);ob.rotation_euler=(math.pi/2,0,0)
    def line(name,points):m.tube(name,[(x,cy-.14,z) for x,z in points],.006,'Section lettering','Section marks',5)
    text('POND SECTION  /  actual vertical scale',0,1.04,.15)
    text('Continuous dry ground',-1.95,.66)
    line('Ground callout',[(-2.15,.54),(-2.65,.31),(-2.65,0)])
    text('Nominal water level: -6.5 cm',1.55,.66)
    line('Water callout',[(1.65,.53),(1.5,.28),(.95,m.WATER_Z)])
    text('Shallow sloped bed',-.15,.37)
    line('Bed callout',[(-.15,.26),(-.15,-.24)])
    text('Metre scale, water level and depth are proposed',0,-1.05,.11)
    text('The section uses the modeled bed and cut paving meshes',0,-1.24,.10)
    line('One metre scale',[(-.5,-.89),(.5,-.89)])
    for x in (-.5,.5):line('Scale tick',[(x,-.92),(x,-.86)])
    text('1 m',0,-.82,.085)
    m.camera('section',(0,cy-8,.1),(0,cy,-.1),ortho=6.7)
    return {'cut_y_m':round(cy,3),'copied_paving_meshes':copied,'water_level_m':m.WATER_Z,
            'sampled_bed_z_range_m':[round(min(z for _,z in wet),3),round(max(z for _,z in wet),3)],
            'vertical_exaggeration':1,'note':'Profile sampled from the bed mesh; paving is cut from evaluated stone meshes.'}
