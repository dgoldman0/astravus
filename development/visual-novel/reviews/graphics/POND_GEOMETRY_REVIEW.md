# Pond geometry correction and pairwise review

The author reopened pond consistency after the graphics pass. The earlier
checks established plausible local contacts, but did not prove that these
pictures depicted the same physical basin. Four landscape repairs and a fresh
seven-view comparison now resolve the scoped findings. The final native run has
12 inspected captures and 20 passing assertions; see [source findings](pond-repair-review.md)
and [runtime findings](pond-runtime-review.md). A prior face, texture or grounded-knee
review alone cannot settle basin geometry.

The governing production view is
[garden-pond.png](../../../../visual-novel/game/images/backgrounds/book-one/garden-pond.png). Its shallow
water, low irregular coping and adjacent ground define the geometry.
[garden-work-area.png](../../../../visual-novel/game/images/backgrounds/book-one/garden-work-area.png)
is a secondary wider view that must agree with that master. This is an explicit adaptation choice: the source says
there are garden ponds and a small shallow pond, without prescribing exact
measurements or making every pond event occur at one named basin.

The initial side-by-side inspection exposed the problem: the wider work area,
planting CG and comfort CG gave the basin a conspicuous elevated exterior wall. The
establishing pond, completed waterwheel and rescue edge instead read as low,
accessible coping beside the ground. “Different angle” is insufficient unless
one coherent ground/water/wall construction can explain both views.

| Selected view | Review requirement |
| --- | --- |
| garden-pond | Governing shallow basin; retain its low coping/ground/water relationship. Recheck against each repaired view. |
| garden-work-area | Repair the raised pool-wall reading while retaining an ample dry planting bank and pots. |
| garden-compromise | Repair matching raised-wall geometry behind the planting trio. Preserve bodies, pot contacts and expressive faces. |
| pond-comfort | Repair the raised exterior wall behind the seated/crouched group. Preserve the figures, familiar contacts and bank composition. |
| pond-rescue | Remove the separate-looking water ribbon behind the far bank; retain the original foreground coping, reach and dry-knee support. Recheck the connected shoreline against the master and comfort shot. |
| theme-waterwheel-team | Recheck the low bank and small construction-test arrangement; this remains a theme illustration, not the completed in-pond story state. |
| waterwheel | Recheck the added small wheel against the otherwise governing basin; a wheel must not change ground elevation or pool construction. |

Review these independently before recording a current geometry acceptance:

1. **Waterline, coping and dry ground:** mark where water meets the inner edge,
   the coping top, and the adjacent dry paving in the master and candidate.
   Their vertical relationship must describe one low basin. A tall exposed wall
   or elevated water surface needs a source/production reason; camera elevation
   alone cannot move the water above the neighboring ground.
2. **Perimeter and thickness:** compare the visible near arc, far arc and side
   returns. Wall thickness, the basin's broad outline and its scale relative to
   the people/pots must admit a coherent camera/depth change. Do not stretch a
   crop until unrelated curves happen to line up.
3. **Shared anchors:** compare at least three visible landmarks when the crop
   permits: recognizable coping/edge junctions, the inlet side, fence/plant
   boundary and dry access path. Distinguish a fixed boundary from movable pots,
   tools or plants. Cropped-out anchors remain unobserved, not a pass or failure.
   Trace every visible patch of water back to the same basin. An isolated far
   ribbon beyond a supposed bank must not introduce a second pool or contradictory
   shoreline; a genuine peninsula needs a coherent connection around it.
4. **Reach and support:** inspect native details of knees, boots, paws, pot
   bottoms and rescue hands after the environmental repair. Raising paving or
   lowering the wall must not bury feet, float figures or make Lyra unreachable.
5. **Whole composition and scene sequence:** compare equal-aspect full images,
   then actual pond→rescue→comfort gameplay and planting/waterwheel uses. Preserve
   rich paint, readable faces and coherent light. Geometry approval cannot
   override an artistic regression or a contradictory illustrated action.

A lightweight annotated ground/water profile or measured anchor sketch can make
an ambiguous view reviewable. It must label inferred geometry as a production
model, not canonical dimensions or a recovered full 3D reconstruction. Each
review should identify its exact master/candidate hashes, visible anchor pairs,
any camera explanation, and which hidden features could not be inspected.

## Reopening and recording evidence

The [location register](../../../../visual-novel/docs/location-continuity.json) retains the seven pond findings
and their explicit resolutions. Four required landscape repairs; three unchanged
views received a fresh pairwise comparison. These were focused gates, not a
withdrawal of unrelated character, story or art findings. Bank-height, pairwise
geometry and connected-water invariants are now required for all seven views.

The graphics ledger API records an actual observed failure or remaining scope:

```sh
python3 scripts/graphics_review.py record game/images/backgrounds/book-one/garden-work-area.png \
  --dimension setting_geometry --outcome needs_rework \
  --reviewer "Reviewer" --notes "Concrete observed geometry mismatch" \
  --evidence ../development/visual-novel/reviews/graphics/POND_GEOMETRY_REVIEW.md \
  --comparison-reference "game/images/backgrounds/book-one/garden-pond.png"
```

Use `partial` for a reviewed master/related image whose new pairwise comparison
is still pending. `sync` only updates the inventory and preserves outcomes;
changed pixels/references automatically make previous receipts stale. After
actual source and runtime inspection, record `accepted` with that new evidence,
update only the applicable location findings/signatures, and run:

```sh
python3 scripts/check_assets.py --provenance-only
python3 scripts/check_assets.py
python3 scripts/graphics_review.py status --strict
```

No old receipt should be bulk-refreshed to make the matrix green. This document
records this completed re-review and the method for reopening future changes.

## Same-version replacement builds

The release target remains **0.1-alpha** in `docs/release-matrix.json` and
`game/options.rpy`. Desktop/web commands check that agreement before packaging,
even with `--review-build`; pruning, provenance recording and archive validation
also check it. This replaces the same recognized filenames, rather than silently
incrementing the version. The user's release target should change only with a
new explicit version decision. Build hashes and web cache-busting IDs can still
change while the public version stays fixed. Old pushed commits are preserved;
subsequent work uses new commits.
