"""Weathering, joint fill and overhead growth for the VN pond fragment."""
import math
import json
import bpy
from mathutils import Vector


def _stone_finish(m):
    """World-sized grain and darker mineral flecks break up the broad slabs."""
    for index in range(5):
        mat=m.MATERIALS['stone'+str(index)]
        nodes=mat.node_tree.nodes;links=mat.node_tree.links
        p=nodes.get('Principled BSDF');base=mat.diffuse_color[:3]
        coord=nodes.new('ShaderNodeNewGeometry')
        broad=nodes.new('ShaderNodeTexNoise')
        broad.inputs['Scale'].default_value=11;broad.inputs['Detail'].default_value=5
        links.new(coord.outputs['Position'],broad.inputs['Vector'])
        ramp=nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].position=.32
        ramp.color_ramp.elements[0].color=(*(c*.35 for c in base),1)
        ramp.color_ramp.elements[1].position=.69
        ramp.color_ramp.elements[1].color=(*(c*1.10 for c in base),1)
        links.new(broad.outputs['Fac'],ramp.inputs[0])
        fleck=nodes.new('ShaderNodeTexNoise')
        fleck.inputs['Scale'].default_value=115;fleck.inputs['Detail'].default_value=2
        links.new(coord.outputs['Position'],fleck.inputs['Vector'])
        grains=nodes.new('ShaderNodeValToRGB')
        grains.color_ramp.elements[0].position=.27
        grains.color_ramp.elements[0].color=(.10,.085,.06,1)
        grains.color_ramp.elements[1].position=.42
        grains.color_ramp.elements[1].color=(1,1,1,1)
        links.new(fleck.outputs['Fac'],grains.inputs[0])
        mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.85
        links.new(ramp.outputs[0],mix.inputs[1]);links.new(grains.outputs[0],mix.inputs[2])
        links.new(mix.outputs[0],p.inputs['Base Color'])
        relief=nodes.new('ShaderNodeBump');relief.inputs['Strength'].default_value=.65
        relief.inputs['Distance'].default_value=.023
        links.new(broad.outputs['Fac'],relief.inputs['Height'])
        fine=nodes.new('ShaderNodeBump');fine.inputs['Strength'].default_value=.42
        fine.inputs['Distance'].default_value=.003
        links.new(fleck.outputs['Fac'],fine.inputs['Height']);links.new(relief.outputs[0],fine.inputs['Normal'])
        links.new(fine.outputs[0],p.inputs['Normal'])
        p.inputs['Roughness'].default_value=.72
    earth=m.MATERIALS['earth'].node_tree.nodes.get('Principled BSDF')
    earth.inputs['Base Color'].default_value=(.027,.033,.015,1)


def _layered_growth(m):
    """Compose distinct margins, low ferns, taller sprays and hanging growth."""
    rng=m.RNG
    # Plants reach the far coping instead of sitting behind a strip of bare soil.
    for i in range(19):
        x=-2.6+i*.28+rng.uniform(-.1,.1);y=-.22+rng.uniform(-.05,.10)
        if m.inside((x,y)):continue
        m.shrub((x,y,-.015),rng.uniform(.22,.42),rng.uniform(.18,.34),fern=i%2==0)
    # The reference has an irregular high spray left of the central iris,
    # and smaller open silhouettes across the darker timber background.
    for x,y,h,spread in [(-.90,.20,1.18,.32),(-1.60,.36,.82,.4),
                         (.74,.16,.76,.35),(1.55,.29,1.08,.35),(-2.60,.25,1.35,.5)]:
        base=Vector((x,y,-.01))
        for stem in range(7):
            angle=stem*2.4
            end=base+Vector((math.cos(angle)*spread,math.sin(angle)*spread,h*rng.uniform(.65,1)))
            m.tube('Open upper planting spray',[base,base.lerp(end,.55),end],[.006,.004,.0015],'vine',sides=5)
            for j in range(6):
                t=.35+j*.105;p=base.lerp(end,t)
                for sign in (-1,1):
                    m.leaf(p,(math.cos(angle+sign*1.1),math.sin(angle+sign*1.1),.12),
                           rng.uniform(.09,.16),rng.uniform(.018,.035),'leaf'+str(rng.randrange(4)))
    # Uneven hanging vines over the central enclosure, with gaps that expose
    # weathered boards. Each leaf is attached to a descending living stem.
    for i in range(33):
        x=-1.1+i*.075+rng.uniform(-.035,.035);high=1.48+rng.uniform(-.10,.22)
        low=.38+.53*abs(math.sin(i*.17+.6))+rng.uniform(-.1,.12)
        points=[(x+.075*math.sin(j*.55+i),1.08-.06*math.sin(j*.4),high+(low-high)*j/15) for j in range(16)]
        m.tube('Trailing canopy vine',points,[.006-j*.00024 for j in range(16)],'vine',sides=5)
        for j,p in enumerate(points):
            for sign in (-1,1):
                if rng.random()<.16:continue
                length=rng.uniform(.06,.15)
                m.leaf(p,(sign*rng.uniform(.1,.8),rng.uniform(-.7,-.25),rng.uniform(-1,.05)),
                       length,length*rng.uniform(.22,.43),'leaf'+str((i+j)%4))
    # Small emergent shoots interrupt selected stretches of the far waterline.
    # Their roots are in the shallow bed; the bank remains accessible at front.
    for i in range(18):
        t=.28+i*.022;p=m.contour(t,-rng.uniform(.025,.08),-.20)
        if p.y<m.CENTER.y:continue
        for j in range(5):
            a=j*2.4
            m.leaf(p,(math.cos(a)*.18,math.sin(a)*.18,1),rng.uniform(.22,.32),.004,'reed')
    # Fine arching grass enters the side margins and supplies a smaller scale
    # beside broad leaves, rather than repeating the same shrub everywhere.
    for side in (-1,1):
        for i in range(10):
            y=-.4-i*.25;x=side*(2.03+.14*math.cos(i))
            if m.inside((x,y)):x+=side*.22
            for j in range(13):
                angle=j*2.4;h=rng.uniform(.22,.52)
                m.leaf((x+rng.uniform(-.09,.09),y+rng.uniform(-.08,.08),-.01),
                       (math.cos(angle)*.4,math.sin(angle)*.4,1),h,.0045,'reed')


def apply(m):
    rng=m.RNG
    # Keep the garden's joint bed almost flush with the walking stones.
    ob=bpy.data.objects['Continuous garden ground around the water']
    for v in ob.data.vertices:v.co.z=-.012
    m.material('moss',(.075,.11,.027),.9,.004,80)
    m.material('joint rubble',(.19,.175,.115),.85,.008,35)
    m.material('vine',(.065,.10,.031),.8)
    _stone_finish(m)
    _layered_growth(m)
    # Pebbles have independent orientations and asymmetry rather than sharing
    # the same aligned oval silhouette beneath the clear foreground water.
    from mathutils import Matrix, noise
    for pebble in m.GROUPS['Ground'].objects:
        if not pebble.name.startswith('Submerged pebble'):continue
        center=sum((v.co for v in pebble.data.vertices),Vector())/len(pebble.data.vertices)
        rotation=Matrix.Rotation(rng.uniform(0,math.tau),3,'Z')
        for vertex in pebble.data.vertices:
            relative=vertex.co-center
            variation=1+.12*noise.noise(vertex.co*37)
            vertex.co=center+rotation@(relative*variation)
    rough=bpy.data.textures.new('Stone worn relief',type='CLOUDS')
    rough.noise_scale=.11;rough.noise_depth=2
    for ob in list(m.GROUPS['Ground'].objects):
        if ob.get('surface')!='dry paving':continue
        for mod in list(ob.modifiers):
            if mod.type=='WEIGHTED_NORMAL':ob.modifiers.remove(mod)
        subdiv=ob.modifiers.new('Stone surface relief mesh','SUBSURF')
        subdiv.subdivision_type='SIMPLE';subdiv.levels=3;subdiv.render_levels=3
        d=ob.modifiers.new('Worn stone surface','DISPLACE');d.texture=rough
        d.texture_coords='GLOBAL';d.direction='Z';d.strength=.016;d.mid_level=.52
        for face in ob.data.polygons:face.use_smooth=False
    # Fine aggregate belongs to the ground between slabs, not a raised border.
    for i in range(950):
        x=rng.uniform(-3.3,3.3);y=rng.uniform(-6,-.3)
        if m.inside((x,y)):continue
        if y>m.CENTER.y+.25:continue
        z=-.012;r=rng.uniform(.008,.024)
        m.sphere('Garden joint aggregate',(x,y,z),(r,r*.72,r*.43),'joint rubble',segments=7,rings=4)
    # Root the small ground cover in actual joints, then let its leaves spread
    # across the slabs. A random point on a stone face is not a planting pocket.
    paving_edges=[]
    for stone in m.GROUPS['Ground'].objects:
        if not stone.get('footprint_xy'):continue
        poly=json.loads(stone['footprint_xy'])
        area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1]))
        for a,b in zip(poly,poly[1:]+poly[:1]):
            a=Vector((*a,0));b=Vector((*b,0));delta=b-a
            outward=Vector((delta.y,-delta.x,0)).normalized()*(1 if area>0 else -1)
            paving_edges.append((a,b,outward))
    for i in range(75):
        t=rng.random();p=m.contour(t,rng.uniform(.34,.70),.005)
        if p.y<m.CENTER.y-.75 and rng.random()<.83:continue
        choices=[]
        for a,b,outward in paving_edges:
            fraction=max(0,min(1,(p-a).dot(b-a)/(b-a).length_squared))
            point=a.lerp(b,fraction);choices.append(((point-p).length_squared,point+outward*.004))
        p=min(choices,key=lambda item:item[0])[1];p.z=-.008
        for j in range(8):
            a=j*2.4;length=rng.uniform(.035,.08)
            m.leaf(p,(math.cos(a),math.sin(a),.38),length,length*.3,'moss')
    # Slender vines climb and hang across irregular parts of the timber plane.
    for i,(x,low,high) in enumerate([(-3.4,.2,2.2),(-2.6,.45,2.1),(-1.7,.4,1.8),(-.65,.15,1.55),(.7,.55,2.2),(1.55,.1,1.95),(2.45,.2,2.1),(3.3,.3,2.2)]):
        points=[]
        for j in range(17):
            z=low+(high-low)*j/16
            points.append((x+.17*math.sin(j*.42+i),1.17-.035*math.sin(j*.7),z))
        m.tube('Climbing boundary vine',points,[.008-j*.00032 for j in range(17)],'vine',sides=5)
        for j,p in enumerate(points[1:]):
            for side in (-1,1):
                m.leaf(p,(side*.8,-.5,-.25),rng.uniform(.065,.13),.033,'leaf'+str((j+i)%4))
    # The dapple pattern is cast by real leaves on connected overhead boughs.
    boughs=[([(-3.0,-.1,2.1),(-2.5,-1.7,2.65),(-1.5,-3.3,3.0),(-.8,-4.5,3.15)],[.08,.06,.035,.012]),
            ([(3.05,.1,2.4),(2.55,-1.2,2.8),(1.5,-3,3.0),(.3,-3.8,3.1)],[.08,.06,.035,.012])]
    for points,radii in boughs:m.tube('Overhead shade bough',points,radii)
    segments=[(Vector(a),Vector(b)) for points,_ in boughs for a,b in zip(points,points[1:])]
    for cx,cy,cz in [(-2.4,-1.5,2.7),(-1.4,-3.3,3),(-.7,-4.5,3.15),(2.2,-1.7,2.9),(1.2,-3.1,3.0)]:
        center=Vector((cx,cy,cz));anchors=[]
        for a,b in segments:
            t=max(0,min(1,(center-a).dot(b-a)/(b-a).length_squared))
            anchors.append(a.lerp(b,t))
        anchor=min(anchors,key=lambda p:(p-center).length_squared)
        for i in range(14):
            angle=i*2.4;reach=rng.uniform(.42,.84)
            tip=center+Vector((math.cos(angle)*reach,math.sin(angle)*reach,rng.uniform(-.12,.12)))
            m.tube('Canopy twig attached to shade bough',[anchor,anchor.lerp(tip,.55),tip],[.007,.004,.001],'branch',sides=5)
            for j in range(7):
                p=anchor.lerp(tip,.22+j*.12)
                for side in (-1,1):
                    length=rng.uniform(.075,.14)
                    m.leaf(p,(math.cos(angle+side*1.1),math.sin(angle+side*1.1),rng.uniform(-.2,.2)),length,length*.29,'leaf'+str((i+j)%4))
    # Timber grain varies along a board rather than forming uniform flat panels.
    for name in ('timber0','timber1','timber2','wood','bamboo','branch'):
        mat=m.MATERIALS[name];nodes=mat.node_tree.nodes;links=mat.node_tree.links
        p=nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.72
        tex=nodes.new('ShaderNodeTexCoord');mapping=nodes.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY'
        mapping.inputs[1].default_value=(24,12,.8)
        noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=3.5;noise.inputs['Detail'].default_value=4
        links.new(tex.outputs['Generated'],mapping.inputs[0]);links.new(mapping.outputs[0],noise.inputs['Vector'])
        ramp=nodes.new('ShaderNodeValToRGB');base=mat.diffuse_color[:3]
        ramp.color_ramp.elements[0].position=.2;ramp.color_ramp.elements[0].color=(*(v*.45 for v in base),1)
        ramp.color_ramp.elements[1].position=.8;ramp.color_ramp.elements[1].color=(*(v*1.35 for v in base),1)
        links.new(noise.outputs['Fac'],ramp.inputs[0]);links.new(ramp.outputs[0],p.inputs['Base Color'])
        bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.75;bump.inputs['Distance'].default_value=.010
        links.new(noise.outputs['Fac'],bump.inputs['Height']);links.new(bump.outputs[0],p.inputs['Normal'])
    # Thin leaves transmit a little filtered light, with a restrained waxy sheen.
    for name in ('leaf0','leaf1','leaf2','leaf3','reed','moss'):
        mat=m.MATERIALS[name];nodes=mat.node_tree.nodes;links=mat.node_tree.links
        p=nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.53
        p.inputs['Specular IOR Level'].default_value=.25
        translucent=nodes.new('ShaderNodeBsdfTranslucent');translucent.inputs['Color'].default_value=mat.diffuse_color
        mix=nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=.20
        links.new(p.outputs[0],mix.inputs[1]);links.new(translucent.outputs[0],mix.inputs[2])
        links.new(mix.outputs[0],nodes.get('Material Output').inputs['Surface'])
