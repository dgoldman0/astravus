"""Fitted flagstones based on the pond outline and visible slab positions."""
import json
from pathlib import Path
import subprocess


def build(m):
    seeds=[]
    for i in range(30):
        t=(i+.5)/30;p=m.outline(t)
        if p.y<m.CENTER.y-.87:continue
        p=m.contour(t,.20)
        seeds.append([p.x,p.y])
    # Centers of broad slabs read in the VN foreground. The shared partition
    # reconciles them with the coping instead of placing intersecting polygons.
    for uv in [(.049,.711),(.178,.785),(.319,.830),(.470,.860),(.595,.849),
               (.744,.825),(.883,.748),(.045,.888),(.205,.947),(.367,.990),
               (.505,.984),(.644,.978),(.786,.974),(.939,.901)]:
        p=m.unproject(uv,0);seeds.append([p.x,p.y])
    shore=[[m.outline(i/168).x,m.outline(i/168).y] for i in range(168)]
    result=subprocess.run(['python3',str(Path(__file__).with_name('paving_cells.py'))],
                          input=json.dumps({'shore':shore,'seeds':seeds}),
                          text=True,capture_output=True,check=True)
    layout=json.loads(result.stdout)
    for i,poly in enumerate(layout['stones']):
        ob=m.prism('Fitted garden flagstone '+str(i),poly,m.RNG.uniform(-.004,.006),-.27,
                   'stone'+str(m.RNG.randrange(5)),bevel=.005)
        ob['surface']='dry paving'
        ob['source_shape']='Fitted partition guided by VN slab positions and shoreline'
        ob['footprint_xy']=json.dumps(poly)
    m.PAVING_CHECKS=layout['checks']
