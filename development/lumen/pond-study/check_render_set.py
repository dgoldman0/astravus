"""Verify that the review, Blender file and six images form one current set."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct

HERE=Path(__file__).resolve().parent
VIEWS={'pond','wheel','overview','section','rescue','comfort'}
SOURCES={
    'pond':'visual-novel/game/images/backgrounds/book-one/garden-pond.png',
    'wheel':'visual-novel/game/images/backgrounds/book-one/waterwheel.png',
    'rescue':'visual-novel/game/images/cg/book-one/pond-rescue.png',
    'comfort':'visual-novel/game/images/cg/book-one/pond-comfort.png',
}


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_artifacts(here=HERE):
    manifest=json.loads((here/'render-manifest.json').read_text())
    build=manifest['build_id']
    if not re.fullmatch('[0-9a-f]{16}',build):raise ValueError('Invalid build ID')
    folder=here/'builds'/build
    if json.loads((folder/'manifest.json').read_text())!=manifest:raise ValueError('Published and bundle manifests differ')
    js=(here/'render-manifest.js').read_text().strip()
    if not js.startswith('window.POND_RENDER_SET = ') or not js.endswith(';'):raise ValueError('Invalid browser manifest')
    if json.loads(js[len('window.POND_RENDER_SET = '):-1])!=manifest:raise ValueError('Browser uses a different manifest')
    if set(manifest['views'])!=VIEWS:raise ValueError('Incomplete render set')
    dimensions=set()
    for label,entry in [('blend',manifest['blend']),*manifest['views'].items()]:
        path=here/entry['path']
        if not path.resolve().is_relative_to(folder.resolve()):raise ValueError(label+' points outside its build')
        if sha(path)!=entry['sha256']:raise ValueError(label+' file hash differs from its published build')
        if label=='blend':continue
        if entry['snapshot_sha256']!=manifest['blend']['sha256']:raise ValueError(label+' uses another Blender snapshot')
        if entry['common_geometry_sha256']!=manifest['common_geometry_sha256']:raise ValueError(label+' uses different shared geometry')
        header=path.read_bytes()[:24]
        if header[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError(label+' is not a PNG')
        dimensions.add(struct.unpack('>II',header[16:24]))
    if len(dimensions)!=1:raise ValueError('Render dimensions differ across views')
    if (here/'pond-study.blend').resolve()!=(here/manifest['blend']['path']).resolve():raise ValueError('Native-file shortcut is stale')
    if (here/'renders').resolve()!=(folder/'renders').resolve():raise ValueError('Render-directory shortcut is stale')
    return manifest


def verify_inputs(manifest,here=HERE):
    for name,digest in manifest['inputs'].items():
        if sha(here/name)!=digest:raise ValueError(name+' changed since the published build; rebuild all views')
    report=json.loads((here/'builds'/manifest['build_id']/'study.json').read_text())
    root=here.parents[2]
    for key,digest in report['source_sha256'].items():
        if sha(root/SOURCES[key])!=digest:raise ValueError(key+' VN reference changed; review and rebuild')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--artifacts-only',action='store_true',help='Check the published set while a new source revision is in progress')
    args=parser.parse_args()
    try:
        manifest=verify_artifacts()
        if not args.artifacts_only:verify_inputs(manifest)
    except (ValueError,KeyError,FileNotFoundError) as error:raise SystemExit(str(error))
    print('Verified six views from one Blender snapshot: '+manifest['build_id'])
    print('This checks artifact consistency, not visual acceptance or physical simulation.')


if __name__=='__main__':main()
