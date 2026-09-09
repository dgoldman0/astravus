# Archived validation checkpoint

Preserved during the September 9, 2026 organization pass. The statements below belong to earlier checkpoints and are not current build evidence. See [current validation](../../../../visual-novel/docs/VALIDATION.md) for the final-pass results.

# Book I validation — 0.1-alpha

**Current status: graphics production review complete; full release signoff remains open.**
The author-authorized production graphics pass has replaced the bounded design
demonstration, which is preserved in a recoverable path-scoped stash and
`../development/visual-novel/archive/local/design-proof/`. The current runtime differs from commit `c721791`;
old archives and technical receipts must not be described as a fresh polished
release or as proof for these assets.

[Graphics production review](../../../../visual-novel/docs/GRAPHICS_POLISH.md) records 78 selected images and
546 scoped dimension findings (434 accepted, 112 not applicable), with actual
source/native evidence. The new four-state treehouse, three added project/time
backgrounds, character repairs, familiar contacts and bounded matte cleanup have
been inspected. This renews graphics scope only. The current MP4 also has its own
[delivery check](../graphics/graphics-film-review.md). Desktop and web **graphics review
builds** have been rebuilt and checked against all 128 current runtime source
files; their actual hashes are in `test-results/review-exports.json`. This archive
check does not establish launch behavior on Windows/macOS or renew story/wording,
score listening, browser/platform or full release approval.

The [release matrix](../../../../visual-novel/docs/RELEASE_MATRIX.md) retains the previous 75-image release
checklist plus its shared checks. It has not yet been expanded/promoted for this
78-image production state. Ren'Py remains pinned to 8.5.3.26051504 and the save
namespace remains `Astravus-Book-I`. The current graphics review builds are for
inspection; they do not assert that the whole release has been freshly verified.

## Previous checkpoint evidence (superseded creative signoff)

## Story and reader knowledge

All **32 scenes, 658 dialogue blocks and 7,857 words** were reviewed against Book I and the author’s corrections. The restored source passage and bridge from scenes 24 to 25 remain unchanged. The story keeps the sudden loss, its unusual cultural context and the subsequent grief without adding metaphysical explanations. [The story/audio review](../audio/POLISH_STORY_AUDIO.md) and [glossary review](GLOSSARY_REVIEW.md) record the source comparisons.

The new **Glossary has eight entries and ten reveal stages**. Terms appear at their introduction, and later revelations expand definitions only when reached. Future titles and locked-entry counts stay hidden. Rollback, load and new game restore current-reading knowledge. Chapter jumps reconstruct earlier context, like People, while destination revelations wait for their own cues. The constellation passage now reads naturally without interrupting the family scene to define the adult partnership.

The **40–50 minute** reading estimate comes from the text and reading beats, not a timed human playthrough. The optional **2:58** closing theme adds about three minutes. Credits retain the repository, itch.io and SUNO links and the requested Daniel Goldman/ChatGPT/SUNO song credit. The afterword points toward Calista’s wider life without promising a release date. See [credits and release review](CREDITS_RELEASE_REVIEW.md).

## Visual quality and physical continuity

Every one of the **75 selected images** has a separate artistic-quality review against a deliberately chosen earlier image or reference, covering composition, light, detail, anatomy, expression, identity and sharpness. A correct iris or file hash is not an artistic approval. The three reports are [CG artwork](../graphics/ART_REVIEW_CG.md), [standing characters and stable CGs](../graphics/ART_REVIEW_STABLE.md), and [backgrounds and familiars](../graphics/BACKGROUND_FAMILIAR_QUALITY_REVIEW.md).

Compared with the previous committed build, **16 CGs and four Calista sprites** change. The stronger close path, arrival and morning compositions replace the rejected distant versions. Pond comfort returns to its original painting with only a small Calista iris correction; the waterwheel painting is restored byte for byte. Supported crouching and leaning explain their crown heights, so neither needed a body enlargement. The previous review called these pictures acceptable; the author subsequently rejected the remaining facial, shading and style inconsistencies. That judgment is reopened.

All **20 CGs** have explicit identity, face, age, iris and supported-proportion findings in [the character register](../../../../visual-novel/docs/cg-character-review.json). Four sprite and eleven CG iris corrections have deterministic recipes, source/output hashes and exact reproducibility checks in [iris-retouches.json](../../../../visual-novel/docs/iris-retouches.json). Independent checks confirm no changes outside their masks or to protected pupils and catchlights. That proof is separate from approval of the source painting.

[Location continuity](../../../../visual-novel/docs/LOCATION_CONTINUITY.md) covers **29 images across seven locations**. The treehouse retains its broad upper room, connected ladder/entry and separate lower hollow; festival and memorial retain shared plaza landmarks and a visible community. The close trio’s neighborhood walkway is a distinct source-supported place, not another version of Maia’s treehouse. [CG scale review](../graphics/CG_SCALE_REVIEW.md) distinguishes stature from pose and depth; production proportions do not invent canonical centimeters or exact ages.

The runtime support-plane pass corrects construction-path standing positions, places the children on the treehouse’s clear floor at one shared camera distance, and moves several familiar placements onto actual floors/ledges. It preserves their relative size. **Twelve UI-hidden captures and eight assertions** support these changes in [the grounding review](../graphics/CONSTRUCTION_GROUNDING_REVIEW.md).

The [integrated scene review](../graphics/RUNTIME_VISUAL_REVIEW.md) inspects the assembled game, including portraits, dialogue, staging and the larger reading controls. Native captures supply 29 scene views plus the news transition; final browser frames supply readable dialogue for all 32 scenes, including the three native screenshot gaps. The native functional suite separately traverses every scene. This distinguishes actual visual evidence from automated progression.

## Reader controls and usability

The final browser usability probe passes **five grouped control checks**, with **41 fresh captures at 1280×720 and 960×540** and no reported engine/browser errors. The screenshots were inspected separately for legibility, spacing, visible focus, pointer targets, feedback and predictable destinations. [The usability review](USABILITY_REVIEW.md) records the actual observations and limits.

That visual inspection caught concatenated shortcut/explanation text in the reading guide. Fixed-width label containers and a separate gap now keep those columns aligned. The bottom reading controls also use larger labels, which fit at both tested sizes. Save switches away from the read-only Automatic page; empty or incompatible Load slots stay disabled. Warning, overwrite and delete cancellation preserve the current story or saved slot. The unread-chapter warning, its opt-out setting, People/Glossary navigation, larger dialogue, stronger contrast, reduced motion and theme pause/skip controls were exercised through real mouse and keyboard input.

## Completed technical checks

| Check | Final evidence |
| --- | --- |
| Native full-book integration | **156/156 assertions pass**, including progression, saves, menu state, People/familiars, chapter reconstruction and cleanup. `test-results/release-matrix/native-playthrough.log`. |
| Standing-character framing | **26 rendered silhouettes pass**, with feet within 2 virtual pixels and same-stage variants within 3 pixels. `test-results/release-matrix/native-framing.log`. |
| Native glossary | **25/25 assertions pass**, including rollback, loading, new game and chapter knowledge. |
| Native closing theme | **19/19 assertions pass**, including timing, pause/resume, reduced motion, skip/replay and audio state. |
| Final browser playthrough | All **32 normal scenes and 32 backward chapter jumps pass**, including corresponding story/character state, glossary reveals, portraits, audio ordering, theme, spoiler controls, actual credit-link clicks, cache refresh and unsupported-graphics fallback. `test-results/release-matrix/browser-playthrough.log`. |
| Regression tests | **50 tests pass**, covering review invalidation, source/reveal state, build gates, review-only artifacts, comparison references, version-reset export retention and the exact allowed generated engine files. |
| Asset and continuity guards | **75 selected files, 160 complete generation records, 20 CG reviews, 29 location views and 26 sprite layouts pass**. Iris recipes and their scripts are tracked inputs. |
| Syntax and source references | Final Ren’Py lint passes with **658 dialogue blocks and 7,857 words**. |
| Audio measurements | All **20 delivered audio files and four related-cue balance checks pass**. `test-results/release-matrix/audio-measurements.log`. |

The song now enters at approximately **0.4 LU** above the preceding home music, rather than 6.4 LU. Hesitant and practiced flute phrases are about **0.3 LU** apart; the initial broken breath remains deliberately quieter and unskilled. Repeated score/ambience cues continue across adjacent scenes instead of restarting. The original song WAV remains unchanged. See [audio sequence review](../audio/AUDIO_SEQUENCE_REVIEW.md).

## Closing film

The final [standalone movie](../../../../visual-novel/build/closing-theme.mp4) is **1920×1080 at 60 fps, 126.5 MiB**, using H.264 video and stereo AAC audio. All **10,666 frames** decode; their timestamps are unique and exactly 1/60 second apart. The complete **177.76-second** source song remains present, with measured encoded level change of −0.0556 dB and no applied mastering change.

All 15 settled compositions and all 14 dissolves were inspected. The overlapping pictures hold their camera positions and blend smoothly; movement resumes between overlaps. The review also investigated keyframe difference peaks, previously classifying the peaks as fine-detail compression refresh. The author still reports jitter; those measurements did not justify editorial approval. The [final film report](../graphics/FINAL_FILM_REVIEW.md) records those observations, measurements and limits. Runtime and export use the same final cue sheet and selected images; reduced motion intentionally holds images and uses cuts.

## Reproduce

From `visual-novel/`:

```sh
python3 scripts/project.py review --strict
python3 scripts/release_review.py run asset-registers
python3 scripts/release_review.py run glossary-rules
python3 scripts/release_review.py run regressions
python3 scripts/release_review.py run lint
python3 scripts/release_review.py run audio-measurements
python3 scripts/project.py test --headless
python3 scripts/project.py test --headless --suite character_framing_review
python3 scripts/project.py test --headless --suite glossary_review
python3 scripts/project.py test --headless --suite closing_theme_review
python3 scripts/project.py build
python3 scripts/project.py web
python3 scripts/project.py serve --port 8000
# Separate terminal with Playwright and Chromium installed:
python3 scripts/browser_smoke.py --url 'http://127.0.0.1:8000/?preview=0.1-alpha'
python3 scripts/browser_usability.py 'http://127.0.0.1:8000/?preview=0.1-alpha'
python3 scripts/check_release.py
```

Normal build commands require current content approval; temporary `--review-build` artifacts cannot pass final signoff. Test state is isolated from the reader’s saves. Reports, screenshots and packages are ignored development artifacts. Only selected runtime assets ship; no before/after artwork bundles or previous release archives are included.

## Verification limits

Windows and macOS archives are constructed on Linux; **target-OS launch testing has not been performed**, and macOS is unsigned. Safari, mobile layouts, self-voicing output and physical speaker/headphone playback remain unverified. Technical audio measurements and cue review are not a subjective listening assessment.

The movie review uses complete decoding, native 60 fps timestamps, inspected frame sequences and measured motion/blending. It does not claim subjective real-time audiovisual viewing or verified word-by-word lyric alignment. These explicit limits remain separate from required artistic, narrative, functional and package checks.

## Release artifacts

| Artifact | Size | Use |
| --- | ---: | --- |
| [PC ZIP](../../../../visual-novel/dist/astravus-book-one-0.1-alpha-pc.zip) | 223.4 MiB | Windows and Linux download, with both launchers. |
| [macOS ZIP](../../../../visual-novel/dist/astravus-book-one-0.1-alpha-mac.zip) | 217.9 MiB | macOS app bundle; unsigned and not launched on macOS here. |
| [Browser ZIP](../../../../visual-novel/build/web.zip) | 197.5 MiB | HTML game with `index.html` at the ZIP root. |
| [Closing film](../../../../visual-novel/build/closing-theme.mp4) | 126.5 MiB | Separate 1080p60 video; the game plays the same stills and song directly. |

The current PC, Mac and browser candidates pass ZIP integrity and exact equality against **125 runtime/source files**, plus expected launcher/permission checks and version metadata. Only the pinned engine’s generated `build_info.json` and `bytecode-312.rpyb` are allowed under its cache directory; development caches, tests, tools, marketing files and saves are excluded. Actual archive identities are recorded in `test-results/release-exports.json`. Superseded Astravus desktop exports were removed only after replacement archives passed integrity checks. Nothing was uploaded or published.

The final PC ZIP also passes a **bundled Linux startup/quit smoke test**. An isolated temporary extraction launched its own `.sh` and bundled executable, reached the rendered title with the correct artwork, fonts, controls and `Version 0.1-alpha`, then exited cleanly through its Quit button. No traceback was reported and the archive hash remained unchanged. This used Xvfb, Mesa software rendering and dummy audio; it checks packaged initialization/title/quit, while the full native story tests are separate. Evidence is in `test-results/packaged-linux/`; the extraction and isolated saves were removed afterward.
