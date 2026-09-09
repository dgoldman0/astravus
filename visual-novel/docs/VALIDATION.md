# Book I validation — 0.1-alpha

The September 9, 2026 visual pass has been rebuilt into the PC, macOS and browser **review builds**, plus the standalone closing film. These packages include the corrected Lyron wardrobe and the final Sage/familiar touchups. Full release approval remains separate from this graphics and rebuild checkpoint.

The browser package was rebuilt again at **10:22:47 AM EDT** with the audio handoff repair. Its subsequent full browser run passes. The [repair review](../../development/visual-novel/reviews/audio/browser-handoff/README.md) records the resolved failure, exact package and focused transition/save checks. The native game files and standalone film are unchanged by this browser repair.

The current art review covers all **78 selected images**: 29 backgrounds, 20 scene illustrations, 26 human sprites and three familiars. The [character gallery](../art/character-keys/index.html) contains 20 selected sheets for all 17 named depicted characters, with separate early/later keys for the three childhood friends. Current findings are in the [character and scene review](../../development/visual-novel/reviews/characters-and-scenes.md), [background review](../../development/visual-novel/reviews/backgrounds.md) and [familiar compositing review](../../development/visual-novel/reviews/familiar-compositing.md).

## Checks completed for this checkpoint

| Check | Result |
| --- | --- |
| Asset provenance and continuity | 78 selected files, 172 generation records and 30 active production edits pass; 20 CG reviews and 30 location views across seven locations are current. |
| Native full-book integration | 156/156 assertions pass through the existing `chapter_playthrough` suite. |
| Native standing-character framing | All 26 silhouettes pass; feet remain within 2 virtual pixels of the shared baseline and wardrobe heights within 3 pixels. Sage has fresh before/after native renders. |
| Regression tests | 67 tests pass, including review invalidation, relocated evidence paths, browser audio behavior and safe archive patching. |
| Ren'Py lint | Passes on the pinned 8.5.3.26051504 SDK: 659 dialogue blocks and 7,873 words. |
| PC, Mac and browser archives | ZIP integrity and byte-for-byte equality pass for all 144 packaged runtime/README files; expected launchers, permissions, version and generated engine files pass. |
| Browser integration | Full Chromium playthrough passes all 32 scenes and 32 reverse chapter jumps, rain, save/load, closing-theme controls, Credits, reload/Continue, cache refresh and unsupported-graphics handling. Separate rapid and normal-fade checks verify rain and music both play and survive save/load. See the [completed browser log](../../development/visual-novel/reviews/audio/browser-handoff/browser-playthrough.log). |
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

Current archive identities and passing browser checks are retained in [the audio repair rebuild receipt](../../development/visual-novel/reviews/audio/browser-handoff/rebuild.json). The [current export check](../../development/visual-novel/reviews/audio/browser-handoff/export-check.json) verifies the corrected browser engine and all 144 game/README files; local copies remain at `test-results/review-exports.json` and `build/release-builds.json`. The [earlier organization receipt](../../development/visual-novel/reviews/organization/rebuild.json) retains the pre-fix package and failed-browser history. The [film render receipt](../../development/visual-novel/reviews/film/render-result.json) records all 22 frozen inputs, complete stream decoding and the expected 10,666 frames. The original WAV and game OGG are unchanged. No files were published or uploaded.

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
python3 scripts/browser_audio_check.py
python3 scripts/browser_smoke.py --url 'http://127.0.0.1:8000/?preview=0.1-alpha'
```

Headless native tests require a working local Xvfb display. Test saves are isolated from reader saves. An already-open browser game needs a reload to load the new build; cache refresh passes in the completed browser test.

Windows/macOS launch testing, Safari/mobile game behavior and subjective full-film audio playback are not established by these checks. The release matrix still retains older content and platform approvals; review builds do not renew those approvals. [Earlier validation notes](../../development/visual-novel/reviews/releases/validation-before-final-pass.md) are preserved as history rather than mixed into the current results. Ren'Py remains pinned and the save namespace remains `Astravus-Book-I`.
