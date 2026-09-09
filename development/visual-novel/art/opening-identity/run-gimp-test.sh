#!/usr/bin/env bash
# Rebuild and verify the isolated opening-scene editing test.
set -euo pipefail
TASK_TEST_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd -- "$TASK_TEST_DIR/../../../../visual-novel"
TASK_GIMP_TMP=$(mktemp -d /tmp/astravus-opening-gimp-XXXXXX)
trap 'rm -rf -- "$TASK_GIMP_TMP"' EXIT
mkdir -p "$TASK_GIMP_TMP/profile/gradients"

python3 - <<'PY'
import hashlib
from pathlib import Path
from PIL import Image
paths = {
    '../development/visual-novel/art/opening-identity/opening-original.png': '796c68db5e23c791ffb486c3f998b0c3b44c32915efff9f090fdec075176ea4f',
    '../development/visual-novel/art/opening-identity/opening-generated-v1.png': '17423b95da463da9185dc732903e2b8ee96a314d15e2a04922c7dbad1c415512',
}
for filename, expected in paths.items():
    assert hashlib.sha256(Path(filename).read_bytes()).hexdigest() == expected, filename
    with Image.open(filename) as image:
        assert image.size == (1672, 941) and image.mode == 'RGB', filename
PY

GIMP2_DIRECTORY="$TASK_GIMP_TMP/profile" timeout 55s gimp \
  --no-interface --new-instance --no-data --no-fonts \
  --no-splash --no-shm --console-messages \
  --batch-interpreter=plug-in-script-fu-eval \
  --batch "(begin (define audit-dir \"$TASK_GIMP_TMP\") (load \"../development/visual-novel/art/opening-identity/assemble.scm\"))" \
  --batch '(gimp-quit 0)' > "$TASK_GIMP_TMP/gimp.log" 2>&1
cat "$TASK_GIMP_TMP/gimp.log"

python3 - "$TASK_GIMP_TMP" <<'PY'
# Analysis only: native GIMP creates every image, mask, and XCF.
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
from PIL import Image

folder = Path('../development/visual-novel/art/opening-identity')
audit = Path(sys.argv[1])
def pixels(path):
    with Image.open(path) as image:
        return np.asarray(image).copy()
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def bbox(support):
    ys, xs = np.where(support)
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]

source_path = Path('../development/visual-novel/art/opening-identity/opening-original.png')
source = pixels(source_path)
candidate = pixels(folder / 'opening-generated-v1.png')
final = pixels(folder / 'opening-refined-v1.png')
reopened = pixels(audit / 'reopened-output.png')
restored = pixels(audit / 'restored-base.png')
assert source.shape == final.shape == candidate.shape == (941, 1672, 3)
union = np.zeros(source.shape[:2], dtype=bool)
masks = []
for name in ['mask-arin-head.png', 'mask-arin-arms.png', 'mask-sage.png']:
    values = pixels(folder / name)
    assert values.shape == source.shape[:2], (name, values.shape)
    support = values > 0
    union |= support
    masks.append({'file': name, 'sha256': sha(folder / name),
                  'nonzero_pixels': int(support.sum()), 'support_bbox': bbox(support),
                  'feather_pixels': int(((values > 0) & (values < 255)).sum())})

changed = np.any(final != source, axis=2)
outside = int((changed & ~union).sum())
assert outside == 0, f'{outside} pixels changed outside the native masks'
assert np.array_equal(final, reopened), 'XCF reopened export does not match the final PNG'
assert np.array_equal(source, restored), 'Hiding all three refinement layers did not restore original pixels'

# Conservative bounding boxes inside the central subjects, excluding Arin/Sage.
protected = {
    'Selene face': [611, 125, 674, 257],
    'Dorian face': [1014, 111, 1156, 302],
    'Maia face': [818, 232, 926, 398],
    'Calista newborn face and reaching hand': [938, 435, 1125, 536],
    'Maia hands around the blanket': [801, 586, 1080, 731],
}
checks = []
for name, (x0, y0, x1, y1) in protected.items():
    number = int(changed[y0:y1, x0:x1].sum())
    assert number == 0, (name, number)
    checks.append({'region': name, 'box': [x0, y0, x1, y1], 'changed_pixels': number})

report = {
    'status': 'passed', 'tool': 'GIMP 2.10.36 Script-Fu',
    'generation_model': 'Built-in image tool; backend version not exposed',
    'source_file': str(source_path), 'source_sha256': sha(source_path),
    'candidate_file': 'opening-generated-v1.png',
    'candidate_sha256': sha(folder / 'opening-generated-v1.png'),
    'final_file': 'opening-refined-v1.png', 'final_sha256': sha(folder / 'opening-refined-v1.png'),
    'xcf_file': 'opening-refined-v1.xcf', 'xcf_sha256': sha(folder / 'opening-refined-v1.xcf'),
    'dimensions': [1672, 941], 'mode': 'RGB',
    'methods': ['Unscaled locked original base', 'Three generated-paint layers in legacy Normal mode',
                'Native GIMP hand-traced polygon selections with 4px feather',
                'Editable layer masks, with actual masks exported for analysis'],
    'masks': masks, 'changed_pixels': int(changed.sum()),
    'raw_generation_changed_pixels': int(np.any(candidate != source, axis=2).sum()),
    'outside_mask_changed_pixels': outside,
    'outside_mask_pixels_identical': True, 'xcf_reopened_matches_final': True,
    'hidden_refinement_layers_restore_original': True, 'protected_regions': checks,
    'assembly_file': 'assemble.scm', 'assembly_sha256': sha(folder / 'assemble.scm'),
    'rebuild_file': 'run-gimp-test.sh', 'rebuild_sha256': sha(folder / 'run-gimp-test.sh'),
    'limitation': 'Numeric checks establish preservation and editability, not artistic or canonical approval.',
}
(folder / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({key: report[key] for key in ['status', 'changed_pixels', 'raw_generation_changed_pixels',
    'outside_mask_changed_pixels', 'xcf_reopened_matches_final', 'hidden_refinement_layers_restore_original']}, indent=2))
PY
