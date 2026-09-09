"""Capture every selected theme composition through the actual Ren'Py screen.

A temporary visual-review testcase is removed after the run; it is never shipped.
Audio is paused after opening the theme so each recorded cue position is stable.
"""
import hashlib
import json
from pathlib import Path

import project

ROOT = Path(__file__).resolve().parents[1]
temporary = ROOT / 'game/_graphics_theme_inventory.rpy'
assert not temporary.exists(), 'Refusing to overwrite an existing test file'
cues = json.loads((ROOT / 'game/closing_theme.json').read_text())
lines = ['testcase theme_art_inventory:', '    assert screen "main_menu"',
         '    $ persistent.chapter_spoiler_warnings = False', '    $ persistent.reduced_motion = False',
         '    click "Chapters"', '    click "32 · What remains"',
         '    advance until screen "book_afterword"', '    click "Play closing theme"',
         '    assert screen "closing_theme"', '    pause .5', '    click "Pause"']
shots = []
for index, shot in enumerate(cues['shots']):
    end = cues['shots'][index + 1]['at'] if index + 1 < len(cues['shots']) else cues['duration'] - cues['fade_out']
    moment = (shot['at'] + cues['dissolve'] + end) / 2
    capture = f'theme-art-{index:02d}'
    lines.extend([f'    $ renpy.get_widget("closing_theme", "montage").last_position = {moment!r}',
                  '    pause .25', f'    screenshot "{capture}"'])
    path = ROOT / 'game' / shot['image']
    shots.append({'capture': capture, 'position': moment, 'image': 'game/'+shot['image'],
                  'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'label': shot['label']})
lines.extend(['    click "Skip closing theme"', '    assert screen "chapter_end"'])
out = ROOT / '../development/visual-novel/archive/local/graphics-workspace'
out.mkdir(parents=True, exist_ok=True)
(out / 'theme-art-testcase.txt').write_text('\n'.join(lines)+'\n')
try:
    temporary.write_text('\n'.join(lines)+'\n')
    project.engine(ROOT, 'test', 'theme_art_inventory', '--overwrite-screenshots', '--hide-execution', 'hooks', headless=True, testing=True)
    (out / 'theme-art-inputs.json').write_text(json.dumps({'shots': shots, 'cue_sha256': hashlib.sha256((ROOT / 'game/closing_theme.json').read_bytes()).hexdigest()}, indent=2)+'\n')
finally:
    temporary.unlink(missing_ok=True)
    temporary.with_suffix('.rpyc').unlink(missing_ok=True)
