# First Breath: character refinement test

September 8, 2026. This records the opening-scene trial approved before the broader visual pass. The accepted composite is now selected for the game; the original input is frozen as `opening-original.png` so this comparison remains reproducible. See [the broader pass](../visual-pass-2026-09/README.md) for subsequent character keys and propagation.

Open [the comparison viewer](review.html) for the original, refined composite, unmasked generation, paired face details and actual Ren'Py captures. The viewer works as a local file and uses only local assets.

## The design change

The primary correction is Sage's face and build. The [biography](../../../wiki/bios/Sage.md) specifies round, soft features and a medium build; the existing opening and everyday sprite had a narrow, angular face and lean neck, close to Arin's design. The candidate gives Sage fuller cheeks, a rounder chin, a calmer sandy crop and modest upper-body fullness while preserving the inward gaze and adult androgynous appearance.

Arin retains their defined profile and lean build. Their cropped auburn hair and paler freckled complexion now separate them more clearly from Sage under the same warm light. The manuscript fixes the crop and lean muscular build (`revision/latest.md:29`), and [Arin's biography](../../../wiki/bios/Arin.md) supplies the pale complexion.

The source-based directions for all five parents, the siblings and the friends' parents are in [CHARACTER_REFINEMENTS.md](CHARACTER_REFINEMENTS.md). Exact facial contours and hairstyle arrangements remain proposed production interpretations. This test does not establish full multi-view keys.

## Generation and editing

- **Input:** [opening-original.png](opening-original.png), copied from `game/images/cg/first-memory-young.png` at commit `41c410e`, 1672 × 941, SHA-256 `796c68db5e23c791ffb486c3f998b0c3b44c32915efff9f090fdec075176ea4f`.
- **Generated material:** [opening-generated-v1.png](opening-generated-v1.png), 1672 × 941, SHA-256 `17423b95da463da9185dc732903e2b8ee96a314d15e2a04922c7dbad1c415512`.
- **Prompt:** [prompt-v1.txt](prompt-v1.txt), provided with the original opening as the sole edit target.
- **Generation method:** one built-in `image_gen` edit, approximately 93 seconds. The tool did not expose a model selector or return an underlying model identity. This is therefore a test of the available image editor, not independent confirmation that GPT Image 2.5 or either API variant was used. No fallback API/CLI generation was used.
- **Finishing method:** native GIMP 2.10.36 layer masks over a locked original. The [editable XCF](opening-refined-v1.xcf) retains separate repair layers. The selected composite is [opening-refined-v1.png](opening-refined-v1.png).

The generated composition stayed at the exact source dimensions and remained closely aligned. It nevertheless changed 1,572,137 of 1,573,352 decoded pixels across the image. Mean absolute RGB difference was 7.174 on a 0–255 channel scale. Similarity of composition was not enough to satisfy preservation of unrelated details.

GIMP is used to retain the useful Arin and Sage changes while recovering the original elsewhere. Hair silhouettes need small areas of surrounding paint to remove the old contour; these areas are part of the explicit masks. Pixel preservation is assessed outside the actual feathered masks, not merely outside a loose rectangle around the characters.

## Observed result

The final composite changes 250,921 pixels (15.95% of the source). All decoded RGB pixels outside the three native masks match the original exactly. Protected regions covering the central parents' faces, the newborn's face and reaching hand, and Maia's holding hands also have zero changes. Reopening and flattening the saved XCF reproduces the final PNG; hiding its three refinement layers restores the original pixels.

At full composition size, Arin's paler skin and cropped auburn sides remain coherent with the warm lighting. Sage's fuller cheeks, rounded chin and softer neck make them more distinct. Separate visual inspections found no conspicuous seams around hair silhouettes, collars or the arm/sleeve junctions. Sage's original bare forearms, hands and lap are retained. The warm shared gaze and central holding gesture remain intact.

The actual Ren'Py captures show both faces clearly above the same dialogue panel at 1920 × 1080. Both captures passed the six targeted opening-scene assertions; the after capture uses the exact candidate hash recorded in the verification. The original artwork and game source hashes stayed unchanged.

This is a promising local correction. The downward gazes cannot establish the blue-versus-gray iris distinction, and full standing proportions and other angles remain untested. Sage and Arin still share freckles, short wavy hair and a tender inward pose, but their facial construction carries more of their individual identity.

## Review and reproduction

[verification.json](verification.json) records the image hashes, actual mask support, unchanged-pixel checks and XCF round-trip results. Run `bash run-gimp-test.sh` from this directory to reproduce the composite with the installed GIMP. The masks are authored in [assemble.scm](assemble.scm); they remain independently editable in the XCF.

[runtime-before.png](runtime-before.png) and [runtime-after.png](runtime-after.png) use the real opening scene and say screen at `opening_003`: “They told me about the Sanctuary. About my First Breath, and the five pairs of hands waiting to hold me.” They are made with [capture-runtime.py](capture-runtime.py) in an isolated temporary source copy, with separate temporary saves and the original or candidate image linked into that copy. [Runtime capture notes](runtime-capture-notes.json) record the actual engine, image hashes and source-preservation checks.

To repeat the native capture with the local Ren'Py SDK and an available X display:

```sh
python3 capture-runtime.py --variant both
```

## Practical limit

The trial tests a local identity correction in one shared pose and lighting condition. It does not establish identity consistency across profiles, expressions, standing sprites or later ages. At the time of this trial, the Arin and Sage sprites still represented their earlier designs. The subsequent broader pass supplies full keys and coordinated sprite updates; this directory retains the narrower trial evidence.
