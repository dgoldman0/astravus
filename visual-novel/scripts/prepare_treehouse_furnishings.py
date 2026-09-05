"""Isolate later-childhood furniture paint from a referenced material edit.

The fixed room is read from Git. Only movable furniture and its vacated floor
footprint receive new pixels; walls, trunk, openings and rails keep their paint.
The output layer is reusable with each later weather state.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from repair_treehouse_environments import PROJECT, SIZE, EARLY_PAPERS, SOURCES, source_images, compose, rgba, mask


# Boundaries include the old furniture footprint and its contact shadows, not
# merely the new objects: otherwise the old foreground table would remain.
POLYGONS = [
    [[0,562],[126,540],[226,555],[315,573],[376,563],[433,562],[483,600],[524,667],
     [551,732],[627,761],[682,798],[890,941],[0,941]],
    [[612,941],[1672,941],[1672,592],[1580,563],[1465,550],
     [1416,542],[1370,520],[1321,511],[1310,478],[1290,468],
     [1279,445],[1257,445],[1248,471],[1138,466],[1088,475],
     [1035,478],[987,490],[958,513],[944,556],[935,596],
     [888,630],[832,650],[816,680],[760,719],[724,762]],
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('material', type=Path, help='Builtin imagegen furniture material, same 1672x941 framing')
    args = parser.parse_args()
    donor = Image.open(args.material).convert('RGB')
    assert donor.size == SIZE
    sources = source_images()
    early = compose(sources['room'], rgba(sources['papers'], mask(EARLY_PAPERS, .7)))
    alpha = mask(POLYGONS, 2.0)
    layer = rgba(donor, alpha)
    # Discard unused generated architecture from the retained source layer.
    pixels = np.array(layer)
    pixels[pixels[:,:,3] == 0,:3] = 0
    layer = Image.fromarray(pixels)
    destination = PROJECT/'art/production/treehouse-later-furnishings.png'
    destination.parent.mkdir(parents=True, exist_ok=True)
    layer.save(destination)
    later = compose(early, layer)
    out = PROJECT/'build/graphics/environments/states'
    out.mkdir(parents=True, exist_ok=True)
    later.save(out/'later-furnished-base.png')
    delta = np.any(np.array(early) != np.array(later), axis=2)
    support = np.array(alpha) > 0
    assert not np.any(delta & ~support)
    receipt = {
        'schema_version': 1,
        'purpose': 'Later childhood: worktable moved back, two low stools, drawing board, rolled-map holder and rearranged textiles.',
        'material': str(destination.relative_to(PROJECT)),
        'material_sha256': sha(destination),
        'generation_output_sha256': sha(args.material),
        'generation_method': 'builtin imagegen referenced material edit; bounded furniture and old footprint retained',
        'prompt_file': 'docs/graphics-sources/treehouse-furnishings-prompt.txt',
        'sources': list(SOURCES.values()),
        'early_wall_drawings': EARLY_PAPERS,
        'furniture_polygons': POLYGONS,
        'feather_px': 2.0,
        'script_file': 'scripts/prepare_treehouse_furnishings.py',
        'script_sha256': sha(Path(__file__)),
        'base_output_sha256': sha(out/'later-furnished-base.png'),
        'verification': {'changed_pixels': int(delta.sum()), 'outside_furniture_mask_changes': 0,
                         'canvas_size': list(SIZE), 'fixed_architecture_resampled': False},
    }
    (PROJECT/'docs/treehouse-furnishings.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt['verification']))


if __name__ == '__main__':
    main()
