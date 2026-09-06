"""Build Lumen's author-facing scale studies. Run with Blender 4.0.2.

The wiki owns numerical canon. Geometry below is disposable blocking, not
approved replacement art. Rebuilding overwrites only the generated outputs.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import sys

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "wiki/worldbuilding/lumen-layout.json"
DATA = json.loads(DATA_PATH.read_text())
PLACE = {p["id"]: Vector(p["xyz"]) for p in DATA["places"]}
MODEL = DATA["blockout"]
RNG = random.Random(17)
REPORT = {"layout_sha256": hashlib.sha256(DATA_PATH.read_bytes()).hexdigest(),
          "blender": bpy.app.version_string, "scope": "Measured blockout, not a finished reconstruction",
          "routes": [], "checks": [], "surface_reservations_m2": {}}


def collection(name):
    c = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c


def material(name, color, emission=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    shader = m.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1)
    shader.inputs["Roughness"].default_value = .78
    shader.inputs["Emission Color"].default_value = (*color, 1)
    shader.inputs["Emission Strength"].default_value = emission
    return m


def mesh(name, verts, faces, mat, group):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    ob = bpy.data.objects.new(name, data)
    group.objects.link(ob)
    if mat:
        data.materials.append(mat)
    return ob


def box(name, center, size, mat, group):
    x, y, z = center
    a, b, c = (v / 2 for v in size)
    verts = [(x+i*a, y+j*b, z+k*c) for k in (-1, 1)
             for j in (-1, 1) for i in (-1, 1)]
    return mesh(name, verts, [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4),
                             (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)], mat, group)


def line(name, points, radius, mat, group, cyclic=False):
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    data.resolution_u = 1
    data.bevel_depth = radius
    data.bevel_resolution = 1
    data.use_fill_caps = True
    data.resolution_u = 1
    spline = data.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for p, co in zip(spline.points, points):
        p.co = (*co, 1)
    spline.use_cyclic_u = cyclic
    data.materials.append(mat)
    ob = bpy.data.objects.new(name, data)
    group.objects.link(ob)
    return ob


def ellipsoid(name, center, scale, mat, group):
    verts, faces = [], []
    for j in range(9):
        lat = -math.pi / 2 + math.pi * j / 8
        for i in range(16):
            a = math.tau * i / 16
            verts.append((center[0]+scale[0]*math.cos(lat)*math.cos(a),
                          center[1]+scale[1]*math.cos(lat)*math.sin(a),
                          center[2]+scale[2]*math.sin(lat)))
    for j in range(8):
        for i in range(16):
            k, n = j*16+i, j*16+(i+1)%16
            faces.append((k, n, n+16, k+16))
    return mesh(name, verts, faces, mat, group)


def disk(name, center, radii, mat, group, n=48):
    return mesh(name, [(center[0]+radii[0]*math.cos(i*math.tau/n),
                        center[1]+radii[1]*math.sin(i*math.tau/n), center[2])
                       for i in range(n)], [tuple(range(n))], mat, group)


def ring(name, center, inner, outer, mat, group, n=48):
    verts = [(center[0]+r[0]*math.cos(i*math.tau/n),
              center[1]+r[1]*math.sin(i*math.tau/n), center[2])
             for r in (inner, outer) for i in range(n)]
    return mesh(name, verts, [(i, (i+1)%n, (i+1)%n+n, i+n) for i in range(n)], mat, group)


def text_label(name, position, size, group, mat=None):
    data = bpy.data.curves.new(name, "FONT")
    data.body, data.size = name, size
    ob = bpy.data.objects.new(name, data)
    ob.location = position
    group.objects.link(ob)
    data.materials.append(mat or M["ink"])
    return ob


def tree(name, ground, height, radius, group, canopy=True):
    p = Vector(ground)
    line(name+" trunk", [p, p+Vector((height*.06, 0, height*.7))], radius*.14, M["wood"], group)
    for i in range(3):
        a = i*math.tau/3
        q = p+Vector((math.cos(a)*radius*.55, math.sin(a)*radius*.55, height*.78))
        line(name+" branch", [p+Vector((0, 0, height*.42)), q], radius*.055, M["wood"], group)
        if canopy:
            ellipsoid(name+" canopy", q, (radius*.8, radius*.8, height*.24), M["leaf"], group)


def person(name, ground, height, group):
    x, y, z = ground
    box(name+" body", (x, y, z+height*.52), (height*.23, height*.17, height*.55), M["human"], group)
    ellipsoid(name+" head", (x, y, z+height*.9), (height*.1,)*3, M["human"], group)
    for dx in (-height*.07, height*.07):
        line(name+" leg", [(x+dx,y,z), (x+dx,y,z+height*.4)], height*.045, M["human"], group)


def arch(name, foot, width, height, radius, group):
    x, y, z = foot
    pts = [(x-width/2, y, z), (x-width/2, y, z+height-width/2)]
    pts += [(x+width/2*math.cos(a), y, z+height-width/2+width/2*math.sin(a))
            for a in [math.pi-i*math.pi/16 for i in range(17)]]
    pts += [(x+width/2, y, z)]
    return line(name, pts, radius, M["stone"], group)


def camera(name, eye, target, group, ortho=None, lens=30):
    data = bpy.data.cameras.new(name)
    data.clip_start, data.clip_end = .05, 20000
    data.lens = lens
    if ortho:
        data.type, data.ortho_scale = "ORTHO", ortho
    ob = bpy.data.objects.new(name, data)
    group.objects.link(ob)
    rotation = (Vector(target)-Vector(eye)).to_track_quat("-Z", "Y")
    ob.matrix_world = Matrix.Translation(Vector(eye)) @ rotation.to_matrix().to_4x4()
    return ob


def check(name, result, **detail):
    REPORT["checks"].append({"name": name, "passed": bool(result), **detail})


def route_geometry():
    for r in DATA["routes"]:
        points = [Vector(p) for p in r["waypoints"]]
        group = LATER if r["to"] == "P17" else ROUTES
        approach = sum((b-a).length for a, b in zip(points, points[1:]))
        grades = []
        for a, b in zip(points, points[1:]):
            d = b-a
            lateral = Vector((-d.y, d.x, 0)).normalized()*3
            # A supported graded path, with earth/tissue beneath its walking ribbon.
            verts = [tuple(p) for p in (a-lateral, a+lateral, b+lateral, b-lateral)]
            verts += [(x,y,-2) for x,y,z in verts]
            mesh(r["from"]+" to "+r["to"], verts,
                 [(0,1,2,3),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)], M["path"], group)
            grades.append(abs(d.z)/max(Vector((d.x,d.y)).length, .001))
        REPORT["routes"].append({"from": r["from"], "to": r["to"],
                                 "target_m": r["length"], "measured_walk_m": round(approach,1),
                                 "walking_minutes": round(approach/DATA["walking_metres_per_minute"],1),
                                 "max_segment_grade_percent": round(max(grades)*100,1),
                                 "extra": "55 m scaffold ascent" if r["to"] == "P12" else ""})
        check(r["to"]+" route target", abs(approach-r["length"])/r["length"] < .12)
        check(r["to"]+" path grade", max(grades) < .085)


def body_geometry():
    b = DATA["body"]
    rx, ry, rz = b["width"]/2, b["length"]/2, b["depth"]/2
    cz = (b["bottom_z"]+b["top_z"])/2
    for latitude in (-60,-30,0,30,60):
        a = math.radians(latitude)
        line("Body envelope latitude", [(rx*math.cos(a)*math.cos(t), ry*math.cos(a)*math.sin(t), cz+rz*math.sin(a))
             for t in [i*math.tau/96 for i in range(96)]], 3, M["wire"], ENVELOPE, True)
    for a in (0, math.pi/2):
        line("Body envelope meridian", [(rx*math.cos(a)*math.cos(t),ry*math.sin(a)*math.cos(t),cz+rz*math.sin(t))
             for t in [i*math.tau/96 for i in range(96)]], 3, M["wire"], ENVELOPE, True)
    # Area trays are allocations, not literal identical decks or finished farms.
    for row in MODEL["support_reservations"]:
        for z in row["levels"]:
            ob = box(row["use"]+" reservation", (*row["xy"],z-1), (*row["size"],2), M[row["material"]], SUPPORT)
            area = row["size"][0]*row["size"][1]
            REPORT["surface_reservations_m2"][row["use"]] = REPORT["surface_reservations_m2"].get(row["use"],0)+area
            # Reserve the full service headroom as well as the surface itself.
            bound = max((x/rx)**2+(y/ry)**2+((zz-cz)/rz)**2
                        for x in [row["xy"][0]-row["size"][0]/2,row["xy"][0]+row["size"][0]/2]
                        for y in [row["xy"][1]-row["size"][1]/2,row["xy"][1]+row["size"][1]/2]
                        for zz in [z-2,z+row["headroom"]])
            check(row["use"]+" envelope clearance at "+str(z), bound < 1, ellipsoid_fraction=round(bound,3))
            ob["net_reserved_area_m2"], ob["use"] = area, row["use"]
    line("Arrival connection", [(0,-1000,0),(0,-1750,0)],18,M["transport"],SUPPORT)
    for side in (-1,1):
        line("Side-facing docking access", [(0,-1750,0),(side*570,-1750,0)],25,M["transport"],SUPPORT)
    ellipsoid("Aft drive volume - mechanism open", (0,-2140,100),(250,170,130),M["systems"],SUPPORT)
    for p in DATA["places"]:
        if p["id"] != "P17":
            text_label(p["id"]+" "+p["name"], (p["xyz"][0]+12,p["xyz"][1]+10,p["xyz"][2]+65),17,LABELS)


def city_geometry():
    box("Main chamber basal landscape proxy", (0,200,-8),(1400,2400,16),M["ground"],CITY)
    g = DATA["maia_garden"]
    box("Maia garden terrace", ((g["x_min"]+g["x_max"])/2,(g["y_min"]+g["y_max"])/2,10),
        (g["x_max"]-g["x_min"],g["y_max"]-g["y_min"],20),M["garden"],CITY)
    # Perimeter masses express occupied terraces. They are not a dwelling census.
    path_segments = [(Vector(a),Vector(b)) for r in DATA["routes"] if r["to"] != "P17"
                     for a,b in zip(r["waypoints"],r["waypoints"][1:])]
    def path_distance(p):
        ans = 1e6
        for a,b in path_segments:
            v = Vector((b.x-a.x,b.y-a.y))
            q = Vector((p[0]-a.x,p[1]-a.y))
            t = max(0,min(1,q.dot(v)/max(v.length_squared,.001)))
            ans = min(ans,(q-t*v).length)
        return ans
    for x in range(-620,621,100):
        for y in range(-850,1251,150):
            if abs(x)<210 or (-540<x<-60 and 130<y<640):
                continue
            if path_distance((x,y))<42 or any((Vector((x,y,0))-Vector((p.x,p.y,0))).length<65 for p in PLACE.values()):
                continue
            z = 15+max(0,abs(x)-210)*.08
            # Leave a planted sight corridor between the dome and childhood garden.
            if y>450 and x>0 and x<400:
                continue
            box("Residential terrace",(x,y,z/2),(70,80,z),M["ground"],CITY)
            box("Habitation mass",(x,y,z+7),(46,55,14),M["home"],CITY)
            box("Planted roof",(x,y,z+14.5),(48,57,1),M["garden"],CITY)
            tree("Neighborhood tree",(x-25,y+24,z),20,12,CITY)
    for i in range(55):
        x,y = RNG.uniform(-495,-85),RNG.uniform(190,580)
        if min(math.hypot(x-PLACE[p].x,y-PLACE[p].y) for p in ("P02","P03","P04","P05"))>32 and path_distance((x,y))>12:
            tree("Garden canopy",(x,y,20),RNG.uniform(13,24),RNG.uniform(6,11),CITY)
    for key,w,d,h in [("P02",28,20,7),("P07",20,17,7),("P08",25,22,8),("P09",60,48,13),("P10",60,55,11),("P11",20,14,5)]:
        p=PLACE[key]
        box(key+" grounded terrace", (p.x,p.y,(p.z-1)/2),(w+12,d+12,p.z+1),M["ground"],CITY)
        box(key+" building mass",p+Vector((0,0,h/2)),(w,d,h),M["home"] if key!="P10" else M["civic"],CITY)
    p=PLACE["P05"]
    tree("P05 Tree of Echoes - separate transplanted tree",p,38,22,CITY)
    p=PLACE["P06"]
    disk("P06 storytelling circle",p+Vector((0,0,.05)),(14,12),M["stone"],CITY)
    # Main chamber ribs: renderable enclosure cues, not a pressure shell proof.
    for y in (-850,-350,250,850,1350):
        line("Chamber structural rib",[(680*math.cos(t),y,50+550*math.sin(t)) for t in [i*math.pi/32 for i in range(33)]],8,M["rib"],VAULT)
    p=PLACE["P12"]
    box("P12 overlook floor",p-Vector((0,0,.3)),(24,16,.6),M["stone"],CITY)
    box("P12 low front parapet",p+Vector((0,-8,.45)),(24,.55,.9),M["stone"],CITY)
    for side in (-1,1):
        line("P12 scaffold upright",[(p.x+side*11,p.y,30),(p.x+side*11,p.y,110)],.4,M["wood"],CITY)
    for i in range(11):
        a=Vector((350+(i%2)*3,1000+i*50/11,30+i*5))
        b=Vector((350+((i+1)%2)*3,1000+(i+1)*50/11,35+i*5))
        for dx in (-.65,.65):
            line("Scaffold ladder rail",[a+Vector((dx,0,0)),b+Vector((dx,0,0))],.06,M["wood"],CITY)
        for j in range(20):
            q=a.lerp(b,j/19)
            line("Scaffold rung",[q-Vector((.65,0,0)),q+Vector((.65,0,0))],.045,M["wood"],CITY)
        box("Scaffold landing",b-Vector((0,0,.1)),(3.8,3,.2),M["wood"],CITY)
    person("Dome adult scale",p+Vector((7,0,0)),1.7,CITY)


def treehouse_geometry():
    p=PLACE["P04"]
    def at(x,y,z): return tuple(p+Vector((x,y,z)))
    f=DATA["treehouse_upper_floor_above_local_ground"]
    disk("Lower refuge paving",at(-2,-2,.02),(8,7),M["stone"],TREE)
    trunk=line("Oak diagonal trunk",[at(0,0,0),at(1,0,5),at(3,1,15)],1.3,M["wood"],TREE)
    # Cut actual passages through the trunk; an arch drawn on solid wood is not access.
    bpy.ops.object.select_all(action="DESELECT")
    trunk.select_set(True)
    bpy.context.view_layer.objects.active=trunk
    bpy.ops.object.convert(target="MESH")
    for name,center,size in [
        ("Lower hollow void",at(.4,-.4,1.0),(1.5,3.2,2.2)),
        ("Upper entry passage",at(.15,-.5,f+1.1),(1.3,3.5,2.3)),
        ("Upper room connection",at(-.5,-.3,f+1.1),(2.2,1.4,2.3))]:
        cutter=box(name,center,size,None,TREE)
        modifier=trunk.modifiers.new(name,"BOOLEAN")
        modifier.operation="DIFFERENCE"
        modifier.object=cutter
        bpy.context.view_layer.objects.active=trunk
        bpy.ops.object.modifier_apply(modifier=modifier.name)
        bpy.data.objects.remove(cutter,do_unlink=True)
    for q in [(-7,2,11),(1,-6,13),(7,4,12)]:
        line("Oak load-bearing branch",[at(1,0,4),at(*q)],.42,M["wood"],TREE)
        ellipsoid("Oak canopy",at(*q),(6,5,3),M["leaf"],TREE)
    box("Upper room floor",at(-3.5,0,f-.13),(7,5,.26),M["wood"],TREE)
    box("Connected landing",at(.6,-1.6,f-.13),(1.3,2.2,.26),M["wood"],TREE)
    box("Door passage floor",at(.1,-.25,f-.13),(1.5,2.7,.26),M["wood"],TREE)
    box("Timber roof",at(-3.1,0,f+2.85),(9,6,.22),M["wood"],TREE)
    box("Upper back wall",at(-3.5,2.4,f+1.35),(7,.18,2.7),M["wood"],TREE)
    box("Upper left wall",at(-6.9,0,f+1.35),(.18,5,2.7),M["wood"],TREE)
    arch("Arched upper entrance",at(.15,-1.15,f),1.1,2.25,.10,TREE)
    arch("Separate lower hollow entrance",at(.4,-1.4,0),1.35,2.15,.13,TREE)
    # Open viewing bays. The geometry contains no glass.
    for x in (-6.8,-4.7,-2.6,-.5):
        line("Bay upright",[at(x,-2.45,f),at(x,-2.45,f+2.8)],.09,M["wood"],TREE)
        box("Scrap curtain",at(x+.2,-2.44,f+1.85),(.3,.08,1.8),M["fabric"],TREE)
    for z in (.45,1.05):
        line("Branch viewing rail",[at(-6.8,-2.45,f+z),at(-.5,-2.45,f+z)],.07,M["wood"],TREE)
    a,b=Vector(at(.6,-4,0)),Vector(at(.6,-2.55,f))
    for dx in (-.4,.4):
        line("Old ladder side",[a+Vector((dx,0,0)),b+Vector((dx,0,0))],.07,M["wood"],TREE)
    for i in range(18):
        q=a.lerp(b,i/17)
        line("Old ladder rung",[q-Vector((.4,0,0)),q+Vector((.4,0,0))],.045,M["wood"],TREE)
    disk("Round map table",at(-4.3,-.7,f+.5),(.85,.85),M["stone"],TREE)
    box("Map table support",at(-4.3,-.7,f+.25),(.2,.2,.5),M["wood"],TREE)
    for x,y in [(-5,1),(-2,1),(-5,-1.7)]:
        box("Upper cushion",at(x,y,f+.12),(1,.65,.24),M["fabric"],TREE)
    for x,y in [(-5,-4),(-3,-6),(1,-5),(3,-3)]:
        box("Lower refuge cushion",at(x,y,.15),(1.1,.7,.3),M["fabric"],TREE)
    person("Treehouse 1.3 m child scale",at(-2,0,f),1.3,TREE)
    check("Treehouse ladder meets landing", abs(b.z-(p.z+f))<.001 and -.5<=b.x-p.x<=1.25 and -2.7<=b.y-p.y<=-.5,
          upper_floor_m_above_ground=f, room_floor_m2=35, clear_door_width_m=1.1)
    bpy.context.view_layer.update()
    bvh=BVHTree.FromObject(trunk,bpy.context.evaluated_depsgraph_get())
    walk=[Vector(at(x,y,f+1.1)) for x,y in [(.6,-2.55),(.15,-1.6),(.15,-.3),(-1.4,-.3),(-2,-.3)]]
    clear=all(bvh.ray_cast(a,(b-a).normalized(),(b-a).length)[0] is None for a,b in zip(walk,walk[1:]))
    check("Treehouse trunk passage is open",clear,scope="Centreline at torso height from landing through trunk into room")


def pond_geometry():
    p=PLACE["P03"]
    def at(x,y,z): return tuple(p+Vector((x,y,z)))
    q=MODEL["pond"]
    rx,ry=q["radii"]
    ring("Broad dry working bank",at(0,0,0),(rx+.3,ry+.3),(13,11),M["stone"],POND)
    ring("Low coping",at(0,0,q["coping_above_bank"]),(rx,ry),(rx+.3,ry+.3),M["stone"],POND)
    disk("Connected shallow water",at(0,0,-q["water_below_bank"]),(rx,ry),M["water"],POND)
    disk("Pond bed",at(0,0,-q["water_below_bank"]-q["water_depth"]),(rx,ry),M["earth"],POND)
    for i in range(35):
        a,r=RNG.uniform(0,math.tau),RNG.uniform(.3,1)
        disk("Bed pebble study",at(rx*r*math.cos(a),ry*r*math.sin(a),-q["water_below_bank"]-q["water_depth"]+.04),(.14,.12),M["stone"],POND,12)
    for x in range(-8,9):
        box("Timber garden boundary",at(x,6,1.1),(.92,.15,2.2),M["wood"],POND)
        ellipsoid("Far planting",at(x,5,.8),(.8,.65,.9),M["leaf"],POND)
    line("Small supplied inlet",[at(-6,2,.2),at(-3.6,1.8,.15)],.09,M["wood"],POND)
    for i in range(7):
        disk("Right lily group",at(2+i*.18,.4+i*.12,-.105),(.3,.24),M["garden"],POND,16)
    for x,y in [(-7,-3),(-8,-2),(-6,-5)]:
        ellipsoid("Working-bank pot",at(x,y,.3),(.35,.35,.3),M["fabric"],POND)
    person("Pond 1.3 m child scale",at(-6,-4,0),1.3,POND)
    check("Pond reachable water and separate dry bank", q["water_below_bank"]+q["coping_above_bank"]<.3 and q["water_depth"]<=.5,
          water_depth_m=q["water_depth"], water_to_coping_m=q["water_below_bank"]+q["coping_above_bank"], near_bank_width_m=11-ry-.3)


def plaza_geometry():
    box("Main square",(0,0,-.2),(180,140,.4),M["stone"],PLAZA)
    for row in MODEL["plaza_crowd_zones"]:
        x,y,w,d=row["xy_size"]
        box("Clear gathering "+row["name"],(x,y,.015),(w,d,.02),M["crowd_area"],CAPACITY)
        if abs(x)>90:
            box("Connected gathering court",(x,y,-.2),(w,d,.4),M["stone"],PLAZA)
            box("Court approach",(x/2,y,-.2),(abs(x),12,.4),M["stone"],PLAZA)
    area=sum(r["xy_size"][2]*r["xy_size"][3] for r in MODEL["plaza_crowd_zones"])
    check("Plaza gathering allowance", area==20000, clear_m2=area, at_2_m2_per_person=int(area/2),
          limit="Geometric reservations; egress and crowd flow are not certified")
    sx,sy=MODEL["plaza_stage_xy"]
    disk("Familiar low stage",(sx,sy,.6),(6,4.5),M["stone"],PLAZA)
    for i in range(3):
        box("Stage step",(sx,sy-5-i*.5,.1+i*.15),(9,.6,.2+i*.3),M["stone"],PLAZA)
    tree("Plaza great tree",(-22,25,0),26,14,PLAZA)
    for i in range(30):
        a=math.radians(180-i*3.8)
        box("Curved tree stair",(-22+9*math.cos(a),25+9*math.sin(a),i*5.5/29-.17), (2.5,1.1,.34),M["stone"],PLAZA)
    box("Tree stair to rear terrace landing",(-19,40,5.3),(3,15,.4),M["stone"],PLAZA)
    for z in (0,5.5,11):
        box("Rear terrace floor",(0,48,z-.18),(86,10,.36),M["stone"],PLAZA)
        for x in range(-36,37,12):
            arch("Occupied rear arcade",(x,43,z),9,5,.38,PLAZA)
        for side in (-1,1):
            for y in (-5,7,19,31):
                a=arch("Side arcade",(0,0,z),9,5,.38,PLAZA)
                a.rotation_euler.z=math.pi/2
                a.location=(side*44,y,0)
            box("Side terrace",(side*48,18,z-.18),(9,58,.36),M["stone"],PLAZA)
    # Open central passage beneath a bridge: no wall closes the rear route.
    arch("Central rear passage",(0,42,0),9,5,.5,PLAZA)
    for x in range(-34,36,4):
        for y in range(-15,34,5):
            if (x+22)**2+(y-25)**2<120 or ((x-sx)/9)**2+((y-sy)/8)**2<1:
                continue
            person("Gathered resident scale",(x+RNG.uniform(-.6,.6),y,0),RNG.uniform(1.25,1.8),PLAZA)
    person("Performer scale",(sx,sy,.6),1.7,PLAZA)
    for x in range(-35,36,10):
        for y in range(-8,40,12):
            ellipsoid("Festival lantern",(x,y,8+RNG.uniform(0,4)),(.28,.28,.45),M["lantern"],FESTIVAL)


def study_scene(name, groups, cam, evening=False):
    scene=bpy.data.scenes.new(name)
    for c in groups+[CAMERAS,LIGHTS]:
        scene.collection.children.link(c)
    scene.unit_settings.system="METRIC"
    scene.unit_settings.scale_length=1
    scene.gravity=(0,0,-9.8)
    scene.camera=cam
    scene.render.engine="BLENDER_EEVEE"
    scene.eevee.taa_render_samples=32
    scene.eevee.use_gtao=True
    scene.eevee.gtao_distance=3
    scene.eevee.gtao_factor=1.15
    scene.render.resolution_x,scene.render.resolution_y=1280,800
    scene.render.image_settings.file_format="PNG"
    world=bpy.data.worlds.new(name+" sky")
    world.use_nodes=True
    world.node_tree.nodes["Background"].inputs[0].default_value=(.18,.25,.28,1) if not evening else (.035,.055,.10,1)
    world.node_tree.nodes["Background"].inputs[1].default_value=.7 if not evening else .15
    scene.world=world
    scene.view_settings.view_transform="AgX"
    scene["canon_source"]="../../wiki/worldbuilding/lumen-layout.json"
    scene["status"]="Author-facing scale study; local details remain modelling targets"
    return scene


def sightline_check(scene):
    # Test against the actual city meshes and curve meshes, excluding helpers.
    bpy.context.window.scene=scene
    bpy.context.view_layer.update()
    depsgraph=bpy.context.evaluated_depsgraph_get()
    verts,faces=[],[]
    for ob in scene.objects:
        if ob.type not in {"MESH","CURVE"}:
            continue
        evaluated=ob.evaluated_get(depsgraph)
        geom=evaluated.to_mesh()
        if geom:
            offset=len(verts)
            verts.extend(ob.matrix_world@v.co for v in geom.vertices)
            faces.extend(tuple(offset+i for i in poly.vertices) for poly in geom.polygons)
        evaluated.to_mesh_clear()
    bvh=BVHTree.FromPolygons(verts,faces)
    eye=scene.camera.location
    for name,point in [("home roof",(-300,180,27.1)),("central square",(0,-35,.1))]:
        v=Vector(point)-eye
        hit=bvh.ray_cast(eye,v.normalized(),v.length-.2)
        check("Dome view to "+name,hit[0] is None, distance_m=round(v.length,1),
              obstruction_distance_m=round(hit[3],1) if hit[0] is not None else None)
    visible=0
    for x in (-420,-365,-310,-255,-200):
        for y in (250,305,360,415,470):
            v=Vector((x,y,20.5))-eye
            visible+=bvh.ray_cast(eye,v.normalized(),v.length-.2)[0] is None
    check("Dome view across planted garden",visible>=9,visible_ground_samples=visible,total_samples=25,
          scope="Sparse canopy proxies; foliage may hide individual patches")


def main():
    global M, ENVELOPE,SUPPORT,CITY,VAULT,ROUTES,LABELS,LATER,TREE,POND,PLAZA,CAPACITY,FESTIVAL,CAMERAS,LIGHTS
    parser=argparse.ArgumentParser()
    parser.add_argument("--render",action="store_true")
    args=parser.parse_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    original=bpy.context.scene
    ENVELOPE,SUPPORT,CITY,VAULT,ROUTES,LABELS,LATER,TREE,POND,PLAZA,CAPACITY,FESTIVAL,CAMERAS,LIGHTS = [collection(n) for n in (
        "01 Body envelope (guide)","02 Supporting chambers (area reservations)","03 City and neighborhood",
        "04 Main chamber ribs","05 Walking routes","06 Author labels","07 Later growth only",
        "08 Treehouse study","09 Pond study","10 Plaza study","11 Clear gathering reservations",
        "12 Festival dressing","13 Cameras","14 Illumination")]
    colors={"ground":(.13,.24,.23),"garden":(.25,.43,.29),"stone":(.61,.55,.41),"wood":(.25,.13,.07),
            "leaf":(.16,.37,.27),"home":(.56,.43,.31),"civic":(.35,.52,.62),"systems":(.44,.32,.50),
            "cultivation":(.39,.61,.29),"transport":(.25,.55,.62),"reserve":(.55,.45,.23),
            "path":(.81,.66,.39),"wire":(.33,.62,.60),"ink":(.90,.89,.75),"rib":(.30,.35,.29),
            "human":(.85,.37,.16),"fabric":(.65,.25,.16),"water":(.12,.42,.51),"earth":(.23,.20,.13),
            "crowd_area":(.38,.70,.62),"lantern":(1,.47,.10)}
    M={k:material(k,v,3 if k=="lantern" else 0) for k,v in colors.items()}
    M["water"].blend_method="BLEND"
    M["water"].node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value=.5
    body_geometry()
    city_geometry()
    route_geometry()
    treehouse_geometry()
    pond_geometry()
    plaza_geometry()
    measured={}
    for ob in SUPPORT.objects:
        if "use" in ob:
            area=sum(face.area for face in ob.data.polygons if face.normal.z>.99)
            measured[ob["use"]]=measured.get(ob["use"],0)+area
    REPORT["surface_reservations_m2"]={k:round(v,1) for k,v in measured.items()}
    check("Measured net floor reservations match wiki budget",
          all(abs(measured.get(k,0)-v*1e6)<1 for k,v in DATA["surface_budget_km2"].items()),
          measured_total_m2=round(sum(measured.values()),1),
          scope="Packing of net areas within the envelope, not an assigned dwelling plan")
    gathering=sum(face.area for ob in CAPACITY.objects for face in ob.data.polygons if face.normal.z>.99)
    check("Measured clear gathering surfaces",abs(gathering-20000)<1,measured_area_m2=round(gathering,1))
    b=DATA["later_body"]
    line("Later body plan envelope",[(b["width"]/2*math.cos(t),b["plan_centre_y"]+b["length"]/2*math.sin(t),-25)
         for t in [i*math.tau/100 for i in range(100)]],5,M["reserve"],LATER,True)
    p=PLACE["P17"]
    box("Later Radiant Fields chamber",(p.x,p.y,15),(700,900,30),M["garden"],LATER)
    ring("Later Luxa arena reservation",p,(85,130),(110,160),M["civic"],LATER)
    for key in ("P15","P16"):
        p=PLACE[key]
        box(key+" later household",p+Vector((0,0,4)),(26,20,8),M["home"],LATER)
    # Neutral studio illumination serves measurement, rather than imitating final VN art.
    sun=bpy.data.lights.new("Maintained daylight study","SUN")
    sun.energy,sun.angle=2.3,.25
    ob=bpy.data.objects.new(sun.name,sun)
    LIGHTS.objects.link(ob)
    ob.rotation_euler=(.35,-.55,-.35)
    fill=bpy.data.lights.new("Soft architectural fill","SUN")
    fill.energy,fill.angle=.6,.5
    ob=bpy.data.objects.new(fill.name,fill)
    LIGHTS.objects.link(ob)
    ob.rotation_euler=(.4,.6,2)
    cams={}
    for name,row in MODEL["cameras"].items():
        cams[name]=camera(name,row["eye"],row["target"],CAMERAS,row.get("ortho"),row.get("lens",30))
    scenes=[
        study_scene("01 Body and support allocation",[ENVELOPE,SUPPORT,CITY,ROUTES,PLAZA,TREE],cams["world"]),
        study_scene("02 Childhood city",[CITY,VAULT,ROUTES,PLAZA,TREE,LABELS],cams["city"]),
        study_scene("03 Dome overlook",[CITY,VAULT,ROUTES,PLAZA,TREE],cams["dome"]),
        study_scene("04 Treehouse approach",[TREE],cams["treehouse"]),
        study_scene("05 Treehouse room",[TREE],cams["treehouse_interior"]),
        study_scene("06 Pond and bank",[POND],cams["pond"]),
        study_scene("07 Plaza performance area",[PLAZA,FESTIVAL],cams["plaza"],True),
        study_scene("08 Plaza capacity plan",[PLAZA,CAPACITY],cams["plaza_plan"]),
        study_scene("09 Later growth",[ENVELOPE,SUPPORT,CITY,ROUTES,PLAZA,TREE,LATER],cams["later"])]
    bpy.data.scenes.remove(original)
    sightline_check(scenes[2])
    # Screen coordinates verify handedness and framing, not an exact image match.
    for name,scene,points in [
        ("Plaza landmarks",scenes[6],[("tree",(-22,25,8)),("passage",(0,42,2)),("stage",(*MODEL["plaza_stage_xy"],1))]),
        ("Treehouse exterior",scenes[3],[("room",(-113.5,530,26)),("trunk",(-109,530,26)),("lower hollow",(-109.6,528.6,21))])]:
        bpy.context.window.scene=scene
        bpy.context.view_layer.update()
        projected={label:tuple(round(float(v),3) for v in world_to_camera_view(scene,scene.camera,Vector(p))) for label,p in points}
        check(name+" framing",all(0<v[0]<1 and 0<v[1]<1 and v[2]>0 for v in projected.values()), projected=projected)
        if name=="Plaza landmarks":
            check("Plaza left-to-right continuity",projected["tree"][0]<projected["passage"][0]<projected["stage"][0])
        else:
            check("Treehouse room projects left of trunk",projected["room"][0]<projected["trunk"][0])
    OUT.mkdir(exist_ok=True)
    bpy.context.window.scene=scenes[1]
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=="VIEW_3D":
                area.spaces.active.clip_end=20000
                area.spaces.active.region_3d.view_perspective="CAMERA"
                area.spaces.active.shading.color_type="MATERIAL"
    note=bpy.data.texts.new("START HERE")
    note.write("LUMEN | Working blockout\n1 Blender unit = 1 metre; gravity down = -Z.\nChoose scenes 01-09 for body, city, local studies and later growth.\nNumpad 0 enters the saved camera; Numpad . frames selected objects.\nWiki: wiki/worldbuilding/Lumen-Atlas.md and lumen-layout.json.\nSupport trays are net area reservations; decorative masses are not a dwelling count.\nMaterials and unmeasured details are study proxies, not VN replacement assets.\nSee world/lumen/README.md and validation.json for measured results and limits.\n")
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/"lumen-blockout.blend"),compress=True)
    (OUT/"validation.json").write_text(json.dumps(REPORT,indent=2)+"\n")
    if args.render:
        (OUT/"renders").mkdir(exist_ok=True)
        for scene in scenes:
            bpy.context.window.scene=scene
            scene.render.filepath=str(OUT/"renders"/(scene.camera.name+".png"))
            bpy.ops.render.render(write_still=True,scene=scene.name)
    failed=[r["name"] for r in REPORT["checks"] if not r["passed"]]
    print("LUMEN CHECKS:",len(REPORT["checks"]),"FAILED:",failed)
    if failed:
        raise RuntimeError("Blockout checks require review: "+", ".join(failed))


if __name__=="__main__":
    main()
