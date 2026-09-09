# Sage iris refinement — September 9, 2026

The selected childhood sprite's visible iris rings read warm brown. [Sage's biography](../../../../../../wiki/bios/Sage.md), line 11, specifies gray eyes ranging from pale silver to deep storm; the [curated key](../../../../../../visual-novel/art/character-keys/sage/key.png) includes a gray iris detail. This small correction retains the deep shade appropriate to the existing warm light.

[Before](sprite-before.png) and [selected result](sprite-refined.png) differ only in 77 pixels of iris pigment. GIMP's luminance desaturation blends at 80% opacity through two narrowly drawn, 0.25-pixel-feathered masks. The 68 explicitly protected pupil/catchlight pixels are unchanged. The remaining face, sclera, lids, freckles, hair, costume, crossed hands, feet and green backing remain pixel-exact. The subtle remaining warmth is deliberate; the eyes should not become blue or luminous.

The [editable XCF](sprite-refined.xcf) retains the previous head/torso assembly and adds one named masked correction layer. Reopening reproduces the PNG exactly. Hiding that new layer restores the prior selected sprite exactly. [Verification](verification.json) records masks, hashes, pixel counts, luminance rounding and native evidence; [verify.py](verify.py) repeats those checks without modifying art.

The [GIMP before detail](eye-detail-before.png) and [after detail](eye-detail-after.png) are nearest-neighbor enlargements of source rectangle `(442,118,120,80)`. They make the small lower iris crescents legible. Both the full source result and the [actual Ren'Py before](native-sage-before.png)/[after](native-sage-after.png) standing renders were visually inspected. The native change is slight at normal character size, with no face, pose, silhouette or matte shift. The existing `character_framing_review` suite passed before and after; these are standing-render checks, not new dialogue-playthrough evidence.

Reproduce the editable result from `visual-novel/` with GIMP 2.10.36:

```sh
gimp --no-interface --new-instance --no-data --no-fonts --no-splash --no-shm \
  --console-messages --batch-interpreter=plug-in-script-fu-eval \
  --batch '(load "scripts/refine_sage_irises.scm")' --batch '(gimp-quit 0)'
```

[refine_sage_irises.scm](../../../../../../visual-novel/scripts/refine_sage_irises.scm) uses this folder's immutable `sprite-before.png` and the preceding `../sprite-refined.xcf`. It exports the actual masks, editable result, reopened/restored proof images and enlarged details. It does not install the runtime PNG. The reviewed result was subsequently installed at `visual-novel/game/images/characters/book-one/sage-everyday.png`; integration records are maintained separately.
