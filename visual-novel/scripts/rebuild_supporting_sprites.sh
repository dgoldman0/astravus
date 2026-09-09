#!/usr/bin/env bash
# Rebuild editable Lyra/Thalia art outputs. Runtime installation is a separate step.
set -euo pipefail
TASK_SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd -- "$TASK_SCRIPT_DIR/.."
TASK_GIMP_TMP=$(mktemp -d /tmp/astravus-supporting-gimp-XXXXXX)
trap 'rm -rf -- "$TASK_GIMP_TMP"' EXIT
mkdir -p "$TASK_GIMP_TMP/profile/gradients"
GIMP2_DIRECTORY="$TASK_GIMP_TMP/profile" timeout 55s gimp \
  --no-interface --new-instance --no-data --no-fonts --no-splash --no-shm \
  --console-messages --batch-interpreter=plug-in-script-fu-eval \
  --batch "(begin (define audit-dir \"$TASK_GIMP_TMP\") (load \"scripts/refine_supporting_sprites.scm\"))" \
  --batch '(gimp-quit 0)' > "$TASK_GIMP_TMP/gimp.log" 2>&1
cat "$TASK_GIMP_TMP/gimp.log"
python3 scripts/verify_supporting_sprites.py "$TASK_GIMP_TMP"
