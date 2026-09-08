"""REJECTED architectural experiment; see README.md before reusing any geometry.

blender --background --factory-startup --python build_model.py -- [--render all|id,id]

The model is a development candidate. Dimensions are choices, not measurements
recovered from illustrations. Validation uses the resulting mesh geometry.
"""
import argparse
from collections import defaultdict
import hashlib
import json
import math
from pathlib import Path
import random
import sys

import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
from validate_geometry import validate

RNG = random.Random(62026)
GROUPS = [
    ('house', 'Household: garden level', True),
    ('furniture', 'Working rooms and domestic furniture', True),
    ('upper', 'Upper private rooms and passage', True),
    ('roofs', 'Ceilings and shelter', False),
    ('garden', 'Household garden and water', True),
    ('oak', 'Oak and both refuges', True),
    ('canopy', 'Tree canopies', False),
    ('landscape', 'Shared woods, paths and open ground', True),
    ('context', 'Nearby destinations and inhabited depth', True),
    ('routes', 'Measured route guides', False),
    ('wheel_people', 'Waterwheel gathering', False),
    ('rescue_people', 'Pond assistance', False),
    ('landing_people', 'Treehouse arrival', False),
]
COLLECTIONS = {}
MATS = {}
LABELS = []
MARKERS = {}
CAMERAS = []
ROOMS = []
SPEC = {'routes': [], 'sightlines': [], 'clearances': [], 'open_checks': []}


def material(name, color, roughness=.7, emission=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Roughness'].default_value = roughness
    if emission:
        bsdf.inputs['Emission Color'].default_value = (*color, 1)
        bsdf.inputs['Emission Strength'].default_value = emission
    MATS[name] = m
    return m


def mesh(name, verts, faces, mat='plaster', group='house', collision=False, walk=False):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    COLLECTIONS[group].objects.link(obj)
    obj.data.materials.append(MATS[mat])
    obj['review_group'] = group
    obj['collision'] = collision
    obj['walk_surface'] = walk
    return obj


def box(name, center, size, mat='plaster', group='house', collision=True, walk=False):
    x,y,z = center; a,b,c = [s/2 for s in size]
    verts=[(x+dx*a,y+dy*b,z+dz*c) for dx,dy,dz in
           [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
    return mesh(name,verts,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat,group,collision,walk)


def floor(name, bounds, z=0, mat='wood', group='house', thick=.25):
    x0,x1,y0,y1=bounds
    return box(name,((x0+x1)/2,(y0+y1)/2,z-thick/2),(x1-x0,y1-y0,thick),mat,group,False,True)


def tube(name, points, radius, mat='bark', group='house', collision=True, sides=8):
    verts=[]
    for i,point in enumerate(points):
        p=Vector(point)
        d=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        d.normalize()
        guide=Vector((0,0,1)) if abs(d.z)<.9 else Vector((1,0,0))
        u=d.cross(guide).normalized();v=d.cross(u).normalized()
        r=radius[i] if isinstance(radius,(tuple,list)) else radius
        verts.extend(tuple(p+r*(math.cos(j*math.tau/sides)*u+math.sin(j*math.tau/sides)*v)) for j in range(sides))
    faces=[]
    for i in range(len(points)-1):
        faces.extend((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j) for j in range(sides))
    faces += [tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))]
    return mesh(name,verts,faces,mat,group,collision)


def disc(name,center,rx,ry,depth,mat='wood',group='furniture',collision=True,walk=False,n=32):
    x,y,z=center
    verts=[(x+rx*math.cos(i*math.tau/n),y+ry*math.sin(i*math.tau/n),z+h) for h in (-depth/2,depth/2) for i in range(n)]
    faces=[tuple(reversed(range(n))),tuple(range(n,n*2))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return mesh(name,verts,faces,mat,group,collision,walk)


def ellipsoid(name,center,size,mat='leaves',group='garden',collision=False,n=10,rings=6):
    x,y,z=center;a,b,c=size
    verts=[]
    for j in range(rings+1):
        phi=math.pi*j/rings
        for i in range(n):
            theta=math.tau*i/n
            verts.append((x+a*math.sin(phi)*math.cos(theta),y+b*math.sin(phi)*math.sin(theta),z+c*math.cos(phi)))
    faces=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(rings) for i in range(n)]
    return mesh(name,verts,faces,mat,group,collision)


def ring(name,center,rx,ry,width,height,mat='stone',group='garden',walk=False,collision=True,n=48):
    x,y,z=center;verts=[]
    for h in (-height/2,height/2):
        for dr in (0,width):
            verts.extend((x+(rx+dr)*math.cos(i*math.tau/n),y+(ry+dr)*math.sin(i*math.tau/n),z+h) for i in range(n))
    faces=[]
    for i in range(n):
        j=(i+1)%n
        faces += [(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)]
    return mesh(name,verts,faces,mat,group,collision,walk)


def path(name,points,width=2.4,group='garden',mat='stone',rails=False):
    """A continuous supported ribbon with mitered corners, not a route symbol."""
    points=[(x,y,z+.025) for x,y,z in points]
    verts=[]
    for i,p in enumerate(points):
        a=Vector(points[max(0,i-1)]);b=Vector(points[min(i+1,len(points)-1)])
        d=b-a; d.z=0; d.normalize();u=Vector((-d.y,d.x,0))
        verts += [tuple(Vector(p)+u*width/2),tuple(Vector(p)-u*width/2)]
    faces=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(points)-1)]
    obj=mesh(name,verts,faces,mat,group,False,True)
    if rails:
        for side in (-1,1):
            edge=[tuple(Vector(verts[i*2+(0 if side==1 else 1)])+Vector((0,0,1.05))) for i in range(len(points))]
            tube(name+' rail',edge,.055,'bark',group,True)
            for point in edge:
                tube(name+' post',[tuple(Vector(point)-Vector((0,0,1.05))),point],.06,'bark',group,True)
    return obj


def arch(name,center,width,height,axis='x',base=0,group='house',mat='bark',radius=.11):
    x,y=center; r=width/2;spring=base+height-r
    pts=[]
    if axis=='x':
        pts=[(x-r,y,base),(x-r,y,spring)]+[(x+r*math.cos(t),y,spring+r*math.sin(t)) for t in [math.pi-i*math.pi/16 for i in range(17)]]+[(x+r,y,base)]
    else:
        pts=[(x,y-r,base),(x,y-r,spring)]+[(x,y+r*math.cos(t),spring+r*math.sin(t)) for t in [math.pi-i*math.pi/16 for i in range(17)]]+[(x,y+r,base)]
    return tube(name,pts,radius,mat,group,True)


def wall(name,axis,fixed,start,end,z,height,openings,group='house',thickness=.32):
    """Actual arched voids, including full wall depth around doors and windows."""
    cursor=start
    def block(a,b,low,high,suffix):
        if b-a<.001 or high-low<.001:return
        c=((a+b)/2,fixed,(low+high)/2) if axis=='x' else (fixed,(a+b)/2,(low+high)/2)
        size=(b-a,thickness,high-low) if axis=='x' else (thickness,b-a,high-low)
        box(name+suffix,c,size,'plaster',group)
    for pos,width,top,sill in sorted(openings):
        left,right=pos-width/2,pos+width/2
        block(cursor,left,z,z+height,' solid')
        block(left,right,z,z+sill,' sill')
        # Header boundary follows a semicircular arch; short slabs form an
        # evaluated solid whose underside remains open through the wall.
        for i in range(16):
            a=left+width*i/16;b=left+width*(i+1)/16
            bottom=sill+top-width/2+math.sqrt(max(0,(width/2)**2-(((a+b)/2)-pos)**2))
            block(a,b,z+bottom,z+height,' arch header')
        center=(pos,fixed) if axis=='x' else (fixed,pos)
        arch(name+' frame',center,width,top,axis,z+sill,group)
        cursor=right
    block(cursor,end,z,z+height,' solid')


def room(name,bounds,z=0,openings=None,group='house',height=4.1):
    x0,x1,y0,y1=bounds; openings=openings or {}
    floor(name+' floor',bounds,z,group=group)
    wall(name+' north','x',y1,x0,x1,z,height,openings.get('N',[]),group)
    wall(name+' south','x',y0,x0,x1,z,height,openings.get('S',[]),group)
    wall(name+' west','y',x0,y0,y1,z,height,openings.get('W',[]),group)
    wall(name+' east','y',x1,y0,y1,z,height,openings.get('E',[]),group)
    roof=box(name+' ceiling',((x0+x1)/2,(y0+y1)/2,z+height+.10),(x1-x0,y1-y0,.2),'wood','roofs',True)
    for x in [x0+.3,(x0+x1)/2,x1-.3]:
        tube(name+' ceiling rib',[(x,y0,z+height-.2),(x,(y0+y1)/2,z+height+.05),(x,y1,z+height-.2)],.12,'bark','roofs')
    ROOMS.append({'name':name,'bounds':bounds,'floor_z':z,'area_m2':round((x1-x0)*(y1-y0),2),'group':group})
    LABELS.append({'text':name,'position':[(x0+x1)/2,(y0+y1)/2,z+.8],'group':group})


def plant(name,position,height=1,group='garden',color='leaves'):
    x,y,z=position
    tube(name+' stem',[(x,y,z),(x+.08,y+.04,z+height)],.025,'bark',group,False,5)
    for i in range(3):
        theta=i*2.4
        ellipsoid(name+' leaves',(x+math.cos(theta)*height*.22,y+math.sin(theta)*height*.22,z+height*(.45+i*.18)),(height*.33,height*.20,height*.18),color,group,False,8,4)


def pot(name,position,group='furniture',height=.65):
    x,y,z=position
    disc(name+' pot',(x,y,z+.19),.22,.22,.38,'clay',group)
    plant(name,(x,y,z+.38),height,group)


def table(name,position,rx=1,ry=None,height=.75,group='furniture'):
    x,y,z=position;ry=rx if ry is None else ry
    disc(name+' top',(x,y,z+height),rx,ry,.12,'wood',group)
    for dx,dy in [(-.5,-.5),(.5,-.5),(.5,.5),(-.5,.5)]:
        tube(name+' leg',[(x+dx*rx,y+dy*ry,z),(x+dx*rx,y+dy*ry,z+height)],.07,'bark',group)


def cushion(name,position,size=(.65,.55,.18),group='furniture'):
    return ellipsoid(name,position,size,'textile',group,True,12,5)


def bench(name,position,width=2.2,depth=.8,group='furniture',back=True):
    x,y,z=position
    box(name+' base',(x,y,z+.24),(width,depth,.48),'wood',group)
    box(name+' cushion',(x,y,z+.51),(width*.96,depth*.92,.18),'textile',group)
    if back:box(name+' back',(x,y+depth*.40,z+.85),(width,.16,.75),'wood',group)


def cabinet(name,center,width=1.8,height=2.5,group='furniture',books=True):
    x,y,z=center
    box(name+' body',(x,y,z+height/2),(width,.38,height),'wood',group)
    for row in range(4):
        level=z+.2+row*(height-.2)/4
        box(name+' shelf',(x,y-.12,level),(width+.05,.50,.06),'trim',group)
        if books:
            for i in range(9):
                w=.06+RNG.random()*.08
                box(name+' book',(x-width*.43+i*width*.10,y-.29,level+.16+RNG.random()*.02),(w,.19,.3+RNG.random()*.1),'book'+str(i%3),group,False)


def person(name,feet,height=1.6,group='wheel_people',pose='standing'):
    x,y,z=feet
    if pose=='kneeling':
        for dx in (-.13,.13):
            ellipsoid(name+' knee',(x+dx,y,z+.12),(.15,.25,.12),'figure',group)
        tube(name+' torso',[(x,y,z+.20),(x,y+.27,z+.65)],.16,'figure',group,False)
        ellipsoid(name+' head',(x,y+.37,z+.87),(.13,.13,.16),'figure',group)
        for dx in (-.18,.18):tube(name+' reaching arm',[(x+dx,y+.28,z+.64),(x+dx,y+.60,z+.54),(x+dx,y+.90,z+.40)],.05,'figure',group,False)
    else:
        for dx in (-.11,.11):tube(name+' leg',[(x+dx,y,z+.04),(x+dx,y,z+height*.48)],.07,'figure',group,False)
        tube(name+' torso',[(x,y,z+height*.45),(x,y,z+height*.79)],height*.105,'figure',group,False)
        ellipsoid(name+' head',(x,y,z+height*.9),(height*.075,height*.075,height*.09),'figure',group)
        for dx in (-.21,.21):tube(name+' arm',[(x+dx,y,z+height*.74),(x+dx,y+.12,z+height*.45)],.045,'figure',group,False)


def dog(name,feet,group='wheel_people'):
    x,y,z=feet
    ellipsoid(name+' body',(x,y,z+.5),(.45,.20,.24),'figure',group)
    ellipsoid(name+' head',(x+.4,y,z+.69),(.17,.15,.19),'figure',group)
    for dx,dy in [(-.3,-.13),(-.3,.13),(.3,-.13),(.3,.13)]:tube(name+' leg',[(x+dx,y+dy,z),(x+dx,y+dy,z+.5)],.045,'figure',group,False)


def route(id,title,points,radius=.35,height=1.85,**kwargs):
    SPEC['routes'].append(dict(id=id,title=title,points=points,radius=radius,height=height,**kwargs))
    tube(title+' guide',[(p[0],p[1],p[2]+.08) for p in points],.045,'route','routes',False,6)


def setup():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    for c in list(bpy.data.collections):
        if c.name!='Collection':bpy.data.collections.remove(c)
    scene=bpy.context.scene
    scene.unit_settings.system='METRIC';scene.unit_settings.length_unit='METERS'
    scene.unit_settings.scale_length=1
    for id,title,visible in GROUPS:
        col=bpy.data.collections.new(title);scene.collection.children.link(col);COLLECTIONS[id]=col
    for name,color in {
        'plaster':(.56,.47,.32),'wood':(.28,.15,.065),'trim':(.48,.30,.12),
        'bark':(.16,.105,.062),'stone':(.42,.43,.34),'soil':(.15,.11,.075),
        'leaves':(.12,.28,.15),'leaves_light':(.25,.38,.17),'grass':(.16,.24,.12),
        'textile':(.19,.35,.32),'clay':(.40,.22,.12),'water':(.08,.32,.32),
        'book0':(.28,.38,.31),'book1':(.46,.24,.14),'book2':(.56,.45,.23),
        'paper':(.74,.65,.43),'metal':(.23,.28,.25),'context':(.28,.36,.29),
        'figure':(.81,.49,.21),'route':(.25,.78,.72),'flower':(.75,.58,.16)
    }.items():material(name,color)
    material('light',(.72,.88,.66),emission=1.5)
    scene.render.engine='BLENDER_WORKBENCH';scene.cycles.samples=24;scene.cycles.use_denoising=False
    shading=scene.display.shading
    shading.light='STUDIO';shading.studiolight_rotate_z=.5
    shading.color_type='MATERIAL';shading.show_shadows=True
    shading.show_cavity=True;shading.cavity_type='BOTH'
    shading.curvature_ridge_factor=1.2;shading.curvature_valley_factor=.7
    shading.show_specular_highlight=True
    shading.background_type='WORLD'
    scene.cycles.device='CPU';scene.render.threads_mode='FIXED';scene.render.threads=8
    scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100
    scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.38,.50,.42,1)
    scene.world.node_tree.nodes['Background'].inputs[1].default_value=.65
    scene.view_settings.view_transform='Standard'
    scene.view_settings.exposure=.6
    scene.render.image_settings.file_format='PNG'
    scene.render.film_transparent=False


def area_light(name,position,power=600,size=5,color=(1,.82,.58)):
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size;data.color=color
    obj=bpy.data.objects.new(name,data);bpy.context.scene.collection.objects.link(obj);obj.location=position


def household():
    door=lambda p,w=1.8:(p,w,2.9,0)
    window=lambda p,w=2:(p,w,2.3,.85)
    room('Shared central room',(-5,5,-5,4),openings={'N':[door(2.5)],'S':[door(0)],'E':[door(1.7,2.6),door(-2,1.6)]})
    room('Selene — music',(-14,-5,-3,4),openings={'N':[door(-12.2)],'E':[window(.7)],'W':[window(.6)]})
    room('Dorian — library',(-13,-5,6,13),openings={'S':[door(-9)],'N':[door(-8.5)],'W':[window(8),window(11)]})
    room('Sage — room and sleeping alcove',(-4,2,6,12),openings={'S':[door(.5,1.4)],'N':[window(-1,2)],'W':[window(9,2)]})
    room('Arin — workshop',(8.5,17,6,13),openings={'E':[door(8,2)],'W':[door(7.4),window(10.5)]})
    room('Cooking and pantry',(5,11,-5,.4),openings={'W':[door(-2,1.6)],'E':[door(-2,1.8)]})
    room('Garden washing and work store',(17.4,21,6,12),openings={'W':[door(8,2)],'S':[door(19.2,2)]})
    room('Bathing and clothes',(-18,-14,6,12),openings={'S':[door(-16,1.4)]})
    floor('Branching household hall',(-18,8.5,4,6))
    floor('Stair and lift hall',(2,8.5,6,14.7))
    floor('Quiet rear gallery',(-13,8.5,13,15.2))
    floor('Workshop door link',(17,17.4,7,9))
    wall('Gallery north','x',15.2,-13,8.5,0,4.1,[window(-10,2),window(-5,2),window(0,2),window(6,2)],'house')
    # A deliberate loop around the shared room leaves its furniture usable.
    table('Family round table',(0,-.7,0),1.75,height=.76)
    for i in range(8):
        theta=math.tau*i/8
        x,y=2.2*math.cos(theta),-.7+2.2*math.sin(theta)
        cushion('Family chair seat',(x,y,.47),(.29,.29,.09))
        for dx,dy in [(-.19,-.19),(.19,.19),(-.19,.19),(.19,-.19)]:tube('Chair leg',[(x+dx,y+dy,0),(x+dx,y+dy,.47)],.035,'wood','furniture')
        tube('Chair back',[(x+.28*math.cos(theta),y+.28*math.sin(theta),.45),(x+.28*math.cos(theta),y+.28*math.sin(theta),1.05)],.08,'wood','furniture')
    box('Maps left unfinished',(0,-.7,.84),(1.6,.95,.025),'paper','furniture',False)
    bench('Left household sofa',(-3.5,.3,0),2.3,.95)
    # Fountain remains a recessed, substantial object beside the hall.
    arch('Fountain alcove',(-1.7,3.55),2.0,3.15,base=0)
    box('Fountain recess backing',(-1.7,3.85,1.65),(2.1,.55,3.3),'bark','furniture')
    for z,r in [(.38,.82),(.91,.56),(1.45,.33)]:
        disc('Fountain bowl',(-1.7,3.43,z),r,r*.62,.13,'stone')
    tube('Fountain water',[(-1.7,3.39,1.55),(-1.7,3.39,.35)],.045,'water','furniture',False)
    cabinet('Central books',(-3.6,3.66,0),1.2,3.5)
    cabinet('Art and game storage',(4.65,-4,0),.75,2.1)
    disc('Ceiling light well',(0,-.2,4.05),2.1,2.1,.10,'light','roofs',False)
    ring('Ceiling wooden ring',(0,-.2,3.98),2.1,2.1,.2,.15,'wood','roofs')
    # Actual distinctive work and teaching furniture.
    box('Arin workbench',(12.6,11.7,.9),(5.5,1.0,.16),'wood')
    for x in (10.3,14.9):box('Workbench trestle',(x,11.7,.43),(.25,.8,.86),'wood')
    cabinet('Arin parts drawers',(9.1,12.7,0),1.0,2.8,books=False)
    cabinet('Arin tool storage',(15.7,12.7,0),1.6,2.6,books=False)
    disc('Child workshop stool',(12,10.55,.44),.27,.27,.1,'wood')
    for a in (0,2.1,4.2):tube('Stool legs',[(12+.19*math.cos(a),10.55+.19*math.sin(a),0),(12+.19*math.cos(a),10.55+.19*math.sin(a),.44)],.035,'wood','furniture')
    for i in range(7):box('Project parts',(10.6+i*.5,11.8,1.02),(.24,.30,.15),'metal','furniture',False)
    box('Piano',(-9,3.05,.8),(2.3,.65,1.6),'wood')
    box('Piano keys',(-9,2.62,.86),(2.1,.28,.08),'paper')
    for i in range(24):box('Black key',(-10+i*.085,2.68,.92),(.035,.17,.04),'bark','furniture',False)
    bench('Shared piano bench',(-9,1.7,0),1.5,.48,back=False)
    tube('Harp frame',[(-7.4,2.4,.15),(-7.1,2.4,2.0),(-6.45,2.4,2.5),(-6.4,2.4,.15),(-7.4,2.4,.15)],.09,'trim','furniture')
    for i in range(12):tube('Harp string',[(-7.25+i*.065,2.4,.25),(-7.25+i*.065,2.4,1.9+i*.03)],.006,'metal','furniture',False,4)
    bench('Music listening sofa',(-6.1,-1.3,0),1.7,.75)
    for x in (-12.8,-12.1):disc('Drum',(x,-1.7,.45),.28,.28,.8,'wood')
    table('Library map table',(-9,9,0),1.35,1.0,.55)
    box('Library spread map',(-9,9,.63),(1.8,1.2,.02),'paper','furniture',False)
    for x,y in [(-10.5,8.4),(-7.4,8.4),(-8.2,7.6),(-9.2,10.4)]:cushion('Library reading cushion',(x,y,.16),(.5,.45,.15))
    for x in (-12,-6.4):cabinet('Library books',(x,12.7,0),1.1,3.5)
    bench('Library window seat',(-12.45,9.5,0),1.5,.7)
    # Sage's own bed remains in the same room as their invited story circle.
    box('Sage sleeping platform',(-3.0,9.15,.24),(1.8,2.5,.48),'wood')
    box('Sage mattress',(-3.0,9.15,.59),(1.65,2.35,.24),'textile')
    arch('Sage sleeping alcove',(-2.0,9.1),3.7,3.0,'y',0,'furniture')
    table('Sage story table',(-.65,8.6,0),.6,height=.38)
    for x,y in [(-1.4,7.6),(.35,8.2),(-.3,9.8),(-1.25,10.0)]:cushion('Sage story cushion',(x,y,.17),(.55,.45,.17))
    # Kitchen, washing, laundry and supplies have modeled footprints.
    box('Kitchen clean counter',(8,-4.4,.48),(5,.8,.96),'wood')
    box('Kitchen preparation island',(8,-.2,.46),(3.7,.65,.92),'wood')
    cabinet('Pantry',(10.65,-3.5,0),.7,2.4,books=False)
    for x in (6.6,7.4):disc('Cooking pot',(x,-4.4,1.10),.25,.25,.24,'metal')
    box('Separate garden wash counter',(20.5,10,.48),(.65,3,.96),'stone')
    cabinet('Boots and work supplies',(18.4,11.65,0),1.6,2.4,books=False)
    box('Wet clothes and drying rack',(20.6,7,.8),(.35,1.2,1.6),'wood')
    box('Bath',(-16.1,10.1,.35),(1.7,.9,.7),'stone')
    box('Bath privacy screen',(-16.6,8.7,1.15),(2.1,.15,2.3),'wood')
    cabinet('Household linen',(-17.2,11.7,0),1.2,2.5,books=False)
    disc('Toilet',(-17,7,.25),.3,.4,.5,'stone')
    # Private rooms: adjacent child rooms, four further adult retreats.
    for name,bounds,doorpos in [
        ('Kael',(-12.5,-7.7,7,12),-10.1),('Cali',(-7.7,-2.9,7,12),-5.3),('Lyra',(-2.9,1.9,7,12),-.5),
        ('Maia',(-12.5,-7.7,-.5,4.5),-10.1),('Selene',(-7.7,-2.9,-.5,4.5),-5.3),
        ('Arin',(8.5,13.25,7,12),10.7),('Dorian',(13.25,18,7,12),15.6)]:
        south=bounds[2]>5
        room(name+' — private retreat',bounds,4.8,{'S' if south else 'N':[door(doorpos,1.3)],'N' if south else 'S':[window(doorpos,1.7)]},'upper',3.4)
        x0,x1,y0,y1=bounds
        by=y1-1.25 if south else y0+1.25
        if name=='Kael':
            box('Kael loft bed',(x0+1.15,by,6.5),(1.9,2.0,.23),'wood','upper')
            for x in (x0+.25,x0+2):tube('Loft supports',[(x,by-.8,4.8),(x,by-.8,6.7)],.08,'wood','upper')
            box('Kael blanket fort',(x0+1.15,by,5.4),(1.5,.04,1.2),'textile','upper')
        else:
            box(name+' sleeping platform',(x0+1.1,by,5.05),(1.6,2.1,.5),'wood','upper')
            box(name+' bedding',(x0+1.1,by,5.39),(1.5,2,.18),'textile','upper')
        box(name+' desk',(x1-1.1,by,5.53),(1.55,.7,.12),'wood','upper')
        cabinet(name+' personal storage',(x1-.7,(y0+y1)/2,4.8),.9,2.2,'upper')
        # Open door leaf, with a real hinge/closing boundary in each room.
        yy=y0+.65 if south else y1-.65
        box(name+' open private door',(doorpos-.63,yy,6.0),(.07,1.25,2.4),'textile','upper')
        corridor_y=5.8
        route('private_'+name.lower(),name+' — independent room access',[(6,5.8,4.8),(doorpos,5.8,4.8),(doorpos,y0+.85 if south else y1-.85,4.8)],.28,1.85)
    floor('Upper shared passage',(-14,18,4.5,7),4.8,group='upper')
    floor('Upper lift approach',(5.6,8.5,7,10.5),4.8,group='upper')
    room('Upper bathing and clothes',(2,5,-.5,4.5),4.8,{'N':[door(3.5,1.4)]},'upper',3.4)
    box('Upper bath',(3.5,.4,5.15),(1.9,1.0,.7),'stone','upper')
    # A real two-flight stair occupies its own void through the upper floor.
    rise=2.4; steps=15; run=5.4
    for flight in range(2):
        for i in range(steps):
            z=(i+1)*rise/steps+flight*rise
            y=7+(i+.5)*run/steps if flight==0 else 12.4-(i+.5)*run/steps
            floor('House stair tread',(2.0,3.45,y-run/steps/2,y+run/steps/2) if flight==0 else (3.85,5.3,y-run/steps/2,y+run/steps/2),z,group='house',thick=.12)
    floor('Stair half landing',(2,5.3,12.4,13.8),2.4)
    stair_walk=[(2.72,6.6,0)]+[(2.72,7+(i+.5)*run/steps,(i+1)*rise/steps) for i in range(steps)]
    stair_walk += [(2.72,12.9,2.4),(4.57,12.9,2.4)]
    stair_walk += [(4.57,12.4-(i+.5)*run/steps,2.4+(i+1)*rise/steps) for i in range(steps)]
    stair_walk += [(4.57,6.6,4.8)]
    route('house_stair','Household stair and upper passage',stair_walk,.28,1.85,floor_tolerance=.27)
    floor('Lift lower cabin',(5.8,8.0,10.5,12.7),0,mat='metal')
    floor('Lift upper landing',(5.8,8.0,10.1,10.5),4.8,mat='metal',group='upper')
    for x in (5.75,8.05):tube('Lift guide',[(x,12.75,0),(x,12.75,8.5)],.08,'metal','house')
    route('home_lift','Reserved lift travel envelope',[(6.9,11.55,0),(6.9,11.55,4.8)],.70,2.05,support='endpoint-only')
    # Model the upper cabin as a separate posed landing state; it is hidden from
    # the default view, but explicit geometry is available for endpoint support.
    floor('Lift cabin upper endpoint',(5.8,8,10.5,12.7),4.8,mat='metal',group='upper')
    for name,p in [('central',(.5,0,3.8)),('music',(-9,0,3.8)),('library',(-9,9,3.8)),('sage',(-1,9,3.8)),('workshop',(13,9,3.8))]:area_light(name+' warm ceiling',p,180,3)
    for p in [(-4,2.4,0),(4,2.8,0),(-13,3,0),(-12.5,12.5,0),(1.4,11.3,0),(16.4,10.5,0)]:pot('Household planting',p)
    MARKERS['home']={'table':(0,-.7,.82),'fountain':(-1.7,3.40,1.25),'hall':(2.5,4,.15),'garden_door':(5,1.7,.05),'sofa':(-3.5,.3,.7)}


def garden_and_oak():
    # Paved/cultivated ground is a real surface with the pond removed. No floor
    # spans the water. Cell mesh is hidden beneath fine boundary coping.
    verts=[];faces=[]
    step=.5
    for ix in range(88):
        for iy in range(60):
            x=5+ix*step;y=-25+iy*step
            corners=[(x,y,0),(x+.5,y,0),(x+.5,y+.5,0),(x,y+.5,0)]
            if any(((px-19)/3.24)**2+((py+10)/2.54)**2<1 or ((px-43)/1.8)**2+((py+20)/1.2)**2<1 for px,py,_ in corners):continue
            if x<11 and y>=-5:continue
            offset=len(verts);verts+=corners;faces.append(tuple(offset+i for i in range(4)))
    mesh('Garden ground with basin opening',verts,faces,'soil','garden',False,True)
    # The actual dry working platform around the elliptical basin.
    ring('Dry working and recovery bank',(19,-10,-.06),3.25,2.55,2.1,.12,'stone','garden',True,False)
    ring('Low reachable basin coping',(19,-10,.04),3.20,2.50,.26,.20,'stone','garden',True,True)
    disc('Shallow basin bed',(19,-10,-.55),3.20,2.50,.15,'stone','garden',False,True)
    disc('Pond water',(19,-10,-.19),3.18,2.48,.018,'water','garden',False)
    for i in range(28):
        a=i*2.4;r=math.sqrt((i+.5)/28)
        ellipsoid('Submerged pebble',(19+math.cos(a)*r*2.9,-10+math.sin(a)*r*2.2,-.46),(.12,.09,.06),'stone','garden')
    for x,y in [(20.4,-10.3),(20.7,-10.5),(20.8,-10.0),(20.0,-10.5)]:disc('Lily pad',(x,y,-.17),.29,.23,.025,'leaves','garden',False)
    path('Work passage to garden',[(19.2,8,0),(19.2,5,0),(23,2,0),(23,-4,0),(14.3,-4,0),(14.3,-9,0)],2.6)
    path('Garden room threshold',[(5,1.7,0),(8,1.7,0),(12,-1.8,0),(14,-5,0),(14.3,-9,0)],2.5)
    path('Kitchen to garden',[(11,-2,0),(12.5,-2,0),(14,-5,0)],2.2)
    path('Garden path to wooded refuge',[(14,-5,0),(12,-15.5,0),(22,-17,0),(27,-15,0),(29,-12,.2)],2.5)
    # Household beds leave a real patch-to-ladder sightline between plant groups.
    for x,y,w,d in [(12,-7,2,3),(11,-20,3,3),(25,-20,4,2),(27,-4,3,2),(26,3,3,2),(42,-19,4,3)]:
        box('Household planting bed',(x,y,.22),(w,d,.44),'bark','garden')
        box('Garden soil',(x,y,.46),(w-.2,d-.2,.08),'soil','garden')
        for i in range(5):plant('Household flowers',(x+(RNG.random()-.5)*(w-.4),y+(RNG.random()-.5)*(d-.4),.5),.6+RNG.random()*.6,color='leaves_light')
    for x,y in [(18.0,-6.6),(18.6,-6.4),(19,-6.5)]:
        plant('Yellow far-bank flowers',(x,y,0),1.3)
        ellipsoid('Yellow flowers',(x,y,1.3),(.20,.15,.17),'flower','garden')
    for x in [15.5+i*.48 for i in range(15)]:box('Pond timber boundary',(x,-5.9,1.35),(.45,.13,2.7),'wood','garden')
    tube('Movable pond feed',[(16,-7.8,.7),(16,-8.8,.32),(17,-9,.2)],.065,'bark','garden')
    # Additional pond is beyond the familiar basin frames, retaining the plural.
    ring('Further garden pond',(43,-20,.03),1.8,1.2,.25,.15,'stone','garden',True)
    disc('Further pond bed',(43,-20,-.50),1.8,1.2,.12,'stone','garden',False,True)
    ring('Further pond dry bank',(43,-20,-.06),1.8,1.2,.8,.12,'stone','garden',True,False)
    disc('Further pond water',(43,-20,-.15),1.8,1.2,.025,'water','garden',False)
    # Mural is a household working wall, not a public street or physical scene.
    box('Garden mural wall',(29,-22.4,1.6),(6,.4,3.2),'plaster','garden')
    box('Mural paint surface',(29,-22.16,1.7),(4.8,.025,2.2),'paper','garden',False)
    bench('Mural sitting bench',(29,-20.9,0),2,.6,'garden',False)
    path('Mural approach',[(24,-17,0),(25.5,-20,0),(28,-20,0)],2.2)
    # Broad lower sitting platform, hollow room, raised upper room and landing.
    disc('Oak lower sitting platform',(34,-11,.05),7.1,4.8,.30,'wood','oak',False,True)
    # A hollow, load-bearing ring; the south-facing opening is genuinely open.
    cx,cy=37,-5.4
    for i in range(28):
        theta=math.tau*(i+.5)/28
        if abs(((theta-math.pi*1.5+math.pi)%math.tau)-math.pi)<.34:continue
        p=(cx+2.0*math.cos(theta),cy+2*math.sin(theta),.2)
        tube('Oak hollow trunk',[(p[0],p[1],.2),(p[0]-.5,p[1]+.2,4.45)], [.30,.29],'bark','oak',True,8)
    disc('Hollow interior floor',(37,-5.4,.08),1.9,1.9,.24,'wood','oak',False,True)
    floor('Hollow entrance bridge',(36.35,37.65,-8.0,-6.8),.2,group='oak')
    arch('Lower secret entrance',(37,-7.4),1.35,2.15,'x',.2,'oak',radius=.14)
    bench('Lower refuge sofa',(30,-12.5,.2),3,.8,'oak')
    bench('Lower refuge rear cushions',(33,-8.4,.2),2.5,.8,'oak')
    table('Lower refuge table',(33.2,-12.1,.2),.60,height=.38,group='oak')
    for p in [(31,-9.2,.2),(38,-12,.2)]:box('Lower treasure chest',(p[0],p[1],p[2]+.25),(.9,.55,.5),'wood','oak')
    floor('Upper oak room',(28,37.4,-7,-.4),4.8,group='oak',thick=.35)
    floor('Upper entry landing',(34.3,39.7,-9.3,-7),4.8,group='oak',thick=.28)
    # Shelter and rear timber wall; open front bays stay glass-free.
    wall('Upper rear timber wall','x',-.4,28,37.4,4.8,3.2,[],'oak',.2)
    wall('Upper west timber wall','y',28,-7,-.4,4.8,3.2,[],'oak',.2)
    floor('Oak rainproof timber roof',(27.5,38,-7.5,.1),8.25,group='roofs',thick=.22)
    for x in (28.15,31.2,34.2,37.3):
        tube('Upper frontage post',[(x,-7,4.8),(x,-7,8.25)],.12,'bark','oak')
    arch('Upper arched entry',(35.55,-7),1.55,2.65,'x',4.8,'oak',radius=.12)
    for a,b in [(28.15,31.2),(31.2,34.2)]:
        tube('Open bay rail',[(a,-7,5.76),(b,-7,5.76)],.07,'bark','oak')
        for i in range(5):tube('Open bay baluster',[(a+(b-a)*i/4,-7,4.8),(a+(b-a)*i/4,-7,5.76)],.045,'bark','oak')
        box('Open bay rust curtain',(b-.10,-7.03,6.8),(.25,.05,2.25),'clay','oak',False)
    # One diagonal branch intrudes into the room; reverse cameras retain it.
    tube('Diagonal oak within upper room',[(38,-5.4,3.8),(36.8,-4.6,4.8),(35.8,-3.8,7.2),(34.5,-1.0,10.8)], [1.1,1.0,.82,.56],'bark','oak')
    for target in [(26,-8,16),(43,-1,18),(32,5,17)]:tube('Oak canopy limb',[(35.7,-3.8,8),(36,0,12),target],[.75,.5,.15],'bark','oak')
    table('Upper map table',(31.25,-4.55,4.8),1.05,.82,.5,'oak')
    box('Treehouse map',(31.25,-4.55,5.39),(1.5,1.0,.02),'paper','oak',False)
    for x,y in [(29,-5.9),(29.2,-2.0),(33,-5.7)]:cushion('Upper floor cushions',(x,y,4.98),(.62,.50,.18),'oak')
    box('Upper drawings and treasures',(28.5,-1.5,5.15),(.65,1.2,.7),'wood','oak')
    # Familiar ladder and real landing.
    ladder_a=Vector((35.55,-11.2,.2));ladder_b=Vector((35.55,-8.4,4.8))
    for dx in (-.49,.49):tube('Oak ladder rail',[tuple(ladder_a+Vector((dx,0,0))),tuple(ladder_b+Vector((dx,0,.6)))],.065,'wood','oak')
    for i in range(18):
        p=ladder_a.lerp(ladder_b,i/17)
        tube('Oak ladder rung',[tuple(p+Vector((-.49,0,0))),tuple(p+Vector((.49,0,0)))],.042,'wood','oak')
    # Separate rear tread route reaches the SAME upper landing. It preserves
    # the pictured ladder and lets Barkley join the scene without being lifted.
    dog_points=[(41,-11,.2),(43,0,2.6),(40,2.5,4.8),(40,-7.7,4.8),(35.55,-7.7,4.8)]
    dog_walk=[dog_points[0]]
    for k,(a,b) in enumerate(zip(dog_points,dog_points[1:])):
        a,b=Vector(a),Vector(b); dz=b.z-a.z
        if abs(dz)<.01:
            path('Rear oak landing path',[tuple(a),tuple(b)],1.8,'oak','wood',False)
            dog_walk.append(tuple(b))
        else:
            n=math.ceil(dz/.16)
            d=b-a;length=Vector((d.x,d.y,0)).length;side=Vector((-d.y,d.x,0)).normalized()*.7
            for i in range(n):
                p=a.lerp(b,i/n);q=a.lerp(b,(i+1)/n);p.z=q.z
                foot=a.lerp(b,(i+.5)/n);foot.z=q.z;dog_walk.append(tuple(foot))
                mesh('Rear oak stair tread',[tuple(p+side),tuple(p-side),tuple(q-side),tuple(q+side)],[(0,1,2,3)],'wood','oak',False,True)
            dog_walk.append(tuple(b))
            path('Oak stair inner rail base',[tuple(a+side),tuple(b+side)],.05,'oak','wood')
            tube('Oak stair outer handrail',[tuple(a-side+Vector((0,0,1))),tuple(b-side+Vector((0,0,1)))],.06,'bark','oak')
    # Full corner landings join differently oriented tread runs without gaps.
    for x,y,z in dog_points[1:-1]:floor('Rear oak turning landing',(x-.95,x+.95,y-.95,y+.95),z,group='oak',thick=.18)
    # Rails turn around the perimeter, leaving the ladder and doorway open.
    tube('Rear oak continuous outer rail',[(44,0,3.65),(40.95,3.45,5.85),(40.95,-9.15,5.85),(37,-9.15,5.85)],.06,'bark','oak')
    route('oak_dog','Barkley’s proposed rear route to upper landing',dog_walk,.25,.9,floor_tolerance=.27)
    route('upper_entry','Upper landing and room entrance',[(35.55,-7.85,4.8),(35.55,-6.4,4.8),(34,-5.5,4.8),(32.6,-3,4.8)],.28,1.75)
    route('oak_hollow','Lower refuge and separate hollow entrance',[(37,-11,.2),(37,-8,.2),(37,-6.4,.2)],.28,1.8)
    # Root volume exists beneath the garden; lower inhabited context remains
    # around it, not inside an unexplained paper-thin floor.
    for i in range(9):
        theta=i*math.tau/9
        end=(37+math.cos(theta)*10,-5.4+math.sin(theta)*8,-5.5-RNG.random()*2)
        tube('Oak structural roots',[(37,-5.4,-1.2),(37+math.cos(theta)*4,-5.4+math.sin(theta)*3,-2.5),end],[.9,.65,.20],'bark','oak')
    for x,y,z,r in [(34,-5,16,9),(42,-1,18,7),(27,-8,16,7)]:ellipsoid('Oak canopy',(x,y,z),(r,r*.8,3.5),'leaves','canopy')
    # Deliberately bounded small project with removable feed fitting.
    wheel_center=Vector((16.6,-9,.12))
    for i in range(12):
        theta=i*math.tau/12
        a=wheel_center+Vector((0,math.cos(theta)*.56,math.sin(theta)*.56))
        tube('Miniature wheel spoke',[tuple(wheel_center),tuple(a)],.025,'wood','garden')
        box('Wheel paddle',tuple(a),(.46,.10,.12),'wood','garden')
    for x in (16.26,16.94):tube('Wheel support',[(x,-9,-.45),(x,-9,.32)],.045,'wood','garden')
    # Action mannequins are an optional scale layer, never character redesigns.
    for name,p,h in [('Arin',(15.5,-12.1,0),1.75),('Cali',(17.4,-13.65,0),1.35),('Joren',(16.1,-13.5,0),1.42),('Cassia',(18.6,-13.9,0),1.35),('Lyra',(20,-13.9,0),1.15)]:person(name,p,h)
    dog('Barkley',(21.1,-13.8,0))
    ellipsoid('Shadow scale',(20.8,-14.8,.24),(.30,.14,.24),'figure','wheel_people')
    ellipsoid('Nibble scale',(19.5,-14.8,.09),(.12,.055,.07),'figure','wheel_people')
    for name,p in [('Cali',(18,-13.1,0)),('Kael',(19.5,-13.1,0))]:person(name,p,group='rescue_people',pose='kneeling')
    person('Lyra in shallow water',(18.75,-12.05,-.48),1.13,'rescue_people')
    person('Joren on landing',(36.55,-8.0,4.8),1.45,'landing_people')
    person('Cali with the book',(34.65,-7.6,4.8),1.35,'landing_people')
    person('Cassia approaching landing',(35.55,-8.8,4.14),1.35,'landing_people')
    MARKERS['garden']={'upper_door':(35.55,-7,6.0),'ladder_top':tuple(ladder_b),'ladder_bottom':tuple(ladder_a),'lower_door':(37,-7.4,1.3),'lower_table':(33.2,-12.1,.6)}
    MARKERS['treehouse']={'trunk':(36.8,-4.6,4.8),'upper_door':(35.55,-7,6.0),'open_bay':(31.7,-7,6.85),'rail':(31.7,-7,5.76),'table':(31.25,-4.55,5.35)}
    MARKERS['pond']={'far_shore':(19,-7.5,-.18),'near_shore':(19,-12.5,-.18),'spout':(17,-9,.2),'yellow_plants':(18.6,-6.4,1.3),'lilies':(20.4,-10.3,-.15)}
    LABELS.extend([{'text':name,'position':p,'group':g} for name,p,g in [
        ('Maia’s household garden',[14,-18,1],'garden'),('Pond and dry work bank',[19,-10,1],'garden'),('Upper oak refuge',[31.5,-3,6],'oak'),('Lower sitting refuge',[33,-12,1],'oak'),('Mural',[29,-22,2],'garden')]])


def nearby_world():
    # These are connected context destinations, not a complete new ship plan.
    # Broad planted strata surround rather than cap the household slice.
    verts=[];faces=[]
    for ix in range(37):
        for iy in range(29):
            x=-68+ix*4;y=-44+iy*4
            if ((x+2)/74)**2+((y-12)/58)**2>1:continue
            if -20<x+2<24 and -8<y+2<18:continue
            if 4<x+2<50 and -26<y+2<6:continue
            corners=[]
            for px,py in [(x,y),(x+4,y),(x+4,y+4),(x,y+4)]:
                z=-.34+max(0,py-20)*.062+.12*math.sin(px*.10)*math.sin(py*.11)
                corners.append((px,py,z))
            k=len(verts);verts+=corners;faces.append(tuple(k+i for i in range(4)))
    mesh('Continuous shared woodland ground',verts,faces,'grass','landscape',False,True)
    # Exposed margins read as a section through deep substrate. They are
    # local study boundaries, not the outline of a free-floating land island.
    edges={}
    for f in faces:
        for a,b in zip(f,f[1:]+f[:1]):
            pa,pb=verts[a],verts[b];key=tuple(sorted((pa,pb)))
            edges[key]=edges.get(key,0)+1
    skirt_v=[];skirt_f=[]
    for (a,b),count in edges.items():
        if count!=1:continue
        k=len(skirt_v)
        skirt_v += [a,b,(b[0]+1,b[1]+.5,b[2]-6),(a[0]+1,a[1]+.5,a[2]-6)]
        skirt_f.append((k,k+1,k+2,k+3))
    mesh('Shared substrate exposed section',skirt_v,skirt_f,'soil','landscape')
    # Wrap the household in planted ground outside its occupied floor plates.
    floor('Household planted foundation',(-20,23,-7,17),-.32,'soil','house',3.0)
    floor('Garden substrate depth',(5,49,-25,5),-.9,'soil','garden',4.0)
    for x,y in [(-19,0),(-19,9),(-15,14),(-4.7,9),(-4.7,12.5),(-2,14),(2,14),(7.7,10),(7.7,12),(22,13)]:
        plant('Planted household hollow',(x,y,-.2),1.6,'house')
    for x,y in [(-17,15),(0,16),(20,16)]:
        tube('Household flowering bough',[(x,y,-.2),(x+.7,y,4),(x-1,y+.4,7)],[.27,.18,.07],'bark','house')
        ellipsoid('Household flowering crown',(x-1,y+.4,7),(2.4,1.8,1.2),'leaves_light','house')
    path('Public path bypassing household', [(-28,-25,0),(0,-28,0),(25,-28,0),(48,-24,0),(57,-10,0),(56,20,2),(62,43,4)],3.4,'landscape',rails=True)
    path('Home arrival',[(0,-5,0),(0,-8,0),(-13,-12,0),(-28,-25,0)],2.8,'landscape')
    path('Invited woodland spur',[(48,-24,0),(44,-16,0),(40,-13,.2)],2.5,'landscape')
    path('Cassia household route',[(-28,-25,0),(-43,-27,1.2),(-58,-15,3),(-53,-3,3)],3,'landscape',rails=True)
    path('Joren household route',[(22,8,0),(24,21,0),(-8,24,3),(-31,34,6),(-50,43,9)],3,'landscape',rails=True)
    path('Workshop shared arrival',[(21,8,0),(24,8,0),(24,21,0)],2.8,'landscape')
    # Articulated occupied ledges above and below the home's garden demonstrate
    # local depth while their interior details remain explicitly reserved.
    for name,p,scale in [
        ('Cassia’s home',(-54,1,3),(10,9)),('Joren’s home / Soren',(-54,49,9),(11,10)),
        ('Occupied lower ledge',(13,-25,-12),(25,8)),('Homes beyond the garden',(20,41,18),(32,10)),
        ('Upper planted gallery',(-31,25,29),(23,8))]:
        x,y,z=p;w,d=scale
        floor(name+' supported ledge',(x-w/2,x+w/2,y-d/2,y+d/2),z,'stone','context',1)
        # A continuous arcaded frontage with open bays, not house icons.
        wall(name+' inhabited facade','x',y+d/2,x-w/2,x+w/2,z,5,[(x+q*w/3,2.2,3,0) for q in (-1,0,1)],'context',.7)
        LABELS.append({'text':name+' · context','position':[x,y,z+1],'group':'context'})
        for xx in (x-w*.35,x+w*.35):
            tube(name+' living support',[(xx,y,z-10),(xx+2,y+1,z),(xx,y+2,z+9)],[1.2,1.0,.6],'bark','context')
            plant('Ledge planting',(xx,y,z),2,'context')
    # Storytelling court distinct from the larger excursion plaza.
    disc('Storytelling courtyard',(-28,-25,-.2),9,7,.4,'stone','landscape',False,True)
    for i in range(7):
        a=i*math.tau/7
        x,y=-28+7*math.cos(a),-25+5.5*math.sin(a)
        cushion('Courtyard sitting cushion',(x,y,.18),(.65,.55,.18),'landscape')
    LABELS.append({'text':'Storytelling courtyard','position':[-28,-25,1],'group':'landscape'})
    disc('Tree of Echoes clearing',(62,49,3.8),8,7,.4,'soil','landscape',False,True)
    tube('Tree of Echoes — distinct transplanted tree',[(62,49,4),(63,49,10),(60,50,18)],[1.8,1.2,.7],'bark','landscape')
    ellipsoid('Tree of Echoes canopy',(61,49,19),(10,8,4),'leaves','canopy')
    LABELS.append({'text':'Tree of Echoes · separate clearing','position':[62,49,7],'group':'landscape'})
    # Reachable construction branch, machinery room and raised overlook.
    path('Construction approach',[(24,21,0),(41,35,3),(38,63,8),(53,86,13)],3.2,'context',rails=True)
    floor('Construction machinery platform',(34,48,59,72),8,'stone','context')
    for i in range(3):box('Construction machinery',(36+i*4,68,9.2),(2.1,1.8,2.4),'metal','context')
    path('Reserved scaffold climb',[(53,86,13),(68,86,19),(68,99,25),(51,99,31)],2.3,'context',rails=True)
    floor('Dome overlook platform',(43,55,94,104),31,'wood','context')
    for i in range(3):
        x=45+i*4
        tube('Unfinished local dome rib',[(x,101,27),(x,106,39),(x,113,46),(x,125,49)],[.4,.35,.3,.22],'bark','context')
    LABELS.append({'text':'Construction and dome overlook · context','position':[49,99,33],'group':'context'})
    # Plaza is included as an excursion destination, without a false capacity.
    path('Plaza excursion route',[(-28,-25,0),(-60,-45,-2),(-77,-60,-3)],4,'context',rails=True)
    disc('Plaza visible court',(-86,-67,-3.3),19,15,.6,'stone','context',False,True)
    floor('Plaza performance dais',(-82,-75,-61,-57),-2.5,'wood','context')
    LABELS.append({'text':'Central Plaza approach · capacity unresolved','position':[-86,-67,-1],'group':'context'})
    # Forest and open ground continue beyond the household; keep clear routes.
    for i in range(34):
        theta=i*2.4
        x=18+math.cos(theta)*(42+RNG.random()*23);y=10+math.sin(theta)*(35+RNG.random()*20)
        if x<-10 and y<16:continue
        # Preserve the broad bypass below the garden and east of the oak.
        if -31<y<-21 or (51<x<61 and -20<y<24):continue
        z=0 if y<20 else 2
        disc('Shared forest rise',(x,y,z-.3),4,3,.6,'grass','landscape',False,True)
        tube('Shared woodland trunk',[(x,y,z),(x+.5,y+.3,z+7),(x-1,y+1,z+13)],[.7,.48,.20],'bark','landscape')
        ellipsoid('Shared woodland canopy',(x-1,y+1,z+13),(5,4,3),'leaves','canopy')
    # Thick living connections continue through all three axes in the context.
    for pts in [[(-55,45,-16),(-46,27,12),(-35,38,34),(-6,49,49),(25,44,56)],[(15,43,-22),(22,39,9),(29,43,29),(46,57,46)],[(64,-22,-19),(65,-5,-5),(66,20,15),(65,47,34)]]:
        tube('Inhabited body rib',pts,[3.5,2.8,2.3,1.8,1.2][:len(pts)],'bark','context')
    # A living substrate section has thickness and leaves the root mass legible.
    for x in (-12,2,18,30):
        tube('Household supporting tissue',[(x,2,-11),(x+2,3,-4),(x,4,-1.05)],[1.6,1.3,.85],'bark','house')
    area_light('Broad interior daylight',(15,-7,30),12000,35,(.79,.91,1))
    area_light('Warm garden light',(-15,-20,25),7000,25,(1,.83,.57))
    area_light('Shared landscape fill',(20,75,55),18000,55,(.66,.85,1))


def checks():
    route('wheel_carry','Carry the waterwheel from Arin’s bench to the pond',[(14,10.1,0),(14,8,0),(19.2,8,0),(19.2,5,0),(23,2,0),(23,-4,0),(14.3,-4,0),(14.3,-9,0)],.58,1.75)
    route('pond_return','Wide return from pond to garden washing',[(14.3,-9,0),(14.3,-4,0),(23,-4,0),(23,2,0),(19.2,5,0),(19.2,8,0)],.72,1.75)
    route('central_bypass','Central room: circulation around occupied table',[(0,-4,0),(3.1,-4,0),(3.1,1.7,0),(2.5,3.3,0),(2.5,5,0),(.5,5,0),(.5,6.8,0)],.3,1.85)
    route('music_approach','Music room approach from household hall',[(2.5,5,0),(-12.2,5,0),(-12.2,3.2,0),(-11.8,1.5,0)],.3,1.85)
    route('library_approach','Library approach without crossing a private room',[(2.5,5,0),(-9,5,0),(-9,6.9,0)],.3,1.85)
    route('treehouse_pacing_walk','Joren can pace beside the upper map table',[(29.3,-2.8,4.8),(30.8,-2.8,4.8),(32.6,-2.8,4.8),(33.1,-3.7,4.8)],.28,1.55)
    route('bath_access','Bath approach around its privacy screen',[(-16,5,0),(-16,7.7,0),(-14.85,7.7,0),(-14.85,9.3,0),(-15.6,9.3,0)],.28,1.85)
    route('kitchen_work','Shared table to clean cooking area',[(3.1,-2,0),(5,-2,0),(8,-2,0)],.30,1.85)
    route('oak_shared_bypass','Shared woodland route bypasses the household and refuge',[(0,-28,0),(25,-28,0),(48,-24,0),(57,-10,0),(56,20,2)],.6,1.9)
    # Clear standing/working circles have actual floor and obstacle checks.
    for id,title,center,radius,height in [
        ('screw_sorting','Arin and Cali can kneel at the workshop floor',(13.7,10.15,0),.8,1.2),
        ('kitchen_pair','Maia and Lyra can cook together',(8,-2,0),.8,1.85),
        ('landing_help','Clear landing beside the final ladder rung',(36.5,-8.2,4.8),.36,1.8),
        ('treehouse_pacing','Turning space beside the upper map table',(32.5,-2.7,4.8),.48,1.8),
        ('rescue_cali','Cali kneels on supported dry bank',(18,-13.1,0),.29,1.0),
        ('rescue_kael','Kael kneels on supported dry bank',(19.5,-13.1,0),.29,1.0),
        ('recovery','Dry space for the three-child embrace',(18.75,-14.3,0),.70,1.5),
        ('wheel_gathering','Central dry floor for the wheel gathering',(17.7,-14,0),1.35,1.85)]:
        SPEC['clearances'].append(dict(id=id,title=title,center=center,radius=radius,height=height))
    for name,p,r,h in [('Arin',(15.5,-12.1,0),.28,1.75),('Cali',(17.4,-13.65,0),.23,1.35),('Joren',(16.1,-13.5,0),.23,1.42),('Cassia',(18.6,-13.9,0),.23,1.35),('Lyra',(20,-13.9,0),.20,1.15),('Barkley',(21.1,-13.8,0),.57,.9),('Shadow',(20.8,-14.8,0),.32,.5),('Nibble',(19.5,-14.8,0),.13,.2)]:
        SPEC['clearances'].append(dict(id='wheel_position_'+name.lower(),title=name+' — supported wheel-scene position',center=p,radius=r,height=h))
    SPEC['sightlines'] += [
        dict(id='patch_ladder',title='Planting patch sees the oak ladder', **{'from':(12.8,-8.5,1.2),'to':(35.55,-9.8,2.5)}),
        dict(id='upper_garden',title='Upper refuge looks through an open bay toward the garden', **{'from':(31.7,-4,6.1),'to':(26,-15,1.1)}),
    ]
    for id,title,detail in [
        ('action_motion','Reaching, climbing and animal movement','Mannequins and clearance envelopes check occupied space. The pond assistance pose, final ladder step, wheel installation and Barkley’s gait need articulated motion review; static clearance does not establish the whole action.'),
        ('acoustics','Fountain and music audibility','The model provides connected halls and nearby rooms. Reverberation, door transmission and sound levels are not simulated.'),
        ('structure','Living structure, roots and water','Root and support volumes are represented. Material strength, pressure, root biology, growth and hydraulic capacity remain uncalculated.'),
        ('lift_operation','Accessible vertical travel','A 2.2 m cabin envelope and its two landing states are modeled. Motion, gates, power and accessible operation require a further mechanism design.'),
        ('neighborhood_scope','Nearby homes and excursions','Cassia’s home, Joren’s home, the courtyard, Tree of Echoes, construction and plaza are distinct connected context destinations. Their complete interiors and crowd capacities are not reconstructed.'),
        ('dome_access','Dome scaffold descent','The context climb is a sloped placeholder that reserves a broad route suitable for a later tread design. Its detailed stairs and Barkley’s descent remain to be validated before that excursion model is complete.'),
        ('regional_scale','Distances and population','Local distances are proposal values in metres. They do not determine a census, the whole Astravus’s dimensions, or the extent of shared forest and plains.'),
    ]:SPEC['open_checks'].append(dict(id=id,title=title,detail=detail))


def camera(id,title,position,target,fov=65,reference=None,hide=None,note=''):
    data=bpy.data.cameras.new(title);data.type='PERSP';data.lens_unit='FOV'
    data.sensor_fit='HORIZONTAL';data.angle=math.radians(fov)
    obj=bpy.data.objects.new(title,data);bpy.context.scene.collection.objects.link(obj);obj.location=position
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
    data.clip_end=1500;data.clip_start=.06
    if reference:
        image=bpy.data.images.load(str(ROOT/reference),check_existing=True)
        image.filepath=bpy.path.relpath(str(ROOT/reference),start=str(HERE))
        data.show_background_images=True;bg=data.background_images.new();bg.image=image;bg.alpha=.3;bg.display_depth='FRONT'
    # Match render aspect when reporting the vertical field for WebGL.
    vfov=2*math.atan(math.tan(math.radians(fov)/2)*720/1280)
    d=dict(id=id,title=title,position=list(position),target=list(target),fov=math.degrees(vfov),render='renders/'+id+'.png',reference='../../../'+reference if reference else None,note=note,hide_groups=hide or [])
    CAMERAS.append((obj,d))


def cameras():
    common=['wheel_people','rescue_people','landing_people','routes']
    camera('overview','The household and its wooded surroundings',(68,-69,52),(10,1,2),65,hide=['roofs','canopy']+common,note='Editable local geometry in metres. Remove the upper-room group to see the garden-level rooms; surrounding ledges are context.')
    camera('garden_level','Garden-level rooms and household facilities',(35,-42,47),(2,4,0),58,hide=['roofs','upper','canopy','context']+common,note='Upper rooms and ceilings hidden for inspection. The underlying model retains both levels.')
    camera('private_level','Upper private passage and all eight residents',(28,-27,27),(-1,6,4),60,hide=['roofs','canopy','context']+common,note='Seven upper retreats plus Sage’s garden-level room. Upper circulation stays outside the stair void.')
    camera('district','Nearby routes through an inhabited body',(140,-153,103),(0,32,6),67,hide=['roofs']+common,note='This is a local context section with open boundaries, not a whole-vessel outline or a complete regional plan.')
    camera('home','Shared central room',(.55,-4.65,1.55),(0,3.5,1.6),86,'visual-novel/game/images/backgrounds/family-home.png',common,note='Compare the table, fountain, hall and separate garden doorway. Furniture and room dimensions are proposed.')
    camera('garden','Garden exterior and both oak refuges',(17,-29,2.1),(34,-5.5,4.0),66,'visual-novel/game/images/backgrounds/garden.png',common,note='The same upper room projects left from the right-hand oak. Lower hollow and sitting refuge remain separately usable.')
    camera('treehouse','Upper oak room looking back toward the garden',(31.8,-.85,6.25),(32.9,-7,6.1),88,'visual-novel/game/images/backgrounds/treehouse-shaded.png',common,note='The camera reverses the exterior viewing direction; it does not mirror the tree or create a second room.')
    camera('pond','Shallow basin and dry bank',(19,-16.2,1.55),(19,-9.4,-.05),66,'visual-novel/game/images/backgrounds/book-one/garden-pond.png',common,note='The basin is sunk into the ground. The small feed fitting can be redirected for the wheel scene.')
    camera('workshop','Arin’s workshop',(12.7,6.5,1.6),(12.7,12,1.35),77,'visual-novel/game/images/backgrounds/book-one/workshop.png',common,note='Benches, tool storage, child’s stool, clear working floor and planted doorway are actual separate geometry.')
    camera('music','Selene’s music room',(-9,-2.3,1.55),(-9,3.4,1.4),77,'visual-novel/game/images/backgrounds/book-one/music-room.png',common,note='Piano and shared bench, harp, drums and listening seat; hall entry at the left of the view.')
    camera('library','Dorian’s library',(-9,6.5,1.55),(-9,12.3,1.35),80,'visual-novel/game/images/backgrounds/book-one/library.png',common,note='Books, map table, floor cushions and a real rear gallery connection.')
    camera('sage','Sage’s personal room',(1.3,7.3,1.5),(-2.2,9.1,1.35),83,'visual-novel/game/images/backgrounds/book-one/sage-room.png',common,note='Sleeping alcove and invited story circle occupy the same room. Its hall connection is close to the fountain.')
    camera('wheel_action','Space for the waterwheel gathering',(10,-23,8),(18,-11,0),62,'visual-novel/game/images/backgrounds/book-one/waterwheel.png',['rescue_people','landing_people','routes'],note='Scale proxies show Arin, four children and three familiars on the dry bank; this is an action-space view, not a camera match.')
    camera('rescue','Supported kneeling, shallow water and recovery space',(16,-18,4),(18.8,-12.4,.3),60,'visual-novel/game/images/cg/book-one/pond-rescue.png',['wheel_people','landing_people','routes'],note='Kneeling proxies show reach toward Lyra at the low bank. Articulation and water dynamics remain simplified.')
    camera('landing','Ladder, landing and upper entrance',(42,-16,9),(35.6,-8,5.1),65,None,['wheel_people','rescue_people','routes'],note='Three child scale proxies occupy the arrival positions; the rear tread route reaches this same landing.')


def projection_report(scene):
    source=json.loads((HERE/'camera-constraints.json').read_text())
    result=[]
    for view in source['views']:
        if hashlib.sha256((ROOT/view['source']).read_bytes()).hexdigest()!=view['sha256']:
            raise RuntimeError('Reinspect changed camera reference: '+view['source'])
        camera_obj=next(obj for obj,d in CAMERAS if d['id']==view['id'])
        residuals=[];landmarks=[]
        for lm in view['landmarks']:
            v=world_to_camera_view(scene,camera_obj,Vector(MARKERS[view['id']][lm['id']]))
            uv=[round(v.x,4),round(1-v.y,4)]
            residual=math.dist(uv,lm['uv']);residuals.append(residual)
            landmarks.append({'id':lm['id'],'label':lm['label'],'world':MARKERS[view['id']][lm['id']],'reference_uv':lm['uv'],'model_uv':uv,'error':round(residual,4),'in_front':v.z>0})
        result.append({'id':view['id'],'landmarks':landmarks,'rms':round(math.sqrt(sum(x*x for x in residuals)/len(residuals)),4)})
    return result


def export(scene,report):
    deps=bpy.context.evaluated_depsgraph_get();batches={}
    for obj in scene.objects:
        if obj.type!='MESH' or 'review_group' not in obj:continue
        ev=obj.evaluated_get(deps);m=ev.to_mesh();m.calc_loop_triangles()
        group=obj['review_group'];mat=obj.data.materials[0]
        key=(group,mat.name)
        batch=batches.setdefault(key,dict(name=group+' / '+mat.name,group=group,vertices=[],triangles=[],color=list(mat.diffuse_color[:3])))
        offset=len(batch['vertices'])//3
        for v in m.vertices:batch['vertices'].extend(round(a,4) for a in ev.matrix_world@v.co)
        for t in m.loop_triangles:batch['triangles'].extend(offset+i for i in t.vertices)
        ev.to_mesh_clear()
    allcoords=[b['vertices'] for b in batches.values()]
    low=[min(min(v[i::3]) for v in allcoords) for i in range(3)];high=[max(max(v[i::3]) for v in allcoords) for i in range(3)]
    data=dict(title='Cali’s immediate world · local 3D study',units='metres',bounds=dict(min=low,max=high),meshes=list(batches.values()),cameras=[d for _,d in CAMERAS],labels=LABELS,groups=[dict(id=i,title=t,visible=v) for i,t,v in GROUPS])
    (HERE/'model-review.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
    (HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (HERE/'geometry-spec.json').write_text(json.dumps(SPEC,ensure_ascii=False,indent=2)+'\n')
    (HERE/'room-schedule.json').write_text(json.dumps(ROOMS,ensure_ascii=False,indent=2)+'\n')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--render',default='none');parser.add_argument('--samples',type=int,default=24)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    setup();household();garden_and_oak();nearby_world();checks();cameras()
    scene=bpy.context.scene;scene.cycles.samples=args.samples
    bpy.context.view_layer.update()
    report=validate(scene,SPEC)
    projections=projection_report(scene)
    (HERE/'camera-projections.json').write_text(json.dumps(projections,ensure_ascii=False,indent=2)+'\n')
    for p in projections:
        report['checks'].append(dict(id='camera_'+p['id'],title=p['id'].capitalize()+' — reference landmark comparison',status='open',detail=f"Approximate landmark RMS displacement is {p['rms']:.3f} in normalized image coordinates. Camera and geometry require visual review; this is not a recovered blueprint.",camera=p['id'],metrics=p))
    report['summary']['open']+=len(projections)
    report['provenance']={'blender':bpy.app.version_string,'builder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'inventory_sha256':hashlib.sha256((HERE.parent/'lumen-study/space-inventory.json').read_bytes()).hexdigest(),'proposal':'LC02 candidate','units':'metres'}
    export(scene,report)
    scene.camera=CAMERAS[0][0]
    for group,col in COLLECTIONS.items():
        col.hide_render=group in CAMERAS[0][1]['hide_groups']
    # Opening the native file presents a useful local section, not the default cube.
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=='VIEW_3D':
                area.spaces.active.region_3d.view_distance=85
                area.spaces.active.region_3d.view_location=Vector((10,1,2))
                area.spaces.active.clip_end=2000
    bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'cali-local-world.blend'),compress=True)
    (HERE/'renders').mkdir(exist_ok=True)
    selected={d['id'] for _,d in CAMERAS} if args.render=='all' else set(args.render.split(','))
    for obj,d in CAMERAS:
        if d['id'] not in selected:continue
        scene.camera=obj
        for group,col in COLLECTIONS.items():col.hide_render=group in d['hide_groups']
        scene.render.filepath=str(HERE/d['render'])
        bpy.ops.render.render(write_still=True)
    print('LOCAL_MODEL_SUMMARY',json.dumps(report['summary']))


if __name__=='__main__':main()
