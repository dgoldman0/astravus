# Book I validation — 0.1-alpha

The September 9, 2026 visual pass has been rebuilt into the PC, macOS and browser **review builds**, plus the standalone closing film. These packages include the corrected Lyron wardrobe and the final Sage/familiar touchups. Full release approval remains separate from this graphics and rebuild checkpoint.

The current art review covers all **78 selected images**: 29 backgrounds, 20 scene illustrations, 26 human sprites and three familiars. The [character gallery](../art/character-keys/index.html) contains 20 selected sheets for all 17 named depicted characters, with separate early/later keys for the three childhood friends. Current findings are in the [character and scene review](../../development/visual-novel/reviews/characters-and-scenes.md), [background review](../../development/visual-novel/reviews/backgrounds.md) and [familiar compositing review](../../development/visual-novel/reviews/familiar-compositing.md).

## Checks completed for this checkpoint

| Check | Result |
| --- | --- |
| Asset provenance and continuity | 78 selected files, 172 generation records and 30 active production edits pass; 20 CG reviews and 30 location views across seven locations are current. |
| Native full-book integration | 156/156 assertions pass through the existing `chapter_playthrough` suite. |
| Native standing-character framing | All 26 silhouettes pass; feet remain within 2 virtual pixels of the shared baseline and wardrobe heights within 3 pixels. Sage has fresh before/after native renders. |
| Regression tests | 63 tests pass, including review invalidation and the relocated development-evidence path checks. |
| Ren'Py lint | Passes on the pinned 8.5.3.26051504 SDK: 659 dialogue blocks and 7,873 words. |
| PC, Mac and browser archives | ZIP integrity and byte-for-byte equality pass for all 144 packaged runtime/README files; expected launchers, permissions, version and generated engine files pass. |
| Browser integration | Full automated playthrough remains incomplete: at scene 31, rain is queued but the preceding garden ambience continues beyond the 10-second check. The separate closing-theme interaction check passes. See the [rain diagnosis](../../development/visual-novel/reviews/organization/browser-rain.md) and [closing-theme check](../../development/visual-novel/reviews/organization/browser-closing-pointer.md). |
| Relocated GIMP workflows | The opening, parent and supporting-character runners reproduce all five retained results pixel for pixel in an isolated directory with the new structure. |
| Sage iris correction | 77 source pixels change; zero change outside the iris masks or in protected pupils/catchlights. XCF reopening and layer-hidden restoration are exact. |

The [checkpoint evidence directory](../../development/visual-novel/reviews/organization/) retains logs, preservation and gallery checks. [Sage's edit record](../../development/visual-novel/art/characters/sage/iris-refinement/README.md) and the familiar review distinguish source inspection from actual native rendering. The [graphics production guide](GRAPHICS_POLISH.md) links the separate, hash-bound dimension ledger.

## Rebuilt artifacts

| Artifact | Purpose |
| --- | --- |
| [PC ZIP](../dist/astravus-book-one-0.1-alpha-pc.zip) | Windows and Linux package, including both launchers. |
| [macOS ZIP](../dist/astravus-book-one-0.1-alpha-mac.zip) | Unsigned macOS application bundle. |
| [Browser ZIP](../build/web.zip) | HTTP-served HTML game; `index.html` is at the archive root. |
| [Closing film](../build/closing-theme.mp4) | Separate 1920×1080, 60 fps video using the current selected montage art and complete original song. |

Exact archive identities and the completed and incomplete checks are retained in [the rebuild receipt](../../development/visual-novel/reviews/organization/rebuild.json). The [export check](../../development/visual-novel/reviews/organization/export-check.log) has local machine-readable copies at `test-results/review-exports.json` and `build/release-builds.json`. The [film render receipt](../../development/visual-novel/reviews/film/render-result.json) records all 22 frozen inputs, complete stream decoding and the expected 10,666 frames. The original WAV and game OGG are unchanged. No files were published or uploaded.

## Reproduce

From `visual-novel/`, with the pinned SDK installed:

```sh
python3 scripts/check_assets.py
python3 scripts/graphics_review.py status --strict
python3 -m unittest discover -s tests
python3 scripts/project.py lint
python3 scripts/project.py test --headless --suite chapter_playthrough
python3 scripts/project.py test --headless --suite character_framing_review
python3 scripts/project.py build --review-build
python3 scripts/project.py web --review-build
python3 scripts/check_release.py --review-build
python3 scripts/project.py serve --port 8000
# In another terminal with Playwright and Chromium installed:
python3 scripts/browser_smoke.py --url 'http://127.0.0.1:8000/?preview=0.1-alpha'
```

Headless native tests require a working local Xvfb display. Test saves are isolated from reader saves. An already-open browser game needs a reload to load the new build. The full browser test includes cache-refresh checks, but the final run stopped at the rain handoff before reaching them.

Windows/macOS launch testing, Safari/mobile game behavior and subjective full-film audio playback are not established by these checks. The release matrix still retains older content and platform approvals; review builds do not renew those approvals. [Earlier validation notes](../../development/visual-novel/reviews/releases/validation-before-final-pass.md) are preserved as history rather than mixed into the current results. Ren'Py remains pinned and the save namespace remains `Astravus-Book-I`.
