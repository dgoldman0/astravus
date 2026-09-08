"""Standalone pond reconstruction from the current VN, with editable geometry.

blender --background --factory-startup --python build_pond.py -- --render all

The shoreline is traced in the reference view and reconstructed on a coping
plane using a declared camera assumption. Metre scale and hidden depth remain
proposed. No geometry or dimensions are imported from the rejected local model.
"""
import argparse
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
sys.path.insert(0,str(HERE))
import actions
import section
import render_set
import surface_detail
import paving
import aquatic_detail
import stone_scan
import wheel_detail
import lighting
RNG = random.Random(91026)
CAMERA = Vector((0, -6, 1.7))
PITCH = math.radians(23)
HFOV = math.radians(62)
ASPECT = 1672 / 941
WATER_Z = -.065
# Whole inner shoreline, read from garden-pond.png in normalized coordinates.
# This is a visible contour, not a mathematically regular oval.
TRACE = [
    (.505,.807),(.640,.792),(.760,.750),(.846,.697),(.901,.616),
    (.915,.542),(.890,.478),(.827,.423),(.746,.394),(.650,.375),
    (.546,.367),(.442,.371),(.358,.388),(.285,.418),(.231,.456),
    (.186,.498),(.142,.555),(.113,.618),(.110,.675),(.152,.727),
    (.255,.773),(.375,.803),
]
GROUPS = {}
MATERIALS = {}
LEAF_BATCHES = {}
CAMERAS = {}
SOURCE_PATHS = {
    'pond':'visual-novel/game/images/backgrounds/book-one/garden-pond.png',
    'wheel':'visual-novel/game/images/backgrounds/book-one/waterwheel.png',
    'rescue':'visual-novel/game/images/cg/book-one/pond-rescue.png',
    'comfort':'visual-novel/game/images/cg/book-one/pond-comfort.png',
}


def mesh(name, vertices, faces, mat, group='Ground', smooth=False):
    data=bpy.data.meshes.new(name);data.from_pydata(vertices,[],faces);data.update()
    ob=bpy.data.objects.new(name,data);GROUPS[group].objects.link(ob)
    data.materials.append(MATERIALS[mat])
    if smooth:
        for poly in data.polygons:poly.use_smooth=True
    return ob


def material(name, color, roughness=.7, bump=0, scale=10):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=roughness
    if bump:
        n=m.node_tree.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=scale
        n.inputs['Detail'].default_value=3.5
        b=m.node_tree.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.55
        b.inputs['Distance'].default_value=bump
        m.node_tree.links.new(n.outputs['Fac'],b.inputs['Height'])
        m.node_tree.links.new(b.outputs['Normal'],p.inputs['Normal'])
        ramp=m.node_tree.nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].position=.15
        ramp.color_ramp.elements[0].color=(*(c*.65 for c in color),1)
        ramp.color_ramp.elements[1].position=.85
        ramp.color_ramp.elements[1].color=(*(min(1,c*1.3) for c in color),1)
        m.node_tree.links.new(n.outputs['Fac'],ramp.inputs[0]);m.node_tree.links.new(ramp.outputs[0],p.inputs['Base Color'])
    MATERIALS[name]=m
    return m


def tube(name, points, radii, mat='branch', group='Planting', sides=8):
    vertices=[]
    for i,point in enumerate(points):
        p=Vector(point);direction=(Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])).normalized()
        guide=Vector((1,0,0)) if abs(direction.z)>.85 else Vector((0,0,1))
        u=direction.cross(guide).normalized();v=direction.cross(u).normalized()
        r=radii[i] if isinstance(radii,(list,tuple)) else radii
        vertices.extend(tuple(p+r*(u*math.cos(j*math.tau/sides)+v*math.sin(j*math.tau/sides))) for j in range(sides))
    faces=[]
    for i in range(len(points)-1):
        faces.extend((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j) for j in range(sides))
    faces += [tuple(reversed(range(sides))),tuple((len(points)-1)*sides+i for i in range(sides))]
    return mesh(name,vertices,faces,mat,group,True)


def prism(name, polygon, top, bottom, mat, group='Ground', bevel=0):
    if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(polygon,polygon[1:]+polygon[:1]))<0:
        polygon=list(reversed(polygon))
    n=len(polygon)
    vertices=[(x,y,bottom) for x,y in polygon]+[(x,y,top) for x,y in polygon]
    faces=[tuple(reversed(range(n))),tuple(range(n,n*2))]
    faces.extend((i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n))
    ob=mesh(name,vertices,faces,mat,group)
    if bevel:
        mod=ob.modifiers.new('Worn edges','BEVEL');mod.width=bevel;mod.segments=2
        ob.data.use_auto_smooth=True
        mod=ob.modifiers.new('Broad stone normals','WEIGHTED_NORMAL');mod.keep_sharp=True
    return ob


def box(name,center,size,mat,group='Fittings',bevel=0):
    x,y,z=center;a,b,c=(s/2 for s in size)
    return prism(name,[(x-a,y-b),(x+a,y-b),(x+a,y+b),(x-a,y+b)],z+c,z-c,mat,group,bevel)


def sphere(name,center,size,mat,group='Ground',segments=12,rings=6):
    vertices=[];x,y,z=center;a,b,c=size
    for j in range(rings+1):
        phi=math.pi*j/rings
        for i in range(segments):
            t=i*math.tau/segments
            vertices.append((x+a*math.sin(phi)*math.cos(t),y+b*math.sin(phi)*math.sin(t),z+c*math.cos(phi)))
    faces=[(j*segments+i,j*segments+(i+1)%segments,(j+1)*segments+(i+1)%segments,(j+1)*segments+i) for j in range(rings) for i in range(segments)]
    return mesh(name,vertices,[tuple(reversed(f)) for f in faces],mat,group,True)


def unproject(uv,z=WATER_Z):
    u,v=uv
    forward=Vector((0,math.cos(PITCH),-math.sin(PITCH)))
    up=Vector((0,math.sin(PITCH),math.cos(PITCH)))
    ray=forward+Vector((1,0,0))*(u-.5)*2*math.tan(HFOV/2)+up*(.5-v)*2*math.tan(HFOV/2)/ASPECT
    return CAMERA+ray*((z-CAMERA.z)/ray.z)


SHORE=[unproject(p,0) for p in TRACE]
CENTER=sum(SHORE,Vector())/len(SHORE)


def outline(t):
    # Piecewise cubic interpolation follows the individually observed corners.
    q=(t%1)*len(SHORE);i=math.floor(q);u=q-i
    a,b,c,d=[SHORE[j%len(SHORE)] for j in (i-1,i,i+1,i+2)]
    return .5*((2*b)+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u*u*u)


def contour(t, distance=0, z=0):
    p=outline(t);radial=p-CENTER;radial.z=0;radial.normalize()
    p+=radial*distance;p.z=z
    return p


def inside(point):
    x,y=point[:2];result=False
    for a,b in zip(SHORE,SHORE[1:]+SHORE[:1]):
        if (a.y>y)!=(b.y>y) and x<(b.x-a.x)*(y-a.y)/(b.y-a.y)+a.x:result=not result
    return result


def leaf(base, direction, length, width, mat, group='Planting'):
    """A folded, curved leaf blade with a visible central ridge, not a ball."""
    p=Vector(base);d=Vector(direction).normalized()
    guide=Vector((0,0,1)) if abs(d.z)<.9 else Vector((1,0,0))
    side=d.cross(guide).normalized()
    key=(group,mat);vertices,faces=LEAF_BATCHES.setdefault(key,([],[]));start=len(vertices)
    for i in range(9):
        t=i/8;mid=p+d*length*t+Vector((0,0,math.sin(t*math.pi)*length*.12-t*t*length*.05))
        w=width*math.sin(math.pi*t)**.8
        vertices += [tuple(mid-side*w),tuple(mid+Vector((0,0,w*.08))),tuple(mid+side*w)]
    for i in range(8):
        a=start+i*3;b=a+3
        faces += [(a,b,b+1,a+1),(a+1,b+1,b+2,a+2)]


def shrub(position,height=.7,spread=.5,fern=False):
    base=Vector(position)
    for frond in range(7 if fern else 13):
        a=frond*2.4+RNG.uniform(-.3,.3);reach=spread*RNG.uniform(.65,1.15)
        end=base+Vector((math.cos(a)*reach,math.sin(a)*reach,height*RNG.uniform(.48,.98)))
        points=[tuple(base.lerp(end,t)+Vector((0,0,height*.35*math.sin(t*math.pi)))) for t in (0,.25,.5,.75,1)]
        tube('Fern rachis' if fern else 'Leafy garden stem',points,[.009,.007,.005,.003,.001],sides=5)
        tangent=(end-base).normalized();side=Vector((-tangent.y,tangent.x,.2)).normalized()
        count=11 if fern else 10
        for i in range(count):
            t=.22+i*.7/count;p=base.lerp(end,t)+Vector((0,0,height*.35*math.sin(t*math.pi)))
            length=(.14 if fern else .13)*RNG.uniform(.8,1.15)*(1-t*.60)
            for sign in (-1,1):
                direction=side*sign+tangent*.55+Vector((0,0,RNG.uniform(-.2,.4)))
                leaf(p,direction,length,length*(.14 if fern else .28),'leaf'+str(RNG.randrange(4)))
        leaf(end,tangent,.075,.022,'leaf1')


def iris(position,height=.55):
    p=Vector(position)
    for i in range(9):
        a=i*2.4
        leaf(p,(math.cos(a)*.25,math.sin(a)*.25,1),height*RNG.uniform(.55,1.15),.012,'reed')
    for i in range(5):
        top=p+Vector((RNG.uniform(-.14,.14),RNG.uniform(-.09,.09),height*RNG.uniform(.90,1.5)))
        tube('Yellow iris stem',[tuple(p),tuple(top)],.0035,'reed',sides=5)
        for j in range(5):
            a=j*math.tau/5
            leaf(top,(math.cos(a)*.5,math.sin(a)*.5,.8 if j%2 else -.3),.032,.013,'yellow')


def ground():
    # A continuous paved/soil surface surrounds the actual open basin. Its
    # outer extent is only a cropped garden fragment, never a vessel outline.
    n=168;vertices=[]
    for i in range(n):
        p=contour(i/n,0,-.045);d=p-CENTER;d.z=0;d.normalize()
        vertices += [tuple(p),tuple(Vector((CENTER.x,CENTER.y,-.045))+d*8)]
    faces=[(2*i,2*((i+1)%n),2*((i+1)%n)+1,2*i+1) for i in range(n)]
    mesh('Continuous garden ground around the water',vertices,[tuple(reversed(f)) for f in faces],'earth')
    paving.build(sys.modules[__name__])
    # Sloped bed: marginal water remains shallow, with a deeper central hollow.
    vertices=[(CENTER.x,CENTER.y,-.31)]
    for ring in range(1,9):
        r=ring/8
        for i in range(n):
            p=CENTER+(outline(i/n)-CENTER)*r
            z=-.31+.10*r*r+.008*math.sin(p.x*5)*math.cos(p.y*4)
            vertices.append((p.x,p.y,z))
    faces=[(0,1+i,1+(i+1)%n) for i in range(n)]
    for ring in range(7):
        a=1+ring*n;b=a+n
        faces += [(a+i,b+i,b+(i+1)%n,a+(i+1)%n) for i in range(n)]
    mesh('Shallow sloped pond bed',vertices,faces,'bed',smooth=True)
    # Joint pebbles and larger submerged stones give readable bottom depth.
    for i in range(1400):
        t=RNG.random();r=math.sqrt(RNG.random())*.98;p=CENTER+(outline(t)-CENTER)*r
        z=-.31+.10*r*r+.008*math.sin(p.x*5)*math.cos(p.y*4)
        radius=RNG.uniform(.025,.065)
        sphere('Submerged pebble',(p.x,p.y,z+radius*.25),(radius,radius*RNG.uniform(.55,.9),radius*.42),'pebble'+str(i%4),segments=8,rings=4)
    water=mesh('Water surface — 6.5 cm below the paving',[(p.x,p.y,WATER_Z) for p in [outline(i/n) for i in range(n)]],[tuple(range(n))],'water','Water')
    water['water_level_m']=WATER_Z
    for i,(u,v,radius) in enumerate([(.647,.559,.15),(.695,.571,.16),(.743,.602,.14),(.719,.626,.16),(.672,.61,.13),(.778,.638,.12),(.689,.667,.13),(.632,.58,.11)]):
        radius*=.78
        p=unproject((u,v),WATER_Z+.004);angle=RNG.random()*math.tau
        vertices=[tuple(p)]
        for j in range(25):
            a=angle+.18+j*(math.tau-.36)/24
            vertices.append((p.x+radius*math.cos(a),p.y+radius*.87*math.sin(a),p.z+.006*math.sin(j*.8)))
        mesh('Floating lily leaf',vertices,[(0,j,j+1) for j in range(1,25)],'lily','Water')
    p=unproject((.696,.555),WATER_Z+.045)
    for j in range(12):
        a=j*math.tau/12
        leaf(p,(math.cos(a),math.sin(a),.55),.10,.027,'petal','Water')
    sphere('Water lily center',tuple(p+Vector((0,0,.03))),(.025,.025,.025),'yellow','Water')


def planting():
    # Back boundary follows the source's sheltered timber enclosure.
    for i in range(47):
        x=-4.7+i*.20
        box('Weathered boundary board',(x,1.24,1.27+RNG.uniform(-.025,.025)),(.19,.085,2.58),'timber'+str(i%3),'Boundary',.012)
    for z in (.25,1.4,2.35):box('Boundary cross timber',(0,1.31,z),(9.6,.11,.10),'branch','Boundary')
    for side in (-1,1):
        for i in range(20):box('Returning garden boundary',(side*4.65,1.2-i*.2,1.27),(.08,.19,2.58),'timber'+str(i%3),'Boundary',.01)
    # Dense layers start outside the coping; several plant forms are modeled
    # as actual folded blades and stems so the enclosure exists in other views.
    for row in range(3):
        for i in range(29):
            x=-4.3+i*.31+RNG.uniform(-.10,.10);y=.0+row*.38+RNG.uniform(-.10,.1)
            if inside((x,y)):continue
            h=RNG.uniform(.26,.46) if -1.6<x<1.5 else RNG.uniform(.48,.95)
            shrub((x,y,-.025),h,RNG.uniform(.28,.43),fern=i%3==0)
    for side in (-1,1):
        for i in range(16):
            y=-.15-i*.23;x=side*(2.25+.16*math.sin(i*.7))
            if inside((x,y)):x+=side*.3
            shrub((x,y,-.02),RNG.uniform(.40,.90),RNG.uniform(.35,.55),fern=i%2==0)
            if i%2==0:shrub((x+side*.52,y,-.02),1.1,.7)
    # Vine curtains mask much of the upper fence, leaving irregular glimpses.
    for i in range(23):
        x=-4.6+i*.4
        for j in range(3):
            z=1.0+j*.55+RNG.uniform(-.13,.13)
            if j<2 and -1.8<x<1.8:continue
            shrub((x,1.02,z),.48,.36)
    left_iris=unproject((.378,.406),WATER_Z);left_iris.z=-.20
    center_iris=unproject((.535,.384),WATER_Z);center_iris.z=-.19
    for p,h in [(left_iris,.60),(center_iris,.48),((2.3,-.75,-.02),.48),((-2.5,-2.0,-.02),.65)]:
        for i in range(2 if p[0]>1 else 3):iris((p[0]+RNG.uniform(-.12,.12),p[1]+RNG.uniform(-.07,.07),p[2]),h)
    # Branches and foliage overlap the boundary rather than isolated tree icons.
    for pts,r in [([(-3.6,-.8,0),(-3.4,-.5,1.3),(-3.0,-.1,2.1),(-2.1,.4,2.65)],[.15,.12,.07,.025]),
                  ([(3.7,-.6,0),(3.55,-.3,1.4),(3.05,.1,2.4),(1.9,.6,2.8)],[.16,.11,.065,.02]),
                  ([(-3.5,-.1,1.6),(-1.9,.3,2.3),(-.5,.7,2.6),(1,.8,2.7)],[.08,.065,.04,.015])]:
        tube('Enclosing garden branch',pts,r)
        a,b=Vector(pts[-2]),Vector(pts[-1])
        for j in range(6):shrub(tuple(a.lerp(b,j/5)),.4,.45)
    # Small living lights remain among vegetation, as in the VN.
    for i in range(44):
        side=-1 if i%2 else 1
        p=(side*RNG.uniform(1.8,3.4),RNG.uniform(-2.7,.6),RNG.uniform(.2,1.1))
        sphere('Blue living light',p,(.004,.003,.008),'glow','Planting',8,4)


def fittings():
    # Two feed states share their concealed supply route, with the small
    # fitting repositioned when the portable project is installed.
    base=unproject((.212,.399),.19);tip=unproject((.319,.440),.035)
    supply=base-(tip-base).normalized()*.7
    tube('Low pond feed',[tuple(supply),tuple(base),tuple(tip)],.031,'bamboo','Pond feed',12)
    tube('Concealed feed support',[(base.x-.2,base.y,-.04),(base.x-.2,base.y,base.z)],.024,'branch','Pond feed',8)
    tube('Small falling inlet stream',[tuple(tip),tuple(tip+Vector((.04,0,-.15)))],.004,'stream','Pond feed',8)
    center=unproject((.262,.510),.14)
    radius=.255
    tube('Wheel axle',[(center.x,center.y-.27,center.z),(center.x,center.y+.27,center.z)],.024,'wood','Wheel')
    for y in (center.y-.13,center.y+.13):
        ring=[]
        for i in range(49):
            a=i*math.tau/48;ring.append((center.x+radius*.81*math.cos(a),y,center.z+radius*.81*math.sin(a)))
        tube('Small wheel rim',ring,.020,'wood','Wheel',6)
        for i in range(8):
            a=i*math.tau/8
            tube('Small wheel spoke',[(center.x,y,center.z),(center.x+radius*.83*math.cos(a),y,center.z+radius*.83*math.sin(a))],.012,'wood','Wheel',6)
    for i in range(10):
        a=i*math.tau/10
        ob=box('Wheel paddle',(center.x+radius*math.cos(a),center.y,center.z+radius*math.sin(a)),(.065,.32,.025),'wood','Wheel',.005)
        # Rotate the mesh around the paddle's own center, retaining editability.
        pivot=Vector((center.x+radius*math.cos(a),center.y,center.z+radius*math.sin(a)))
        from mathutils import Matrix
        rot=Matrix.Rotation(-a,4,'Y')
        for v in ob.data.vertices:v.co=pivot+rot@(v.co-pivot)
    for x in (center.x-.31,center.x+.31):
        for y in (center.y-.21,center.y+.21):
            tube('Wheel support leg',[(x,y,-.32),(x,y,center.z+.04)],.020,'wood','Wheel',6)
        box('Wheel support foot',(x,center.y,-.28),(.05,.53,.06),'wood','Wheel',.005)
    for y in (center.y-.21,center.y+.21):
        box('Wheel support crossbar',(center.x,y,center.z),(.68,.035,.035),'wood','Wheel')
    outlet=(center.x-.03,center.y,center.z+radius+.13)
    start=(base.x,base.y,base.z+.22)
    tube('Raised feed for installed wheel',[start,outlet],.033,'bamboo','Wheel',12)
    tube('Feed prop',[(start[0]+.20,start[1],-.22),(start[0]+.20,start[1],start[2])],.025,'wood','Wheel',8)
    tube('Stream onto small paddles',[outlet,(center.x,center.y,center.z+radius)],.007,'stream','Wheel',8)
    # Tool tray is on the near dry bank, never floating in the water.
    tray=unproject((.10,.757),.08)
    box('Tool tray bottom',tuple(tray),(.40,.28,.025),'wood','Wheel',.007)
    for dx in (-.20,.20):box('Tool tray side',(tray.x+dx,tray.y,.14),(.025,.28,.14),'wood','Wheel',.006)
    for dy in (-.14,.14):box('Tool tray end',(tray.x,tray.y+dy,.14),(.40,.025,.14),'wood','Wheel',.006)
    for i in range(5):tube('Loose project piece',[(tray.x-.12+i*.05,tray.y-.07,.11),(tray.x-.11+i*.05,tray.y+.07,.11)],.01,'bamboo','Wheel',6)
    p=tray+Vector((.20,-.23,-.055))
    tube('Small screwdriver',[tuple(p),tuple(p+Vector((.22,.08,0)))],.007,'metal','Wheel',8)
    tube('Screwdriver handle',[tuple(p),tuple(p+Vector((.075,.025,0)))],.018,'clay','Wheel',8)
    return center


def setup():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    for name in ['Ground','Water','Planting','Boundary','Fittings','Pond feed','Wheel','Rescue poses','Comfort poses','Section marks']:
        c=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(c);GROUPS[name]=c
    colors={
        'earth':(.072,.080,.039),'bed':(.16,.155,.095),
        'branch':(.090,.055,.022),'bamboo':(.28,.195,.078),'wood':(.22,.14,.058),
        'reed':(.19,.26,.048),'yellow':(.72,.52,.08),'lily':(.20,.285,.045),
        'petal':(.90,.87,.64),'metal':(.27,.31,.28),'clay':(.30,.07,.029),
        'leaf0':(.028,.087,.033),'leaf1':(.055,.14,.053),'leaf2':(.11,.18,.053),'leaf3':(.043,.12,.068),
        'timber0':(.14,.125,.07),'timber1':(.19,.164,.09),'timber2':(.12,.115,.065),
        'stone0':(.29,.26,.18),'stone1':(.35,.31,.21),'stone2':(.255,.26,.22),'stone3':(.39,.335,.235),'stone4':(.24,.225,.18),
        'pebble0':(.34,.33,.23),'pebble1':(.24,.235,.16),'pebble2':(.44,.41,.29),'pebble3':(.18,.19,.16),
        'proxy_cali':(.24,.43,.54),'proxy_kael':(.48,.26,.12),'proxy_lyra':(.67,.43,.16),
        'proxy_dog':(.52,.35,.14),'proxy_cat':(.065,.075,.065),'section':(.08,.25,.27),
    }
    for name,color in colors.items():
        stone=name.startswith(('stone','pebble'))
        material(name,color,.68 if stone else .8,.018 if stone else (.008 if name.startswith('timber') else 0),13 if stone else 4)
    m=material('water',(.035,.11,.066),.13,.008,145)
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Transmission Weight'].default_value=0;p.inputs['IOR'].default_value=1.333
    p.inputs['Alpha'].default_value=.17
    m.blend_method='BLEND';m.use_screen_refraction=False;m.show_transparent_back=False
    m=material('stream',(.50,.67,.62),.08)
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Alpha'].default_value=.4
    m.blend_method='BLEND'
    m=material('glow',(.1,.60,.75),.3)
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(.06,.6,1,1);p.inputs['Emission Strength'].default_value=2.5
    s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
    s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=64
    s.eevee.use_gtao=True;s.eevee.gtao_distance=2;s.eevee.gtao_factor=1.1
    s.eevee.use_soft_shadows=True;s.eevee.use_ssr=True;s.eevee.use_ssr_refraction=True
    s.render.resolution_x=1672;s.render.resolution_y=941;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.render.film_transparent=False
    s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast'
    s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.19,.25,.16,1)
    s.world.node_tree.nodes['Background'].inputs[1].default_value=.4
    for name,pos,energy,size,color in [('Warm opening',(-3,-4,6),420,3,(1,.83,.54)),('Sky fill',(3,-1,5),180,4,(.66,.83,1)),('Back canopy',(0,.5,5),110,2,(.9,1,.65))]:
        d=bpy.data.lights.new(name,'AREA');d.energy=energy;d.shape='DISK';d.size=size;d.color=color;d.use_shadow=True;d.use_contact_shadow=True
        o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=pos
        o.rotation_euler=(Vector((0,-1,0))-o.location).to_track_quat('-Z','Y').to_euler()


def camera(name,position,target,fov=62,ortho=None):
    data=bpy.data.cameras.new(name);data.clip_start=.04;data.clip_end=200
    data.sensor_fit='HORIZONTAL';data.angle=math.radians(fov)
    if ortho:data.type='ORTHO';data.ortho_scale=ortho
    o=bpy.data.objects.new(name,data);bpy.context.scene.collection.objects.link(o);o.location=position
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    if name in SOURCE_PATHS:
        im=bpy.data.images.load(str(ROOT/SOURCE_PATHS[name]),check_existing=True)
        im.filepath=str(ROOT/SOURCE_PATHS[name])
        if not im.packed_file:im.pack()
        data.show_background_images=False;bg=data.background_images.new();bg.image=im;bg.alpha=.35;bg.display_depth='FRONT'
    CAMERAS[name]=o
    return o


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--render',default='all');parser.add_argument('--percent',type=int,default=100)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    inputs={name:render_set.sha(HERE/name) for name in ('build_pond.py','actions.py','section.py','render_set.py','surface_detail.py','lighting.py','paving.py','paving_cells.py','aquatic_detail.py','stone_scan.py','wheel_detail.py')}
    inputs.update({str(p.relative_to(HERE)):render_set.sha(p) for p in (HERE/'textures').glob('*.jpg')})
    setup();ground();aquatic_detail.apply(sys.modules[__name__]);planting();wheel=fittings()
    surface_detail.apply(sys.modules[__name__])
    stone_scan.apply(sys.modules[__name__])
    wheel_report=wheel_detail.apply(sys.modules[__name__])
    action_report=actions.build(sys.modules[__name__])
    for (group,mat),(vertices,faces) in LEAF_BATCHES.items():mesh('Leaf blades / '+mat,vertices,faces,mat,group,True)
    lighting.apply(sys.modules[__name__])
    aim=CAMERA+Vector((0,math.cos(PITCH),-math.sin(PITCH)))*4
    camera('pond',CAMERA,aim);camera('wheel',CAMERA,aim)
    camera('overview',(7,-9,8),(0,-1.2,.2),58)
    section_report=section.build(sys.modules[__name__])
    scene=bpy.context.scene;scene.render.resolution_percentage=args.percent
    bpy.context.view_layer.update()
    hidden_default={'Wheel','Rescue poses','Comfort poses','Section marks'}
    for name,group in GROUPS.items():
        group.hide_render=name in hidden_default
        for ob in group.objects:ob.hide_set(name in hidden_default)
    scene.camera=CAMERAS['pond']
    scene['status']='Standalone VN reconstruction study; dimensions proposed, visual review required'
    scene['source_priority']='Current VN images; root AGENTS.md controls workflow'
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=='VIEW_3D':
                area.spaces.active.region_3d.view_perspective='CAMERA'
                area.spaces.active.clip_end=200
                area.spaces.active.shading.type='MATERIAL'
    for im in bpy.data.images:
        if im.source=='FILE' and not im.packed_file:im.pack()
    work=render_set.stage();(work/'renders').mkdir()
    bpy.ops.wm.save_as_mainfile(filepath=str(work/'pond-study.blend'),compress=True)
    # Render the saved scene itself, so the downloadable file is the source
    # of every published view rather than an earlier in-memory snapshot.
    bpy.ops.wm.open_mainfile(filepath=str(work/'pond-study.blend'))
    scene=bpy.context.scene
    for name in list(GROUPS):GROUPS[name]=bpy.data.collections[name]
    for name in list(CAMERAS):CAMERAS[name]=bpy.data.objects[name]
    bpy.context.view_layer.update()
    common_hash=render_set.geometry_hash(GROUPS)
    selected=['pond','wheel','overview','section','rescue','comfort'] if args.render=='all' else args.render.split(',')
    for name in selected:
        if name not in CAMERAS:continue
        for group,collection in GROUPS.items():
            hidden=(group!='Section marks') if name=='section' else (
                group=='Section marks' or group=='Wheel' and name!='wheel' or
                group=='Pond feed' and name=='wheel' or group=='Rescue poses' and name!='rescue' or
                group=='Comfort poses' and name!='comfort')
            collection.hide_render=hidden
            for ob in collection.objects:ob.hide_set(False)
        if render_set.geometry_hash(GROUPS)!=common_hash:raise RuntimeError('Shared geometry changed before rendering '+name)
        scene.camera=CAMERAS[name];scene.render.filepath=str(work/'renders'/f'{name}.png')
        bpy.ops.render.render(write_still=True)
    report={'status':'Reconstruction study; visual acceptance remains open','camera_assumption':{'position_m':list(CAMERA),'pitch_degrees':23,'horizontal_fov_degrees':62},'shoreline_bounds_m':{'width':max(p.x for p in SHORE)-min(p.x for p in SHORE),'depth':max(p.y for p in SHORE)-min(p.y for p in SHORE)},'water_level_m':WATER_Z,'proposed_bed_range_m':[-.318,-.202],'source_sha256':{k:hashlib.sha256((ROOT/v).read_bytes()).hexdigest() for k,v in SOURCE_PATHS.items()},'trace_uv':TRACE,'section':section_report,'paving':PAVING_CHECKS,'wheel_fittings':wheel_report}
    (work/'study.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (work/'action-checks.json').write_text(json.dumps(action_report,ensure_ascii=False,indent=2)+'\n')
    if args.render=='all':
        manifest=render_set.publish(HERE,work,selected,common_hash,inputs)
        for file in ('study.json','action-checks.json'):
            (HERE/file).write_text((HERE/'builds'/manifest['build_id']/file).read_text())
        print('PUBLISHED_RENDER_SET',manifest['build_id'])
    else:print('PRIVATE_PREVIEW_ONLY',str(work))
    print('POND_STUDY',json.dumps(report['shoreline_bounds_m']))


if __name__=='__main__':main()
