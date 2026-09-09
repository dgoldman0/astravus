> Historical production-review narrative retained during the project organization. Current status and build instructions are in the visual novel production docs; this record does not approve a later build.

# Graphics production review

**September character pass:** all 17 depicted named characters now have
[visual keys](../../../../visual-novel/art/character-keys/index.html), including separate early and
later childhood sheets for the three friends. The approved opening trial is
installed; Arin and Sage have matching sprite refinements. Lyra's sprite and
three illustrations receive bounded eye/face adjustments, Thalia's irises are
green, and Lyron has a new overlapping woven garment following the author's
targeted wardrobe correction. Nine selected images changed; the other 69 retain
their pixels. [Before/after viewer](../../art/character-refinements/review.html),
[source-art audit](../../art/character-refinements/VISUAL_AUDIT.md) and
[native checks](../../art/character-refinements/runtime-checks.json) identify the work
and its evidence. Exact garment construction remains production interpretation.

The production ledger is [graphics-polish.json](ledger.json). It covers
all **78 selected runtime images and 546 dimension reviews**: 435 scoped
acceptances and 111 justified not-applicable findings. Current asset validation
covers 172 generation records, 30 active production edits, 20 CG character
reviews, 30 recurring-location views and 26 measured human silhouettes.
Reviews are tied to actual inspections; recomputing a hash does not approve art.

The current native checks passed the full chapter playthrough (156 assertions),
human framing (2 assertions with all 26 measured sprites), closing-player tests
(19 assertions) and paused montage capture (3 assertions and 15 compositions).
Ren'Py lint passed. The linked reports distinguish fresh captures from retained
evidence for unchanged art and rendering. This pass does not rebuild the earlier
desktop/web archives or encoded closing film; those remain the previous graphics
review builds. It does not renew release or audio-listening approval.

## Earlier environment and compositing pass

The earlier pond geometry correction completed four landscape repairs aligning the
working-bank, planting, comfort and rescue views with the governing low basin.
All seven related views received a focused pairwise review of water/coping/ground
height, connected shoreline and shared visible anchors. The final native run
passed 20 assertions with 12 inspected captures, including the actual paused
planting theme cue. [Source review](pond-repair-review.md),
[geometry criteria](POND_GEOMETRY_REVIEW.md) and
[native review](pond-runtime-review.md) bind the current findings.

The original 75-image set gained three derived scene-state backgrounds: later
treehouse, workshop construction and family painting. At that stage, twenty-five
selected assets had active production-edit recipes. Its asset validation covered
78 files, 160 generation records, 25 reproducible edits, 20 CG character reviews,
30 recurring-location views and 26 measured human silhouettes. The following
receipts describe that earlier pass; the September records above supersede them
where a character image changed.

The review combines the independent 73-frame native story/UI/support inspection,
fifteen final environment-state captures, fifteen actual paused theme-player
views, two Barkley matte views and the separately captured courtyard opening.
Dedicated human bright/dark and garden UI frames supplement those contexts.
Every selected image has an explicit representative native view. This does not
mean every dialogue line, possible window size or camera movement was inspected.
The scene-15 support view has hidden UI; tiny irises/notches rely on their native
source-detail reviews rather than reduced gameplay frames.

The four treehouse states now distinguish early/later furnishing and dry/rainy
light. Final native review confirmed Shadow on the moved table, Nibble clear of
Calista's boot and the daylight comfort CG connected to the preceding room.
Workshop/painting supplies occupy their actual work surfaces. Barkley's isolated
matte pass removes a few green edge flecks while preserving the gold coat. Fine
painted gold/pale rims remain on some fur/hair; no perfect-matte claim is made.

Actual scoped observations are in [source CG review](graphics-cg-audit.md),
[CG repair review](graphics-cg-repair-review.md),
[settings and sprite review](graphics-background-sprite-audit.md),
[human sprite review](graphics-human-sprite-audit.md),
[environment review](graphics-environments.md),
[visible support review](graphics-support-art-review.md),
[native review](graphics-runtime-review.md),
[final state review](graphics-state-runtime-review.md),
[theme fitting](graphics-theme-runtime-review.md) and
[Barkley matte review](graphics-barkley-matte-review.md).
[Runtime reconciliation](graphics-runtime-reconciliation.json) proves the narrow
code differences between capture batches and names which new states received
fresh captures. The per-image ledger binds the exact evidence and artwork.

Each image records its starting SHA-256 and immutable Git blob, current bytes,
manifest, runtime aliases, scene uses, conditional speaker portraits, closing
theme shots and interface uses. Character, stature and location facts point back
to the existing contracts rather than creating another conflicting design bible.
The usage inventory follows the book's actual linear call/return sequence through
all 32 scenes and invokes the existing portrait resolver against that staged
state. It is a static inventory, not a native game rendering check.

Review identity, anatomy/expression, age/stature, setting geometry, lighting/style/
detail, scene truth/action and runtime compositing independently. For an empty
environment, a reviewer may record a dimension as not applicable with a reason.
Artistic quality remains a separate judgment from correct iris pigment, pixel
hashes or physical measurements. Choose an explicit comparison reference; the
latest image is not automatically the strongest reference.

From `visual-novel/`:

```sh
python3 scripts/graphics_review.py sync
python3 scripts/graphics_review.py status --strict
```

`sync` refreshes the inventory without approving art or erasing prior reviews.
`status --strict` fails while any dimension is pending, partially reviewed,
needs rework or is stale,
or when a runtime image differs from its asset manifest. Changed image bytes,
relevant source/reference files or evidence invalidate recorded reviews.
Source-art dimensions bind the painting, relevant references, story role and edit
provenance. Shader/player implementation changes specifically invalidate runtime
compositing; they do not erase an unchanged source painting's face/room review.
The underlying record still identifies the complete current runtime context.

Record only an actual completed inspection, with its current evidence:

```sh
python3 scripts/graphics_review.py record game/images/cg/book-one/theme-path-friends.png \
  --dimension anatomy_expression --outcome needs_rework \
  --reviewer "Reviewer name" --notes "Concrete observed finding" \
  --evidence ../development/visual-novel/reviews/graphics/graphics-cg-audit.md \
  --comparison-reference "git:<deliberately selected blob>"
```

The other outcomes are `accepted`, `partial` and `not_applicable`. A partial
runtime review records actual inspected uses in `runtime_coverage`, along with
the specific remaining contexts; it does not convert those gaps into acceptance.
This command does not
update the older release matrix or manufacture a visual inspection.

## Refreshing edited assets

Update the selected entry in its existing asset manifest with actual PNG hash,
dimensions/mode and the new edit provenance. Do not relabel a GIMP/geometry edit
as image generation or as an iris-only correction. `check_assets.py` validates
active `production_edit` pointers into `graphics-edits.json` or
`environment-edits.json`: the exact recipe, immutable input bytes, script,
output hash, canvas/mode and actual changed-pixel count. Operation-specific
outside-mask measurements remain the producer's asserted, hash-bound evidence;
they do not certify artistic quality. Geometry may deliberately move lids and
pupils. The older iris-only recipes retain their strict pupil/catchlight rules
where still selected. Replace their active pointer only when a production edit
supersedes that output, retaining its earlier source lineage in the new recipe.

During production, `python3 scripts/check_assets.py --provenance-only` checks
selected files and technical lineage while artistic reviews remain open. The
normal command retains its visual-registry and character-layout requirements;
the narrower mode cannot serve as a release or artistic signoff.

For a changed human sprite, measure the real output before updating its entry in
`game/character_layout.json`; retain the existing age/stature contract unless a
review establishes a deliberate change:

```sh
python3 -c 'from pathlib import Path; import sys; sys.path.insert(0,"scripts"); from character_layout import measure; print(measure(Path("game/images/characters/book-one/cassia-young.png")))'
python3 scripts/character_layout.py
```

After new pixels and their relevant reviews are complete, refresh CG and location
review hashes/reference signatures in their existing registries. The helpers are
`check_assets.cg_reference_signature(data, item)` and
`check_assets.location_reference_signature(location)`. Recomputing a signature
does not establish that a character or location passed visual review.

Run the appropriate existing checks only after the new provenance/review records
are ready:

```sh
python3 scripts/check_assets.py
python3 scripts/project.py test --headless --suite character_framing_review
python3 scripts/project.py test --headless --suite environment_grounding_review
python3 scripts/project.py test --headless --suite environment_state_review
python3 scripts/project.py lint
python3 scripts/graphics_review.py sync
python3 scripts/graphics_review.py status --strict
```

The first two native suites address sprite framing and recurring physical
placement. `environment_state_review` captures the revised early/rain/later/
remembrance rooms, dispute familiars, Cassia before/after the comfort CG,
the two project-specific work surfaces, Lyra's scene, annual remembrance and
the actual loss dialogue after its one-second pause. It records 15 frames and
their exact story/input state; these captures still require visual inspection.
The completed native runs and their observed findings are recorded above and in
the linked runtime reports. The replacement movie has also been rendered; its
bounded check verifies the updated planting cue and unchanged encoded song. See
[delivered film review](graphics-film-review.md) for the exact movie hash, checked
frames and limits; native static views do not certify encoded motion.

The earlier desktop and web archives were replaced under the same **0.1-alpha**
filenames as **graphics review builds**, then checked with
`python3 scripts/check_release.py --review-build`. All 128 packaged runtime source
files match the reviewed working tree, including the four current pond repairs.
`test-results/review-exports.json` records the exact PC, Mac and web ZIP hashes.
The version lock rejects accidental version changes before packaging. This
archive-integrity check remains separate from full release/platform approval;
editing materials, tests and local review artifacts are excluded.

## Recovering the archived proof

The proof source is preserved in the path-scoped Git stash
`c251e6da134771b833f84a6d9efa2104e878c08a`, titled
“Archived bounded design proof before graphics production polish”. It contains
exactly 31 proof files: 23 documents/art/templates and eight scripts. The four
release documents and `marketing/` were excluded and verified unchanged.

Generated media was moved, without copies, to
`../development/visual-novel/archive/local/design-proof/`. Its 98 regular files and six symlinks were verified
after the move. The archive also holds the proof's old test results and two music
logs. `ARCHIVE.json` records every move. The preview server was stopped.

To recover the whole proof, first ensure its original destinations are free.
Run these commands from the **Astravus repository root**, not `visual-novel/`:

```sh
git stash apply c251e6da134771b833f84a6d9efa2104e878c08a
mv development/visual-novel/archive/local/design-proof visual-novel/build/design-proof
mv visual-novel/build/design-proof/_test-results visual-novel/test-results/design-proof
mv visual-novel/build/design-proof/_logs/design-proof-music-render.log visual-novel/build/
mv visual-novel/build/design-proof/_logs/design-proof-music-browser.log visual-novel/build/
rmdir visual-novel/build/design-proof/_logs
```

Use `apply`, which retains the archive's stash entry. Relative art symlinks become
usable again when their source docs and generated directory return to their
original locations. Recover one source file without restoring the whole proof:

```sh
git show c251e6da134771b833f84a6d9efa2104e878c08a^3:visual-novel/scripts/gimp_cassia_repair.py
```
