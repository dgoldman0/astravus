# Release acceptance matrix — 0.1-alpha

The [machine-readable matrix](release-matrix.json) is the final-pass checklist. It covers **32 story scenes, 75 selected images and 23 shared release checks**. The [evidence register](release-evidence.json) holds one current receipt per check. No earlier development log is automatically a pass for the new build.

Run `python3 scripts/project.py review` from `visual-novel/` to see current results. This also writes a full table to `test-results/release-matrix-status.md` and structured status to the adjacent JSON file. Each receipt identifies its reviewer, method, UTC date, exact input signature, evidence files and their hashes. A missing or changed source, new file in the reviewed scope, altered acceptance criterion, changed reference or modified evidence makes an earlier result **STALE**.

**A technical check does not approve artistic quality.** A file hash records which picture was inspected; it cannot tell whether Cassia's face is natural, whether the children look the right age, whether a composition has become dull, or whether the story flows. Manual rows require an explicit comparison and observations. Required checks cannot be waived as platform limitations.

The author's September 5 review reopened creative approval. The bounded design
demonstration is now archived; the authorized production graphics pass is
recorded separately in [GRAPHICS_POLISH.md](GRAPHICS_POLISH.md) and its 78-image
ledger. Its current source/native findings replace the old graphics checkpoint
for that scope. The release matrix still describes the earlier 75-image export
set and must be reconciled before full release signoff. Its prior passing rows
are not automatically renewed for changed production assets.

The separate required `score-editorial` row continues to cover musical variety
and emotional fit through contextual listening. No graphics-only review grants
story/audio approval, validates another platform, or certifies an old archive as
a newly polished build.

## Governing references

| Subject | Authority and acceptance |
| --- | --- |
| Story and pacing | [Book I prose](../../revision/latest.md), the author's corrections and [source coverage](BOOK_ONE_COVERAGE.md). Each scene row identifies its passage, key development, stage and adjacent-transition review. Preserve the restored 24→25 bridge, rare loss, mortality reflection and grief order; do not add metaphysical answers. |
| Terminology and revelations | [Glossary data](../game/glossary.json), [source coverage](BOOK_ONE_COVERAGE.md) and the author's constellation correction. Definitions grow with what the current reading has introduced. Dialogue carries action and emotion without inserting a dictionary lesson. |
| Human and familiar identity | [CG character register](cg-character-review.json), [character continuity](CHARACTER_CONTINUITY.md), aligned biographies and approved reference assets. Face, iris, anatomy, age and expression have their own approval in addition to stature. |
| Relative stature | [Shared layout contract](../game/character_layout.json). Calista and Cassia are near-equal peers; Joren is modestly taller; Kael reads older/larger and Lyra distinctly smaller. These are production proportions, not invented canonical centimeters. Seated and kneeling CGs must use actual torso/limb/support-plane evidence. |
| Places and physical action | [Location register](location-continuity.json). The treehouse keeps its upper room, connected ladder/door and separate lower hollow; plaza variants keep landmarks and believable attendance; garden pots and pond action have plausible support surfaces. |
| Artistic quality | A separate `quality-*` row for **every selected image** requires a deliberately chosen prior Git/generation/reference image. Compare focal presence, lighting and tonal depth, material detail, anatomy/expression, identity/stage, sharpness and accumulated edit degradation. The candidate from commit `7b1c760` is a comparison starting point, not an automatic assertion that it is the best version. Author rejection blocks approval even when iris, height and geometry checks pass. |
| Sound | [Audio direction](AUDIO_DIRECTION.md), source audio provenance and actual cue placements/gains. Preserve the broken first breath, later hesitant phrase and practiced melody in order. Check all delivered audio technically; a separate required listening review establishes musical variety, phrasing, instrumentation, emotional fit and purposeful silence. Cue order or loudness cannot pass that review. |
| Theme | [Cue sheet](../game/closing_theme.json), [motion review](../../development/visual-novel/reviews/graphics/POLISH_MOTION.md) and [song provenance](closing-theme-audio.json). Character presence, varied framing, stable camera motion and blended fades must coexist with approved art. The closing song recalls earlier happiness; it is not a new adventure after Joren's death. |
| Reader usability | Separate manual `reader-usability` review checks discoverable labels, text/contrast/spacing, keyboard focus and pointer targets, predictable Back/Cancel/Escape, safe warnings, save/load and empty states, knowledge-page navigation and theme feedback. Functional assertions do not replace this review. |
| Reader controls | Normal-play and jump/save/rollback state, People/familiars, growing glossary, chapter warnings and opt-out, menus, navigation, text layout, reduced motion, theme pause/skip/replay and channel cleanup. |
| Credits and release | Actual 0.1-alpha labels, supported reading estimate, hopeful afterword, repository/itch/SUNO links, current PC/Mac/web archives, exact runtime bytes and exclusions. Archive construction is separate from launch testing on each target OS. |

## How evidence is collected

Automated rows run their declared command and capture a fresh log. The runner hashes inputs both before and after execution; a command cannot pass if its inputs changed while it ran. For example:

```sh
python3 scripts/release_review.py run glossary-rules
python3 scripts/release_review.py run audio-measurements
python3 scripts/release_review.py run native-playthrough
```

Manual rows are recorded **only after the named review has actually happened**. Evidence can be a current inspection report, screenshot/contact sheet, or detailed comparison record. Notes must describe what was inspected and what supports the result. The following is a command template, not a completed review:

```sh
python3 scripts/release_review.py record scene-01 \
  --outcome pass --reviewer REVIEWER \
  --notes 'Specific findings from reading the current scene and transition.' \
  --evidence docs/CURRENT_REVIEW_REPORT.md
```

Image-quality approval additionally requires `--comparison-reference`, naming the actual selected Git blob, generation or approved image used for comparison. A failure can be recorded immediately with its finding; it remains failed until corrected and freshly reviewed. Reviewers must not copy another row's pass merely because the pictures share a generation batch.

```sh
python3 scripts/release_review.py record quality-cg-book-one-theme-path-friends \
  --outcome pass --reviewer REVIEWER \
  --comparison-reference 'git:ACTUAL_COMPARISON_BLOB' \
  --notes 'Specific composition, lighting, detail, facial and sharpness observations.' \
  --evidence docs/CURRENT_ART_REVIEW_REPORT.md
```

The register stores one latest result for each row and writes atomically so simultaneous reviewers cannot erase each other's work. Review reports and source history remain in Git; no before/after image bundles are added to the game.

## Completion and limits

The phases separate checks by the artifacts they need:

1. **Content:** all scene/source reviews, per-image quality approvals, character/location comparisons, terminology, credits, asset guards, audio measurements, musical editorial/listening review, regressions and lint.
2. **Runtime:** final native playthrough, framing, glossary/theme tests, actual scene/UI review and audio cue review.
3. **Exports:** final browser behavior and presentation, ZIP integrity/source equality, final movie decode/editorial review and target-platform limitations.

Normal `build` and `web` commands enforce the content matrix as well as the asset guard. `python3 scripts/project.py review --strict` then checks final release signoff. These commands fail while any required row is pending, stale, blocked or failed. An explicit `--review-build` can produce temporary browser or desktop artifacts before content approval. Their exact hashes are recorded as review builds in `build/release-builds.json`; successful browser checks on them remain **REVIEW**, and package signoff rejects them. Rebuild normally after content approval to create candidates for final runtime/export checks.

The package audit compares every delivered runtime source file and README byte-for-byte and verifies ZIP CRCs, launchers and executable permissions. Ren’Py 8.5.3 intentionally includes `game/cache/build_info.json` and its Python 3.12 `bytecode-312.rpyb`; these two generated runtime files are checked for correct metadata and valid compression. Other developer caches and saved games are excluded. The local pinned SDK’s `renpy/common/00build.rpy`, `launcher/game/distribute.rpy` and `renpy/script.py` establish this narrow exception.

`LIMITED` means explicitly **unverified**, never passed. Windows/macOS launch testing, unsigned macOS packaging, Safari/mobile layouts, physical speaker/headphone playback and self-voicing can be reported honestly here without turning them into fictitious successes. Any required artistic, narrative or functional failure remains open. [VALIDATION.md](VALIDATION.md) is the concise release report and must agree with the live matrix.
