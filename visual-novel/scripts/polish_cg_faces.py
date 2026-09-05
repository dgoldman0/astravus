"""Prepare registered face patches and assemble editable production CGs in GIMP.

Every run starts from immutable Git pixels. Face material can change expression
construction only inside its hand-traced skin mask; eye warps never resample the
whole painting. The XCF retains a locked original and named, bounded edit layers.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from polish_character_geometry import edit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/graphics-polish/cg'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def quote(value):
    return json.dumps(str(value))


def run(item):
    name = Path(item['file']).stem
    folder = OUT / name
    folder.mkdir(parents=True, exist_ok=True)
    raw = subprocess.check_output(['git', 'cat-file', 'blob', item['source_git_blob']], cwd=ROOT)
    assert hashlib.sha256(raw).hexdigest() == item['source_sha256']
    source = Image.open(io.BytesIO(raw)).convert('RGB')
    base = folder / 'base.png'
    base.write_bytes(raw)
    layers = []
    support = np.zeros((source.height, source.width), dtype=bool)
    if item.get('eye_geometry'):
        changed, proof = edit(source, item)
        delta = np.any(np.array(changed) != np.array(source), axis=2)
        support |= delta
        bounds = tuple(proof['change_bbox'])
        patch = folder / 'eye-geometry.png'
        changed.crop(bounds).save(patch)
        layers.append(('Eye aperture and surrounding skin', patch, bounds[:2]))
    material = item.get('face_material')
    if material:
        donor_path = ROOT / material['file']
        donor = Image.open(donor_path).convert('RGB').resize(tuple(material['resize']), Image.Resampling.LANCZOS)
        donor, _ = edit(donor, material)
        mask = Image.new('L', donor.size)
        ImageDraw.Draw(mask).polygon([tuple(p) for p in material['polygon']], fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(material['feather']))
        affine = cv2.getAffineTransform(np.float32(material['source_landmarks']), np.float32(material['target_landmarks']))
        pixels = cv2.warpAffine(np.array(donor), affine, source.size, flags=cv2.INTER_LANCZOS4)
        alpha = cv2.warpAffine(np.array(mask), affine, source.size, flags=cv2.INTER_LINEAR)
        support |= alpha > 0
        rgba = Image.fromarray(np.dstack([pixels, alpha]))
        bounds = rgba.getbbox()
        patch = folder / 'face-material.png'
        rgba.crop(bounds).save(patch)
        layers.append((material.get('character', 'Cassia') + ' facial painting - registered skin only', patch, bounds[:2]))
    scenery = item.get('scene_overlay')
    if scenery:
        layer_path = ROOT / scenery['file']
        assert sha(layer_path) == scenery['sha256'], 'Scene overlay changed after selection'
        rgba = Image.open(layer_path).convert('RGBA')
        assert rgba.size == source.size
        alpha = np.array(rgba.getchannel('A'))
        assert not np.any((alpha > 0) & support), 'Window layer overlaps a facial edit'
        support |= alpha > 0
        bounds = rgba.getbbox()
        patch = folder / 'window-landmarks.png'
        rgba.crop(bounds).save(patch)
        layers.append(('Shared painted exterior branches - windows only', patch, bounds[:2]))
    xcf = folder / (name + '.xcf')
    output = OUT / (name + '.png')
    forms = [f'(let* ((im (car (gimp-file-load RUN-NONINTERACTIVE {quote(base)} {quote(base)}))) (layer 0) (copy 0))',
             '(gimp-image-undo-disable im)', '(gimp-item-set-name (car (gimp-image-get-active-layer im)) "Original painting - locked")',
             '(gimp-item-set-lock-content (car (gimp-image-get-active-layer im)) TRUE)']
    for title, path, (x, y) in layers:
        forms.extend([f'(set! layer (car (gimp-file-load-layer RUN-NONINTERACTIVE im {quote(path)})))',
                      '(gimp-image-insert-layer im layer 0 0)', f'(gimp-item-set-name layer {quote(title)})',
                      f'(gimp-layer-set-offsets layer {x} {y})'])
    forms.extend(['(gimp-image-undo-enable im)',
                  f'(gimp-file-save RUN-NONINTERACTIVE im layer {quote(xcf)} {quote(xcf)})',
                  '(set! copy (car (gimp-image-duplicate im)))',
                  f'(file-png-save2 RUN-NONINTERACTIVE copy (car (gimp-image-flatten copy)) {quote(output)} {quote(output)} 0 9 0 0 0 0 0 0 0)',
                  '(gimp-image-delete copy)', '(gimp-image-delete im))'])
    batch = folder / 'assemble.scm'
    batch.write_text('\n'.join(forms) + '\n')
    profile = folder / 'gimp-profile'
    (profile / 'gradients').mkdir(parents=True, exist_ok=True)
    env = {**os.environ, 'GIMP2_DIRECTORY': str(profile)}
    result = subprocess.run(['gimp', '-n', '-i', '-d', '-f', '-s', '-c', '--batch-interpreter=plug-in-script-fu-eval',
                             '-b', f'(load {quote(batch)})', '-b', '(gimp-quit 0)'], env=env, capture_output=True, text=True, timeout=120)
    (folder / 'gimp.log').write_text(result.stdout + result.stderr)
    assert result.returncode == 0 and output.exists(), result.stderr
    final = Image.open(output).convert('RGB')
    # GIMP includes volatile creation metadata; normalize the delivery PNG so
    # repeated assembly produces identical files as well as identical pixels.
    final.save(output)
    delta = np.any(np.array(final) != np.array(source), axis=2)
    assert not np.any(delta & ~support), 'Pixels outside the declared edit support changed'
    ys, xs = np.where(delta)
    Image.fromarray(support.astype('uint8') * 255).save(folder / 'edit-support.png')
    sources = [{'file': item['file'], 'git_blob': item['source_git_blob'], 'sha256': item['source_sha256']}]
    if material:
        sources.append({'file': material['file'], 'sha256': sha(ROOT / material['file'])})
    if scenery:
        sources.append({'file': scenery['file'], 'sha256': scenery['sha256']})
    recipe = {**item, 'sources': sources, 'operations': ['bounded eye-aperture inverse warp', 'GIMP editable-layer composition'],
              'mask_geometry': {'eye_geometry': item.get('eye_geometry'), 'face_material': material, 'scene_overlay': scenery},
              'dimensions': list(final.size), 'mode': final.mode, 'script_file': 'scripts/polish_cg_faces.py',
              'script_sha256': sha(Path(__file__)), 'dependencies': [{'file': 'scripts/polish_character_geometry.py', 'sha256': sha(ROOT / 'scripts/polish_character_geometry.py')}],
              'output_sha256': sha(output), 'verification': {'changed_pixels': int(delta.sum()), 'outside_mask_pixels_changed': 0,
              'outside_mask_identical': True, 'canvas_and_mode_unchanged': source.size == final.size and source.mode == final.mode,
              'change_bbox': [int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1]},
              'editable_xcf': str(xcf.relative_to(ROOT)), 'xcf_sha256': sha(xcf)}
    (folder / 'recipe.json').write_text(json.dumps(recipe, indent=2)+'\n')
    print(name, recipe['output_sha256'], flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('names', nargs='*')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for item in json.loads((ROOT / 'docs/cg-geometry-spec.json').read_text())['assets']:
        if not args.names or Path(item['file']).stem in args.names:
            run(item)
