#!/usr/bin/env python3
"""Remove only the extra water pocket behind the rescue coping stones."""
import argparse,hashlib,io,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[1];SIZE=(1672,941)
FILE='game/images/cg/book-one/pond-rescue.png'
BLOB='7d08587c1389a07cfc1c744553fe68ac9ef6908d'
POLYGON=[[1237,449],[1289,449],[1321,451],[1370,451],[1431,454],
 [1508,454],[1567,455],[1608,473],[1614,482],[1596,490],
 [1581,501],[1572,509],[1562,511],[1540,509],[1520,508],
 [1500,506],[1470,506],[1450,504],[1430,506],[1415,508],
 [1400,507],[1380,501],[1360,498],[1340,501],[1320,500],
 [1300,501],[1280,504],[1260,507],[1240,505],[1237,502]]

def sha(raw):return hashlib.sha256(raw).hexdigest()
def run(material=None):
 raw=subprocess.check_output(['git','cat-file','blob',BLOB],cwd=ROOT.parent);base=Image.open(io.BytesIO(raw)).convert('RGB')
 mask=Image.new('L',SIZE);ImageDraw.Draw(mask).polygon([tuple(p) for p in POLYGON],fill=255)
 mask=Image.fromarray(np.minimum(np.asarray(mask),np.asarray(mask.filter(ImageFilter.GaussianBlur(.8)))))
 dest=ROOT/'art/production/pond-rescue-farbank.png';out=ROOT/'build/graphics/pond-geometry';out.mkdir(parents=True,exist_ok=True)
 receiptpath=ROOT/'docs/pond-geometry-materials-rescue.json'
 rawmaterial=None
 if material:
  donor=Image.open(material).convert('RGB');rawmaterial={'sha256':sha(material.read_bytes()),'dimensions':list(donor.size)}
  donor=donor.resize(SIZE,Image.Resampling.LANCZOS);pixels=np.dstack([np.asarray(donor),np.asarray(mask)]);pixels[pixels[:,:,3]==0,:3]=0
  layer=Image.fromarray(pixels);layer.save(dest)
 else:
  layer=Image.open(dest).convert('RGBA')
  if receiptpath.exists():rawmaterial=json.loads(receiptpath.read_text())['raw_generation']
 result=Image.alpha_composite(base.convert('RGBA'),layer).convert('RGB');candidate=out/'pond-rescue.png';result.save(candidate)
 change=np.any(np.asarray(result)!=np.asarray(base),axis=2);support=np.asarray(mask)>0
 assert not np.any(change&~support);assert not np.any(change[:,:1234]);assert not np.any(change[512:])
 ys,xs=np.where(change)
 prompt='docs/graphics-sources/pond-rescue-farbank-prompt.txt'
 receipt={'schema_version':1,'id':'pond-rescue-dry-farbank','file':FILE,'source':{'file':FILE,'git_blob':BLOB,'sha256':sha(raw)},
  'method':'Builtin imagegen soil/paver material retained only through the narrow far-bank water-pocket mask. Original people, animals, foreground water and coping stay original.',
  'generated_material':str(dest.relative_to(ROOT)),'material_sha256':sha(dest.read_bytes()),'raw_generation':rawmaterial,
  'prompt_file':prompt,'prompt_sha256':sha((ROOT/prompt).read_bytes()),'polygon':POLYGON,'feather_px':.8,'feather_direction':'inward; clipped to exact polygon so coping-side pixels are untouched',
  'registration':'Generated 1662x946 material resampled once to original 1672x941; original scene never resampled.',
  'candidate':str(candidate.relative_to(ROOT)),'output_sha256':sha(candidate.read_bytes()),'dimensions':list(SIZE),'mode':'RGB',
  'verification':{'changed_pixels':int(change.sum()),'changed_bounds':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'outside_mask_changes':0,'protected_people_animals_and_main_water_changes':0},
  'script_file':'scripts/repair_pond_farbank.py','script_sha256':sha(Path(__file__).read_bytes())}
 receiptpath.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'sha256':receipt['output_sha256'],**receipt['verification']}))

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--material',type=Path);a=p.parse_args();run(a.material)
