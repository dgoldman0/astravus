#!/usr/bin/env python3
"""Retain only ground-level pond edge material; original people/props are locked."""
import argparse,hashlib,io,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[1];SIZE=(1672,941)
SPECS = {'garden-work-area': {'file': 'game/images/backgrounds/book-one/garden-work-area.png',
                      'blob': '886a5a98d7f746262fd19e250a5b8b112f198ad1',
                      'polygons': [[[550, 316], [606, 338], [730, 370], [919, 394], [1161, 409], [1399, 396],
                                    [1573, 351], [1671, 325], [1671, 537], [1522, 520], [1320, 491], [1100, 512],
                                    [864, 516], [739, 489], [650, 459], [535, 403]]],
                      'protected': [[[666, 497], [721, 496], [717, 544], [671, 544]],
                                    [[776, 532], [836, 532], [831, 573], [785, 573]],
                                    [[1015, 503], [1076, 500], [1073, 558], [1020, 558]],
                                    [[1100, 543], [1182, 548], [1178, 613], [1109, 608]],
                                    [[1185, 554], [1270, 554], [1268, 611], [1195, 611]],
                                    [[1313, 523], [1365, 522], [1361, 563], [1320, 562]]],
                      'prompt': 'docs/graphics-sources/pond-work-area-prompt.txt',
                      'vegetation_regions': [[[393, 423], [450, 418], [487, 435], [530, 437], [539, 486],
                                              [528, 522], [405, 522]],
                                             [[475, 359], [555, 375], [610, 420], [657, 464], [647, 518],
                                              [588, 520], [539, 493], [495, 454]],
                                             [[646, 426], [713, 426], [753, 473], [734, 529], [718, 551],
                                              [663, 551], [645, 518]],
                                             [[752, 471], [821, 473], [856, 506], [853, 557], [838, 580],
                                              [778, 580], [763, 549]],
                                             [[980, 415], [1059, 415], [1103, 453], [1104, 523], [1078, 565],
                                              [1014, 564], [997, 531]],
                                             [[1041, 482], [1104, 449], [1229, 431], [1328, 439], [1402, 467],
                                              [1412, 526], [1379, 564], [1319, 575], [1299, 608], [1164, 620],
                                              [1096, 616], [1083, 574], [1044, 550]]]},
 'garden-compromise': {'file': 'game/images/cg/book-one/garden-compromise.png',
                       'blob': 'e822f7ea1369bb94d5bc3af4cde312c965efeb84',
                       'polygons': [[[847, 353], [946, 359], [1070, 367], [1070, 500], [990, 620], [898, 620],
                                     [875, 582], [856, 451]],
                                    [[1217, 363], [1369, 379], [1518, 378], [1671, 346], [1671, 539], [1534, 537],
                                     [1434, 520], [1360, 535], [1328, 512], [1304, 475], [1265, 428]]],
                       'protected': [[[500, 0], [774, 0], [822, 149], [836, 252], [865, 330], [865, 360],
                                      [852, 382], [858, 414], [870, 466], [878, 523], [889, 559], [919, 581],
                                      [923, 627], [488, 627]],
                                     [[1030, 180], [1215, 184], [1260, 335], [1230, 348], [1250, 374], [1268, 398],
                                      [1294, 421], [1319, 445], [1341, 473], [1352, 495], [1362, 515], [1356, 547],
                                      [1370, 579], [1438, 660], [1286, 731], [931, 717], [940, 630], [954, 597],
                                      [969, 569], [977, 546], [985, 526], [979, 515], [986, 501], [990, 493],
                                      [998, 483], [1000, 475], [1013, 462], [1014, 452], [1024, 432], [1031, 410],
                                      [1037, 390], [1048, 370], [1055, 350], [1022, 327], [1011, 278]]],
                       'prompt': 'docs/graphics-sources/pond-compromise-prompt.txt'}}

def sha(b):return hashlib.sha256(b).hexdigest()
def polygon_mask(polygons):
 m=Image.new('L',SIZE);d=ImageDraw.Draw(m)
 for poly in polygons:d.polygon([tuple(p) for p in poly],fill=255)
 return m

def run(materials):
 out=ROOT/'build/graphics/pond-geometry';out.mkdir(parents=True,exist_ok=True);production=ROOT/'art/production';production.mkdir(exist_ok=True)
 records=[]
 for name,spec in SPECS.items():
  raw=subprocess.check_output(['git','cat-file','blob',spec['blob']],cwd=ROOT.parent)
  base=Image.open(io.BytesIO(raw)).convert('RGB')
  allow=polygon_mask(spec['polygons']).filter(ImageFilter.GaussianBlur(1.5))
  protect=polygon_mask(spec['protected']).filter(ImageFilter.MaxFilter(5))
  if spec.get('vegetation_regions'):
   a=np.asarray(base,dtype=float);r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
   vegetation=((g>r*1.015)&(g>b*1.10))|((b>r*1.04)&(b>g*1.04))|((r>g*1.18)&(b>g*1.1))
   region=np.asarray(polygon_mask(spec['vegetation_regions']))>0
   plants=Image.fromarray((vegetation&region).astype(np.uint8)*255).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.65))
   protect=Image.fromarray(np.maximum(np.asarray(protect),np.asarray(plants)))
  alpha=np.asarray(allow,dtype=float)*(1-np.asarray(protect,dtype=float)/255)
  alpha=Image.fromarray(alpha.astype(np.uint8))
  materialfile=production/(name+'-ground-pond.png')
  original_material=None
  if materials.get(name):
   source=materials[name];original_material={'sha256':sha(source.read_bytes()),'dimensions':list(Image.open(source).size)}
   donor=Image.open(source).convert('RGB').resize(SIZE,Image.Resampling.LANCZOS)
   pixels=np.dstack([np.asarray(donor),np.asarray(alpha)]);pixels[pixels[:,:,3]==0,:3]=0
   layer=Image.fromarray(pixels);layer.save(materialfile)
  else:layer=Image.open(materialfile).convert('RGBA')
  result=Image.alpha_composite(base.convert('RGBA'),layer).convert('RGB');candidate=out/(name+'.png');result.save(candidate)
  changed=np.any(np.asarray(result)!=np.asarray(base),axis=2);support=np.asarray(alpha)>0
  assert not np.any(changed&~support)
  assert not np.any(changed&(np.asarray(protect)==255))
  ys,xs=np.where(changed)
  records.append({'id':name+'-ground-pond','file':spec['file'],'source':{'file':spec['file'],'git_blob':spec['blob'],'sha256':sha(raw)},
   'generated_material':str(materialfile.relative_to(ROOT)),'material_sha256':sha(materialfile.read_bytes()),'raw_generation':original_material,
   'reference':{'file':'game/images/backgrounds/book-one/garden-pond.png','git_blob':'153bbe79a42a1aa4740f068fb012c919c8f65284','sha256':'5fe43f183e54eaa586d4fc085258c770326cc4171234333906840c7fa1f4e958'},
   'prompt_file':spec['prompt'],'prompt_sha256':sha((ROOT/spec['prompt']).read_bytes()),'polygons':spec['polygons'],'protected_polygons':spec['protected'],'vegetation_regions':spec.get('vegetation_regions',[]),'vegetation_mask':'Original green, purple and pink foliage silhouette with 3px gap closing and 0.65px matte antialias; solid plant and pot interiors protected; see script thresholds.',
   'feather_px':1.5,'protected_expansion_px':2,'registered_canvas':list(SIZE),'registration':'Generated 1671x941 material resampled once to original 1672x941; original source never resampled.',
   'candidate':str(candidate.relative_to(ROOT)),'output_sha256':sha(candidate.read_bytes()),
   'verification':{'changed_pixels':int(changed.sum()),'changed_bounds':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'outside_mask_changes':0,'protected_people_and_props_changes':0},
   'script_file':'scripts/repair_pond_geometry.py','script_sha256':sha(Path(__file__).read_bytes())})
 receipt=ROOT/'docs/pond-geometry-materials-planting.json'
 if receipt.exists():
  prior={r['id']:r for r in json.loads(receipt.read_text())['materials']}
  for r in records:
   if r['raw_generation'] is None:r['raw_generation']=prior.get(r['id'],{}).get('raw_generation')
 receipt.write_text(json.dumps({'schema_version':1,'method':'Builtin imagegen material, bounded same-camera composite; preserve all original people and props outside explicitly edited pond-edge regions.','materials':records},indent=2)+'\n')
 print(json.dumps([{r['file']:r['verification'],'output_sha256':r['output_sha256']} for r in records],indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work-material',type=Path);p.add_argument('--compromise-material',type=Path);a=p.parse_args();run({'garden-work-area':a.work_material,'garden-compromise':a.compromise_material})
