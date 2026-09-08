"""Articulated scale studies for the VN pond rescue and recovery.

The builder supplies the actual pond and ground. Poses use proposed child
proportions, rather than treating the painted figures as measured anatomy.
"""

import math

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def _v(value):
    return Vector(value)


def _xyz(value):
    return [round(float(x), 5) for x in value]


class Actions:
    def __init__(self, model):
        self.m = model
        self.supports = []
        self.arms = []
        self.contacts = []
        self.joints = {}
        self.heights = {"Cali": 1.25, "Kael": 1.38, "Lyra": 1.03}
        bpy.context.view_layer.update()
        depsgraph = bpy.context.evaluated_depsgraph_get()
        verts, faces, owners = [], [], []
        for obj in sorted(model.GROUPS['Ground'].objects, key=lambda o: o.name):
            if obj.type != 'MESH':
                continue
            evaluated = obj.evaluated_get(depsgraph)
            data = evaluated.to_mesh()
            try:
                data.calc_loop_triangles()
                offset = len(verts)
                verts.extend(evaluated.matrix_world @ vertex.co for vertex in data.vertices)
                faces.extend(tuple(offset + i for i in triangle.vertices) for triangle in data.loop_triangles)
                owners.extend([obj.name] * len(data.loop_triangles))
            finally:
                evaluated.to_mesh_clear()
        self.ground = BVHTree.FromPolygons(verts, faces, all_triangles=True)
        self.owners = owners

    def ground_point(self, xy):
        p = _v(xy)
        hit, normal, index, _distance = self.ground.ray_cast(_v((p.x, p.y, 3)), _v((0, 0, -1)), 5)
        if hit is None or normal.z < .25:
            raise ValueError(f"No upward ground surface at {_xyz(p)}")
        return hit, self.owners[index]

    def pad(self, name, point, size, mat, group, wet=False):
        """Place a knee, boot, paw or seat onto the evaluated supporting mesh."""
        surface, owner = self.ground_point(point)
        center = surface + _v((0, 0, size[2]))
        obj = self.m.sphere(name, center, size, mat, group, segments=12, rings=8)
        bottom = min(vertex.co.z for vertex in obj.data.vertices)
        inside = bool(self.m.inside((surface.x, surface.y)))
        dryness = surface.z > self.m.WATER_Z + .008 and not inside
        status = 'pass' if abs(bottom - surface.z) < .002 and (wet or dryness) else 'fail'
        self.supports.append({
            'name': name, 'status': status, 'surface': owner,
            'contact_m': _xyz(surface), 'mesh_bottom_m': round(bottom, 5),
            'water_level_m': self.m.WATER_Z, 'dry_required': not wet,
        })
        return center

    def segment(self, name, a, b, radius, mat, group):
        return self.m.tube(name, [_xyz(a), _xyz(b)], radius, mat, group, sides=10)

    @staticmethod
    def endpoints(obj):
        # Read the two actual mesh end rings. This also detects a helper changing
        # the created bone position or scale after the IK coordinates were set.
        points=[obj.matrix_world @ vertex.co for vertex in obj.data.vertices]
        return sum(points[:10], Vector())/10, sum(points[-10:], Vector())/10

    def arm(self, name, shoulder, hand, upper, lower, pole, mat, group):
        """Solve a two-segment arm and check the resulting joint distances."""
        shoulder, hand, pole = _v(shoulder), _v(hand), _v(pole)
        delta = hand - shoulder
        distance = delta.length
        direction = delta.normalized()
        bend = pole - direction * pole.dot(direction)
        if bend.length < .001:
            bend = direction.cross(_v((0, 0, 1)))
        bend.normalize()
        reachable = abs(upper - lower) + .001 < distance < upper + lower - .001
        along = (upper * upper - lower * lower + distance * distance) / (2 * max(distance, .0001))
        height = math.sqrt(max(0, upper * upper - along * along))
        elbow = shoulder + direction * along + bend * height
        upper_mesh=self.segment(name + ' upper arm', shoulder, elbow, .041, mat, group)
        lower_mesh=self.segment(name + ' forearm', elbow, hand, .034, mat, group)
        self.m.sphere(name + ' elbow', elbow, (.044, .044, .044), mat, group)
        self.m.sphere(name + ' hand', hand, (.040, .032, .028), mat, group)
        upper_start,upper_end=self.endpoints(upper_mesh)
        lower_start,lower_end=self.endpoints(lower_mesh)
        actual_upper, actual_lower = (upper_end-upper_start).length, (lower_end-lower_start).length
        elbow_gap=(upper_end-lower_start).length
        good = reachable and max(abs(actual_upper-upper), abs(actual_lower-lower),elbow_gap) < .002
        self.arms.append({
            'name': name, 'status': 'pass' if good else 'fail',
            'shoulder_m': _xyz(shoulder), 'elbow_m': _xyz(elbow), 'hand_m': _xyz(hand),
            'proposed_segments_m': [round(upper, 4), round(lower, 4)],
            'measured_segments_m': [round(actual_upper, 4), round(actual_lower, 4)],
            'shoulder_to_hand_m': round(distance, 4),
            'mesh_elbow_gap_m':round(elbow_gap,6),
        })
        self.joints[name] = lower_end

    def body(self, name, hip, shoulder, forward, across, height, mat, group):
        hip, shoulder = _v(hip), _v(shoulder)
        self.m.tube(name + ' torso', [_xyz(hip), _xyz(hip.lerp(shoulder, .48)), _xyz(shoulder)],
                    [.115*height, .090*height, .112*height], mat, group, sides=12)
        head = shoulder + _v((0, 0, .16*height)) + forward*.035
        self.segment(name + ' neck', shoulder, head, .041*height, mat, group)
        self.m.sphere(name + ' head', head, (.080*height, .074*height, .10*height), mat, group,
                      segments=16, rings=10)
        # A small nose indicates gaze without inventing faces or costumes.
        self.m.sphere(name + ' gaze', head + forward*.072*height,
                      (.018*height, .018*height, .020*height), mat, group)
        return [shoulder + across*sign*.105*height for sign in (-1, 1)]

    def knees(self, name, anchor, forward, across, mat, group, wet=False, scale=1):
        joints = []
        for sign in (-1, 1):
            knee = self.pad(name + (' left knee' if sign < 0 else ' right knee'),
                            anchor + across*sign*.105*scale + forward*.15*scale,
                            (.073*scale, .087*scale, .060*scale), mat, group, wet)
            foot = self.pad(name + (' left boot' if sign < 0 else ' right boot'),
                            anchor + across*sign*.12*scale - forward*.20*scale,
                            (.067*scale, .12*scale, .046*scale), mat, group, wet)
            self.segment(name + ' folded lower leg', knee, foot, .055*scale, mat, group)
            joints.append(knee)
        return joints

    def animal(self, name, point, forward, group, cat=False, seated=False):
        mat = 'proxy_cat' if cat else 'proxy_dog'
        scale = .43 if cat else 1
        p = _v(point)
        across = _v((-forward.y, forward.x, 0))
        if cat:
            # Keep all four small paws on stone, including their perimeter,
            # rather than accepting a center that falls into a paving joint.
            offsets=sorted(((a*.03,b*.03) for a in range(-4,5) for b in range(-4,5)),key=lambda q:q[0]**2+q[1]**2)
            placed=False
            for dx,dy in offsets:
                candidate=p+forward*dx+across*dy;good=True
                for along in (-1,1):
                    for side in (-1,1):
                        paw=candidate+forward*along*.25*scale+across*side*.11*scale
                        center_hit,owner=self.ground_point(paw)
                        if not owner.startswith('Fitted garden flagstone'):good=False;break
                        for i in range(12):
                            angle=i*math.tau/12
                            q=paw+_v((.060*scale*math.cos(angle),.080*scale*math.sin(angle),0))
                            hit,edge_owner=self.ground_point(q)
                            if edge_owner!=owner or abs(hit.z-center_hit.z)>.008:good=False;break
                        if not good:break
                    if not good:break
                if good:
                    p=candidate;placed=True;break
            if not placed:raise ValueError(name+' needs a dry position clear of stone joints')
        height = self.ground_point(p)[0].z
        if seated:
            base = self.pad(name+' seated hindquarters', p, (.19, .23, .15), mat, group)
            neck = base + forward*.10 + _v((0, 0, .43))
            self.m.tube(name+' seated body', [_xyz(base), _xyz(neck)], [.22, .16], mat, group, sides=12)
            for sign in (-1, 1):
                paw = self.pad(name+' front paw', p+forward*.26+across*sign*.11,
                               (.070, .095, .05), mat, group)
                self.segment(name+' front leg', neck+across*sign*.1, paw, .052, mat, group)
        else:
            center = p + _v((0, 0, height+.45*scale))
            neck = center + forward*.29*scale + _v((0, 0, .13*scale))
            self.m.tube(name+' body', [_xyz(center-forward*.28*scale), _xyz(neck)],
                        [.18*scale, .15*scale], mat, group, sides=12)
            for along in (-1, 1):
                for side in (-1, 1):
                    xy=p+forward*along*.25*scale+across*side*.11*scale
                    paw=self.pad(name+' paw', xy, (.060*scale, .080*scale, .035*scale), mat, group)
                    self.segment(name+' leg', paw, paw+_v((0, 0, .36*scale)), .037*scale, mat, group)
        head=neck+forward*.10*scale+_v((0, 0, .10*scale))
        self.m.sphere(name+' head', head, (.12*scale, .11*scale, .13*scale), mat, group)
        self.m.sphere(name+' muzzle', head+forward*.12*scale, (.075*scale, .075*scale, .05*scale), mat, group)
        for sign in (-1, 1):
            self.m.sphere(name+' ear', head+across*sign*.11*scale+_v((0, 0, (-.04 if not cat else .1)*scale)),
                          (.045*scale, .04*scale, .10*scale), mat, group)
        tail_base=p-forward*.26*scale+_v((0, 0, height+.35*scale))
        self.m.tube(name+' tail', [_xyz(tail_base), _xyz(tail_base-forward*.28*scale+_v((0, 0, .18*scale))),
                                 _xyz(tail_base-forward*.40*scale+_v((0, 0, .26*scale)))],
                    [.045*scale, .027*scale, .006*scale], mat, group)

    def rescue(self):
        group='Rescue poses'
        shore=self.m.outline(.915);shore.z=0
        forward=(self.m.CENTER-shore);forward.z=0;forward.normalize()
        across=_v((-forward.y, forward.x, 0))
        lyra_anchor=shore+forward*.27
        lyra_floor=self.ground_point(lyra_anchor)[0].z
        targets=[shore+forward*.08+across*sign*.115+_v((0, 0, .38)) for sign in (-1, 1)]
        for name,sign,index in [('Cali',-1,0),('Kael',1,1)]:
            h=self.heights[name];mat='proxy_'+name.lower();scale=h/1.25
            anchor=shore-forward*.43+across*sign*.29
            knees=self.knees('Rescue '+name, anchor, forward, across, mat, group, scale=scale)
            floor=self.ground_point(anchor)[0].z
            hip=anchor+_v((0, 0, .31*scale+floor))
            shoulder=anchor+forward*.30+_v((0, 0, .57*scale+floor))
            for side,knee in zip((-1,1),knees):
                self.segment('Rescue '+name+' thigh',hip+across*side*.095*scale,knee,.075*scale,mat,group)
            shoulders=self.body('Rescue '+name,hip,shoulder,forward,across,h,mat,group)
            inner=1 if sign<0 else 0
            for side,origin in enumerate(shoulders):
                goal=targets[index] if side==inner else targets[index]+across*sign*.085+_v((0,0,.06))
                label='Rescue '+name+(' contact' if side==inner else ' free hand')
                self.arm(label,origin,goal,.205*h,.19*h,across*sign-_v((0,0,.5)),mat,group)
        mat='proxy_lyra';h=self.heights['Lyra']
        knees=self.knees('Rescue Lyra',lyra_anchor, -forward, across,mat,group,wet=True,scale=.83)
        hip=lyra_anchor+_v((0,0,lyra_floor+.20))
        shoulder=lyra_anchor-forward*.02+_v((0,0,lyra_floor+.55))
        for side,knee in zip((-1,1),knees):
            self.segment('Rescue Lyra thigh',hip+across*side*.08,knee,.058,mat,group)
        shoulders=self.body('Rescue Lyra',hip,shoulder,-forward,across,h,mat,group)
        for i,(origin,goal) in enumerate(zip(shoulders,targets)):
            self.arm('Rescue Lyra hand '+str(i),origin,goal,.205*h,.19*h,
                     across*(-1 if i==0 else 1)+_v((0,0,.2)),mat,group)
        for i,name in enumerate(('Cali','Kael')):
            a=self.joints['Rescue '+name+' contact'];b=self.joints['Rescue Lyra hand '+str(i)]
            gap=(a-b).length
            self.contacts.append({'name':name+' holds Lyra’s hand','status':'pass' if gap<.002 else 'fail',
                                  'contact_m':_xyz(a),'hand_center_gap_m':round(gap,6)})
        self.animal('Rescue Barkley',shore-forward*1.10+across*.22,forward,group)
        self.animal('Rescue Shadow',shore-forward*.75-across*.66,across,group,cat=True)
        self.m.camera('rescue',shore-forward*.15-across*2.8+_v((0,0,1.45)),
                      shore+forward*.02+_v((0,0,.38)),62)

    def comfort(self):
        group='Comfort poses';forward=_v((0,-1,0));across=_v((1,0,0))
        center=self.m.contour(.015,1.10,0)
        poses={}
        for name,offset in [('Cali',(-.35,.05,0)),('Lyra',(0,-.03,0)),('Kael',(.43,.13,0))]:
            h=self.heights[name];mat='proxy_'+name.lower();p=center+_v(offset)
            scale=h/1.25
            knees=self.knees('Comfort '+name,p,forward,across,mat,group,scale=scale)
            floor=self.ground_point(p)[0].z
            hip=p+_v((0,0,floor+.29*scale))
            shoulder=p+forward*.045+_v((0,0,floor+.63*scale))
            for sign,knee in zip((-1,1),knees):
                self.segment('Comfort '+name+' thigh',hip+across*sign*.09,knee,.068*scale,mat,group)
            shoulders=self.body('Comfort '+name,hip,shoulder,forward,across,h,mat,group)
            poses[name]=(p,shoulders)
        lyra_p=poses['Lyra'][0];z=self.ground_point(lyra_p)[0].z
        goals={
            'Cali':[lyra_p+_v((-.13,-.05,z+.40)),lyra_p+_v((.08,.01,z+.53))],
            'Kael':[lyra_p+_v((.18,.02,z+.44)),poses['Kael'][0]+_v((.15,-.12,z+.36))],
            'Lyra':[lyra_p+_v((-.055,-.17,z+.28)),lyra_p+_v((.07,-.16,z+.28))],
        }
        for name,(_p,shoulders) in poses.items():
            h=self.heights[name]
            for i,(origin,goal) in enumerate(zip(shoulders,goals[name])):
                self.arm('Comfort '+name+' arm '+str(i),origin,goal,.205*h,.19*h,
                         across*(-1 if i==0 else 1)+_v((0,0,-.2)),'proxy_'+name.lower(),group)
        self.animal('Comfort Barkley',center+_v((-1.02,.18,0)),forward,group,seated=True)
        self.animal('Comfort Shadow',center+_v((1.12,.05,0)),forward,group,cat=True)
        self.m.camera('comfort',center+_v((.10,-3.35,1.38)),center+_v((.08,.25,.50)),62)

    def report(self):
        failures=[item for item in self.supports+self.arms+self.contacts if item['status']=='fail']
        return {
            'status':'fail' if failures else 'pass-with-open-motion-review',
            'scope':'Static articulated rescue and comfort poses on the reconstructed pond ground.',
            'proposed_reference_heights_m':self.heights,
            'ground_contacts':self.supports,'arm_reach':self.arms,'hand_contacts':self.contacts,
            'open':[
                'Continuous lifting and climbing from water to paving are not animated or dynamically tested.',
                'Balance, joint rotation limits, grip forces and load capacity require further review.',
                'The animal shapes establish scale and paw support, not a validated gait.',
                'Whole-body collision and cloth deformation are not tested by joint-distance and support checks.',
                'Camera compositions are independent views guided by the VN images, not a claim of exact image matching.',
            ],
        }


def build(model_module):
    """Build both separate pose groups and return measured static evidence."""
    study=Actions(model_module)
    study.rescue()
    study.comfort()
    return study.report()
