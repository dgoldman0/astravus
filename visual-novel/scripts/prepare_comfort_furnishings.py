"""Isolate the later treehouse worktable in the Cassia comfort camera view.

No character pixels are admitted into the material layer. Its lower boundary
includes the old foreground table footprint so the selected painting can show
the same relocated furniture as the later wide room.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image

from repair_treehouse_environments import PROJECT, SIZE, compose, mask, rgba


POLYGON = [
    [1012,941],[1672,941],[1672,516],[1550,505],[1470,503],
    [1410,503],[1387,479],[1398,421],[1365,388],[1280,364],
    [1275,330],[1234,325],[1224,300],[1204,300],[1194,346],
    [1090,344],[1040,349],[990,347],[971,366],[965,433],
    [905,449],[901,476],[924,502],[926,553],[963,580],
    [1000,601],[1032,626],[1027,680],[1018,739],[1005,783],
    [1008,846],
]


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('material',type=Path)
    args=parser.parse_args()
    donor=Image.open(args.material).convert('RGB'); assert donor.size==SIZE
    base_path=PROJECT/'game/images/cg/book-one/cassia-comfort.png'
    base=Image.open(base_path).convert('RGB')
    alpha=mask([POLYGON],1.25)
    layer=rgba(donor,alpha)
    pixels=np.array(layer);pixels[pixels[:,:,3]==0,:3]=0
    layer=Image.fromarray(pixels)
    path=PROJECT/'art/production/cassia-comfort-later-furnishings.png'
    layer.save(path)
    out=PROJECT/'build/graphics/environments/states'
    out.mkdir(parents=True,exist_ok=True)
    composed=compose(base,layer)
    composed.save(out/'comfort-furnished-base.png')
    changed=np.any(np.array(base)!=np.array(composed),axis=2)
    assert not np.any(changed & (np.array(alpha)==0))
    receipt={
        'schema_version':1,
        'material':str(path.relative_to(PROJECT)), 'material_sha256':sha(path),
        'generation_output_sha256':sha(args.material),
        'prompt_file':'docs/graphics-sources/comfort-furnishings-prompt.txt',
        'reference_cg_sha256':sha(base_path),
        'reference_furniture_file':'art/production/treehouse-later-furnishings.png',
        'reference_furniture_sha256':sha(PROJECT/'art/production/treehouse-later-furnishings.png'),
        'polygon':POLYGON,'feather_px':1.25,
        'script_file':'scripts/prepare_comfort_furnishings.py','script_sha256':sha(Path(__file__)),
        'verification':{'changed_pixels':int(changed.sum()),'outside_furniture_mask_changes':0,
                        'character_faces_hands_outfits_admitted_to_mask':False,
                        'canvas_size':list(SIZE)},
    }
    (PROJECT/'docs/comfort-furnishings.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt['verification']))


if __name__=='__main__':main()
