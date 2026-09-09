#!/usr/bin/env bash
set -euo pipefail
PARENT_KEYS_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd -- "$PARENT_KEYS_DIR/../.."
PARENT_GIMP_TMP=$(mktemp -d /tmp/astravus-parent-sprite-gimp-XXXXXX)
trap 'rm -rf -- "$PARENT_GIMP_TMP"' EXIT
mkdir -p "$PARENT_GIMP_TMP/profile/gradients"
GIMP2_DIRECTORY="$PARENT_GIMP_TMP/profile" timeout 55s gimp \
  --no-interface --new-instance --no-data --no-fonts --no-splash --no-shm --console-messages \
  --batch-interpreter=plug-in-script-fu-eval \
  --batch "(begin (define audit-dir \"$PARENT_GIMP_TMP\") (load \"scripts/assemble_parent_sprite_keys.scm\"))" \
  --batch '(gimp-quit 0)' > "$PARENT_GIMP_TMP/gimp.log" 2>&1
cat "$PARENT_GIMP_TMP/gimp.log"
python3 - "$PARENT_GIMP_TMP" <<'PY'
# Analysis only. Every image and mask is produced by native GIMP above.
import hashlib, json, sys
from pathlib import Path
import numpy as np
from PIL import Image
root=Path('art/character-keys')
audit=Path(sys.argv[1])
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def pixels(path):
    with Image.open(path) as im: return np.array(im)
results=[]
for name,masks in [('arin',['mask-head.png','mask-arms.png']),('sage',['mask-head.png','mask-torso.png'])]:
    folder=root/name
    before=pixels(folder/'sprite-before.png')
    final=pixels(folder/'sprite-refined.png')
    assert before.shape==final.shape
    union=np.zeros(before.shape[:2],dtype=bool)
    mask_records=[]
    for filename in masks:
        values=pixels(folder/filename)
        support=values>0
        union|=support
        yy,xx=np.where(support)
        mask_records.append({'file':str(folder/filename),'sha256':sha(folder/filename),
                             'support_bbox':[int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1],
                             'nonzero_pixels':int(support.sum())})
    changed=np.any(before!=final,axis=2)
    assert not np.any(changed & ~union),name+' changed outside masks'
    assert np.array_equal(final,pixels(audit/(name+'-reopened.png')))
    assert np.array_equal(before,pixels(audit/(name+'-restored.png')))
    assert not changed[-600:].any(),name+' lower body changed'
    record={'name':name,'tool':'GIMP 2.10.36 Script-Fu','size':[final.shape[1],final.shape[0]],
            'source_file':str(folder/'sprite-before.png'),'source_sha256':sha(folder/'sprite-before.png'),
            'generated_file':str(folder/'sprite-generated.png'),'generated_sha256':sha(folder/'sprite-generated.png'),
            'final_file':str(folder/'sprite-refined.png'),'final_sha256':sha(folder/'sprite-refined.png'),
            'xcf_file':str(folder/'sprite-refined.xcf'),'xcf_sha256':sha(folder/'sprite-refined.xcf'),
            'masks':mask_records,'changed_pixels':int(changed.sum()),
            'outside_mask_changed_pixels':0,'xcf_reopened_matches_final':True,
            'hidden_edit_layers_restore_original':True,'bottom_600_rows_unchanged':True,
            'script_file':'scripts/assemble_parent_sprite_keys.scm',
            'script_sha256':sha(Path('scripts/assemble_parent_sprite_keys.scm')),
            'method':'Generated paint on immutable base; native GIMP polygon layer masks with 2px feather, Normal legacy blend'}
    results.append(record)
(root/'parents-sprite-verification.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['name','changed_pixels','outside_mask_changed_pixels','bottom_600_rows_unchanged']} for r in results],indent=2))
PY
