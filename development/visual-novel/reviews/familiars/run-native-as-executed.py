import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

SOURCE = Path('/home/kir/Documents/Projects/astravus-visual-novel/Astravus/visual-novel')
BASE = Path('/tmp/astravus-familiar-runtime')
PROJECT = BASE / 'project'
VARIANT = sys.argv[1]
assert VARIANT in ('before', 'after', 'candidate')
OUT = BASE / VARIANT
OUT.mkdir(parents=True, exist_ok=True)

if not PROJECT.exists():
    (PROJECT / 'game').mkdir(parents=True)
    for item in (SOURCE / 'game').iterdir():
        if item.name in ('cache', 'saves') or item.suffix == '.rpyc':
            continue
        target = PROJECT / 'game' / item.name
        if item.is_file():
            shutil.copyfile(item, target)
        else:
            target.symlink_to(item, target_is_directory=True)
    (PROJECT / 'docs').symlink_to(SOURCE / 'docs', target_is_directory=True)

shutil.copyfile(SOURCE / 'game/familiars.rpy', PROJECT / 'game/familiars.rpy')
(PROJECT / 'game/familiars.rpyc').unlink(missing_ok=True)
test = '''testcase familiar_compositing_review:
    assert screen "main_menu"
    $ persistent.chapter_spoiler_warnings = False
    $ _test.force = True
    $ _test.screenshot_directory = "OUTPUT_DIRECTORY"
    click "Chapters"
    click "09 · The Tree of Echoes"
    advance until eval (renpy.showing("calista home") and renpy.showing("barkley"))
    pause .25
    screenshot "echoes-dialogue"
    keysym "h"
    pause .25
    screenshot "echoes-clean"
    keysym "h"
    click "Chapters"
    click "21 · The unfinished world"
    advance until eval (renpy.showing("nibble") and renpy.showing("bg construction_path"))
    pause .25
    screenshot "construction-path-dialogue"
    keysym "h"
    pause .25
    screenshot "construction-path-clean"
    keysym "h"
    advance until eval (renpy.showing("bg construction_room"))
    pause .25
    screenshot "construction-room-dialogue"
    keysym "h"
    pause .25
    screenshot "construction-room-clean"
    keysym "h"
    click "Chapters"
    click "01 · First memory"
    advance until eval (renpy.showing("nibble") and renpy.showing("bg family_home"))
    pause .25
    screenshot "home-dialogue"
    keysym "h"
    pause .25
    screenshot "home-clean"
    exit
'''.replace('OUTPUT_DIRECTORY', OUT.as_posix())
(PROJECT / 'game/_familiar_review.rpy').write_text(test)
(PROJECT / 'game/_familiar_review.rpyc').unlink(missing_ok=True)
env = dict(os.environ, SDL_AUDIODRIVER='dummy', RENPY_PATH_TO_SAVES=str(BASE / 'saves'))
command = ['xvfb-run', '-a', '-s', '-screen 0 1920x1080x24',
           str(SOURCE / '.cache/renpy-8.5.3-sdk/renpy.sh'), str(PROJECT), 'test',
           'familiar_compositing_review', '--overwrite-screenshots', '--hide-execution', 'hooks']
with (OUT / 'native.log').open('w') as log:
    subprocess.run(command, cwd=PROJECT, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
inputs = {'familiars_rpy_sha256': hashlib.sha256((PROJECT/'game/familiars.rpy').read_bytes()).hexdigest(),
          'source_images': {str(path.relative_to(SOURCE)): hashlib.sha256(path.read_bytes()).hexdigest()
                            for path in (SOURCE/'game/images/familiars').glob('*.png')},
          'screenshots': {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(OUT.glob('*.png'))}}
(OUT/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
print(json.dumps({'variant': VARIANT, 'shots': len(inputs['screenshots']), 'directory': str(OUT)}))
