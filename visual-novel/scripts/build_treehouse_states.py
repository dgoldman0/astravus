#!/usr/bin/env python3
"""Build four chronologically dressed daylight/rain rooms with editable layers."""
import argparse, hashlib, json, os, subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image
from repair_treehouse_environments import PROJECT,SIZE,SOURCES,EARLY_PAPERS,LATER_PAPERS,OPENINGS,source_images,compose,rgba,mask,sha
from relight_treehouse_states import relight_room

OUTPUTS=[
 ('early_day','treehouse-early-daylight','game/images/backgrounds/treehouse-shaded.png','treehouse-shaded-v1'),
 ('early_rain','treehouse-early-rain-afternoon','game/images/backgrounds/treehouse-rain.png','treehouse-rain-v1'),
 ('later_day','treehouse-later-daylight','game/images/backgrounds/book-one/treehouse-later.png','treehouse-shaded-v1'),
 ('memory_rain','treehouse-memory-rain-afternoon','game/images/backgrounds/book-one/treehouse-memory.png','book-one-treehouse-memory-v1'),
]

def correction_layer(base,target):
    """A translucent ordinary RGBA color layer, not an opaque final-image layer.

    The smallest admissible alpha per pixel permits both brighter and darker
    target channels. One 8-bit unit of output tolerance is retained in the XCF;
    runtime PNGs use the direct lighting function and are exact/reproducible.
    """
    b=np.asarray(base,dtype=float);t=np.asarray(target,dtype=float);delta=t-b
    lower=np.where(delta>=0,delta/np.maximum(255-b,1),-delta/np.maximum(b,1))
    a=np.minimum(1,np.max(lower,axis=2)+1/255)
    a=np.ceil(a*255)/255
    a[np.all(delta==0,axis=2)]=0
    color=b+delta/np.maximum(a[:,:,None],1/255)
    out=np.concatenate([np.round(np.clip(color,0,255)),(a*255)[:,:,None]],axis=2).astype(np.uint8)
    layer=Image.fromarray(out)
    rebuilt=compose(base,layer)
    error=int(np.abs(np.asarray(rebuilt,dtype=int)-np.asarray(target,dtype=int)).max())
    assert error<=1
    return layer,error

def save_xcf(layers,destination):
    first=layers[0][1]
    q=lambda p:json.dumps(str(p))
    code=[f'(let* ((img (car (gimp-file-load RUN-NONINTERACTIVE {q(first)} {q(first)}))) (base (car (gimp-image-get-active-layer img))))',f'(gimp-item-set-name base {q(layers[0][0])})']
    for name,path,visible in layers[1:]:
        code.append(f'(let ((layer (car (gimp-file-load-layer RUN-NONINTERACTIVE img {q(path)})))) (gimp-image-insert-layer img layer 0 0) (gimp-layer-set-mode layer 0) (gimp-item-set-name layer {q(name)}) (gimp-item-set-visible layer {"TRUE" if visible else "FALSE"}))')
    code += [f'(gimp-xcf-save RUN-NONINTERACTIVE img (car (gimp-image-get-active-layer img)) {q(destination)} {q(destination)})','(gimp-image-delete img))','(gimp-quit 0)']
    with tempfile.TemporaryDirectory(prefix='astravus-state-xcf-') as tmp:
        scheme=Path(tmp)/'layers.scm';scheme.write_text('\n'.join(code)+'\n')
        env=dict(os.environ,GIMP2_DIRECTORY=str(Path(tmp)/'profile'))
        subprocess.run(['gimp','--no-interface','--new-instance','--no-data','--no-fonts','--no-splash','--no-shm','--console-messages','--batch-interpreter=plug-in-script-fu-eval','--batch',f'(load {q(scheme)})'],env=env,check=True,timeout=90)
    assert destination.is_file()

def material_pointer(file):
    register='docs/graphics-sources/materials.json'
    entries=json.loads((PROJECT/register).read_text())['materials']
    entry=next(item for item in entries if item['generated_material']==file)
    return {'registry_file':register,'id':entry['id'],'record_sha256':sha(json.dumps(entry,sort_keys=True,separators=(',',':')).encode())}

def run(install=False,xcf=False):
    src=source_images();room=src['room']
    early_layer=rgba(src['papers'],mask(EARLY_PAPERS,.7))
    late_layer=rgba(src['papers'],mask(LATER_PAPERS,.7))
    furniture_file='art/production/treehouse-later-furnishings.png'
    furniture=Image.open(PROJECT/furniture_file)
    early=compose(room,early_layer);later=compose(early,furniture);memory=compose(later,late_layer)
    bases={'early_day':early,'early_rain':early,'later_day':later,'memory_rain':memory}
    out=PROJECT/'build/graphics/environments/states';out.mkdir(parents=True,exist_ok=True)
    layerdir=out/'layers';layerdir.mkdir(exist_ok=True)
    layers=[]
    for name,picture in [('01-original-room',room),('02-early-wall-drawings',early_layer),('03-later-movable-furniture',furniture),('04-remembrance-wall-drawings',late_layer)]:
        path=layerdir/(name+'.png');picture.save(path);layers.append((name,path,True))
    recipes=[]
    for state,id_,file,generation in OUTPUTS:
        is_late=state in ['later_day','memory_rain'];is_rain=state.endswith('rain')
        picture=relight_room(bases[state],state,furniture.getchannel('A') if is_late else None)
        staged=out/(state+'.png');picture.save(staged)
        color,error=correction_layer(bases[state],picture)
        layerfile=layerdir/(state+'-light-weather.png');color.save(layerfile)
        layers.append((state+' light/weather — enable only one',layerfile,state=='memory_rain'))
        if install:
            destination=PROJECT/file;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(staged.read_bytes())
        sources=list(SOURCES.values())
        if is_late:sources.append({'file':furniture_file,'sha256':sha((PROJECT/furniture_file).read_bytes())})
        recipe={
            'id':id_,'file':file,'source_generation':generation,'sources':sources,
            'operations':['Existing early wall drawings at original coordinates','Whole-room daylight/overcast lighting; source geometry is not resampled',
                          'Selective exterior leaf/branch palette and broad window illumination']+
                         (['Moved worktable, two stools, map holder and evolved textiles through bounded furniture material'] if is_late else [])+
                         (['Later wall drawings/messages, including remembered waterwheel; no old-table paper overlay'] if state=='memory_rain' else [])+
                         (['Exterior mist, wet ridge highlights and depth-varied antialiased rain'] if is_rain else []),
            'mask_geometry':{'early_papers':EARLY_PAPERS,'later_papers':LATER_PAPERS if state=='memory_rain' else [],'exterior_openings':OPENINGS,
                             'exterior_hue_extension':'Explicit architectural envelopes in relight_treehouse_states.py; furniture opacity subtracts foreground occlusion',
                             'whole_room_light_scope':'Full canvas color/midtone change; no claim of unchanged interior pixels',
                             'furniture_recipe':'docs/treehouse-furnishings.json' if is_late else None,'state':state,'rain_seed':9131 if state=='memory_rain' else 8117 if is_rain else None},
            'output_sha256':sha(staged.read_bytes()),'dimensions':list(SIZE),'mode':'RGB',
            'script_file':'scripts/build_treehouse_states.py','script_sha256':sha(Path(__file__).read_bytes()),
            'dependencies':[{'file':file_,'sha256':sha((PROJECT/file_).read_bytes())} for file_ in ['scripts/relight_treehouse_states.py','scripts/repair_treehouse_environments.py']],
            'verification':{'changed_pixels':int(np.count_nonzero(np.any(np.asarray(room)!=np.asarray(picture),axis=2))),
                            'canvas_and_mode_unchanged':True,'fixed_architecture_geometry_resampled':False,
                            'lighting_affects_whole_room':True,'xcf_layer_reconstruction_max_channel_error':error}
        }
        if is_late:recipe['material_provenance']=[material_pointer(furniture_file)]
        recipes.append(recipe)
    if xcf:save_xcf(layers,out/'treehouse-states.xcf')
    register=PROJECT/'docs/environment-edits.json'
    data=json.loads(register.read_text())
    obsolete={'treehouse-early-drawings','treehouse-rain-shared-room','treehouse-memory-shared-room'}|{item['id'] for item in recipes}
    data['edits']=[r for r in data['edits'] if r['id'] not in obsolete]+recipes
    data['method']='Bounded retained painting/material composition and explicit day/weather lighting; geometry and art acceptance are separate.'
    register.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'installed':install,'states':[{r['file']:r['output_sha256']} for r in recipes]},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--install',action='store_true');parser.add_argument('--xcf',action='store_true')
    args=parser.parse_args();run(args.install,args.xcf)
