#!/usr/bin/env python3
"""Compose later furnishings and afternoon window light with existing people preserved."""
import argparse,io,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
from repair_treehouse_environments import PROJECT,REPO,SIZE,SOURCES,mask,compose,rgba,sha
from build_treehouse_states import material_pointer,save_xcf
from project_treehouse_exterior import VIEWS
from relight_treehouse_states import forest_light

EXTERIOR_ENVELOPES=[
 [[841,83],[930,103],[953,278],[902,301],[877,299],[842,219]],
 [[969,67],[1073,63],[1178,119],[1234,168],[1243,439],[984,434],[975,281]],
 [[1287,70],[1347,24],[1398,0],[1671,0],[1671,492],[1295,438]],
]

FULL_FOLIAGE=[
 [[866,123],[883,132],[899,151],[901,180],[900,267],[865,265],[861,247],[866,224],[864,197],[865,163]],
 [[1007,139],[1036,139],[1068,121],[1080,154],[1102,208],[1135,240],[1148,250],[1146,274],[985,274],[986,238],[994,193]],
 [[1187,121],[1226,139],[1227,280],[1195,280],[1190,269],[1175,256],[1174,242],[1179,204],[1184,177]],
 [[1196,291],[1228,298],[1228,346],[1204,345]],
]

def run(install=False,xcf=False):
    blob=VIEWS['cassia-comfort']['lighting_source_blob']
    raw=subprocess.check_output(['git','cat-file','blob',blob],cwd=REPO)
    original=Image.open(io.BytesIO(raw)).convert('RGB')
    near=Image.open(PROJECT/'art/production/cassia-comfort-near-exterior.png')
    furnishings=Image.open(PROJECT/'art/production/cassia-comfort-later-furnishings.png')
    base=compose(original,near,furnishings)
    pixels=np.asarray(base,dtype=float)
    known=np.asarray(mask(VIEWS['cassia-comfort']['openings'],.8),dtype=float)/255
    envelope=np.asarray(mask(EXTERIOR_ENVELOPES,.8),dtype=float)/255
    cool=np.clip((np.minimum(pixels[:,:,1],pixels[:,:,2])-pixels[:,:,0]-3)/10,0,1)
    known=np.maximum(known,np.asarray(mask(FULL_FOLIAGE,1.4),dtype=float)/255)
    outside=np.maximum(known*(1-np.asarray(furnishings.getchannel('A'),dtype=float)/255),envelope*cool)
    day=Image.fromarray(np.clip(forest_light(base)*255,0,255).astype(np.uint8))
    layer=rgba(day,Image.fromarray(np.round(outside*255).astype(np.uint8)))
    candidate=compose(base,layer)
    out=PROJECT/'build/graphics/environments/states';out.mkdir(parents=True,exist_ok=True)
    candidate.save(out/'comfort_day.png')
    layer.save(out/'comfort-daylight-layer.png')
    diff=np.any(np.asarray(base)!=np.asarray(candidate),axis=2)
    assert not np.any(diff & (outside==0))
    # This rectangle contains both faces and the joined hands; furniture masks
    # independently exclude the rightmost outfit silhouettes below the windows.
    assert not np.any(diff[:,:835])
    changed=np.any(np.asarray(original)!=np.asarray(candidate),axis=2)
    support=(np.asarray(near.getchannel('A'))>0)|(np.asarray(furnishings.getchannel('A'))>0)|(outside>0)
    assert not np.any(changed & ~support)
    assert not np.any(changed[:,:835])
    if xcf:
        layerdir=out/'comfort-layers';layerdir.mkdir(exist_ok=True)
        layers=[]
        for name,picture in [('01-original-accepted-people',original),('02-shared-near-branches',near),('03-later-furnishings',furnishings),('04-afternoon-window-light',layer)]:
            path=layerdir/(name+'.png');picture.save(path);layers.append((name,path,True))
        save_xcf(layers,out/'cassia-comfort.xcf')
    if install:
        file='game/images/cg/book-one/cassia-comfort.png'
        (PROJECT/file).write_bytes((out/'comfort_day.png').read_bytes())
        recipe={
            'id':'treehouse-comfort-later-daylight','file':file,'source_generation':'review-027-cassia-comfort',
            'sources':[{'file':file,'git_blob':blob,'sha256':sha(raw)},SOURCES['room']]+[
                {'file':f,'sha256':sha((PROJECT/f).read_bytes())} for f in ['art/production/cassia-comfort-near-exterior.png','art/production/cassia-comfort-later-furnishings.png']],
            'operations':['Retained shared nearby fork layer from selected original room',
                          'Bounded later table/stools/textiles and vacated floor footprint; existing people preserved',
                          'Green afternoon light through complete open-air foliage contours; lamp/curtain/rail remain sheltered'],
            'mask_geometry':{'nearby_forks':'docs/treehouse-exterior-rig.json','later_furniture':'docs/comfort-furnishings.json',
                             'openings':VIEWS['cassia-comfort']['openings'],'complete_foliage':FULL_FOLIAGE,'hue_extension_envelopes':EXTERIOR_ENVELOPES,
                             'feather_px':{'openings':.8,'foliage_contours':1.4},'protected_faces_and_hands_rectangle':[0,0,835,941]},
            'output_sha256':sha((out/'comfort_day.png').read_bytes()),'dimensions':list(SIZE),'mode':'RGB',
            'script_file':'scripts/relight_treehouse_comfort.py','script_sha256':sha(Path(__file__).read_bytes()),
            'dependencies':[{'file':f,'sha256':sha((PROJECT/f).read_bytes())} for f in ['scripts/build_treehouse_states.py','scripts/relight_treehouse_states.py','scripts/repair_treehouse_environments.py','scripts/project_treehouse_exterior.py']],
            'material_provenance':[material_pointer('art/production/cassia-comfort-later-furnishings.png')],
            'verification':{'changed_pixels':int(changed.sum()),'outside_mask_pixels_changed':0,'outside_mask_identical':True,
                            'canvas_and_mode_unchanged':True,'geometry_resampled':False,'protected_faces_and_joined_hands_pixels_changed':0}
        }
        register=PROJECT/'docs/environment-edits.json';data=json.loads(register.read_text())
        data['edits']=[r for r in data['edits'] if r['id'] not in ['treehouse-comfort-near-landmarks',recipe['id']]]+[recipe]
        register.write_text(json.dumps(data,indent=2)+'\n')
        print(json.dumps({'installed':file,'sha256':recipe['output_sha256'],'changed_pixels':recipe['verification']['changed_pixels']}))
    return original,base,layer,candidate,outside

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--install',action='store_true');parser.add_argument('--xcf',action='store_true')
    args=parser.parse_args();run(args.install,args.xcf)
