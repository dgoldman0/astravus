"""Partition a source-guided paving footprint into fitted stone polygons.

Runs under the host's Python with Shapely, independently of Blender's Python.
Input and output are geometry JSON on stdin/stdout; this generates no prose.
"""
import json
import math
import random
import sys

from shapely import voronoi_polygons
from shapely.geometry import MultiPoint, Polygon, box
from shapely.ops import unary_union


def partition(data):
    rng=random.Random(48261)
    pond=Polygon(data['shore'])
    # Only the immediate bank and the broader dry foreground are paved.
    # The pond silhouette is an input, never determined by this tessellation.
    domain=pond.buffer(.43,join_style=2).union(box(-4.2,-7.0,4.2,-2.65)).difference(pond)
    seeds=data['seeds'][:]
    for iy in range(15):
        for ix in range(19):
            x=-4.4+ix*.49+rng.uniform(-.13,.13)
            y=-7.15+iy*.48+rng.uniform(-.12,.12)
            if not domain.contains(MultiPoint([(x,y)])):continue
            if any((x-a)**2+(y-b)**2<.46**2 for a,b in seeds):continue
            seeds.append([x,y])
    cells=voronoi_polygons(MultiPoint(seeds),extend_to=domain.envelope,ordered=True)
    pieces=[]
    for cell in cells.geoms:
        clipped=cell.intersection(domain)
        for piece in (clipped.geoms if clipped.geom_type=='MultiPolygon' else [clipped]):
            if piece.is_empty or piece.area<1e-7:continue
            pieces.append(piece)
    if abs(unary_union(pieces).area-domain.area)>1e-6:
        raise ValueError('Unpartitioned paving area')
    stones=[];chipped_count=0
    for piece in pieces:
        inset=piece.buffer(-rng.uniform(.007,.010),join_style=2)
        for poly in (inset.geoms if inset.geom_type=='MultiPolygon' else [inset]):
            if poly.is_empty or poly.area<.006:continue
            # Retain the plan outline; long arc boundaries are simplified by
            # less than the joint width so stones have individual straight cuts.
            poly=poly.simplify(.003,preserve_topology=True)
            coords=list(poly.exterior.coords)[:-1]
            area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(coords,coords[1:]+coords[:1]))
            orientation=1 if area>0 else -1
            chipped=[]
            for a,b in zip(coords,coords[1:]+coords[:1]):
                dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
                chipped.append(a)
                if length<.13:continue
                for fraction in (.23,.48,.74):
                    cut=rng.uniform(.001,.011)
                    chipped.append((a[0]+dx*fraction-dy/length*cut*orientation,
                                    a[1]+dy*fraction+dx/length*cut*orientation))
            candidate=Polygon(chipped)
            # Weathering only cuts inward: it cannot cross a neighbor's joint.
            if candidate.is_valid and poly.buffer(1e-8).covers(candidate):
                poly=candidate;chipped_count+=1
            stones.append(poly)
    overlap=sum(a.intersection(b).area for i,a in enumerate(stones) for b in stones[i+1:])
    if overlap>1e-8:raise ValueError('Paving footprints overlap')
    shore_error=max((p.intersection(pond).area for p in stones),default=0)
    if shore_error>1e-8:raise ValueError('Paving extends into the proposed basin')
    return {'stones':[list(p.exterior.coords)[:-1] for p in stones],
            'checks':{'stone_count':len(stones),'chipped_stones':chipped_count,'overlap_area_m2':overlap,
                      'basin_intrusion_area_m2':shore_error,
                      'nominal_joint_width_m':[.014,.020],
                      'partition_area_m2':domain.area}}


if __name__=='__main__':
    print(json.dumps(partition(json.load(sys.stdin))))
