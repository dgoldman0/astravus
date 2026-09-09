# Graphics production

The game uses 78 selected runtime images. The [character-key gallery](../art/character-keys/index.html)
contains the current reference sheets and source-grounded rules for the depicted
cast. [Character continuity](CHARACTER_CONTINUITY.md),
[location continuity](LOCATION_CONTINUITY.md), [art direction](ART_DIRECTION.md)
and [compositing](GRAPHICS_COMPOSITING.md) govern the selected artwork.

Asset manifests and active production recipes remain here because the build
checks use them. Exact edit inputs, scripts, image hashes and protected-region
checks are required; a matching hash alone does not establish artistic quality.

Exploratory work and inspection history live in
[visual novel development](../../development/visual-novel/README.md). This includes
the [graphics ledger](../../development/visual-novel/reviews/graphics/ledger.json),
[earlier production narrative](../../development/visual-novel/reviews/graphics/production-review-history.md),
[character experiments](../../development/visual-novel/art/characters/README.md)
and [scene comparison viewer](../../development/visual-novel/art/character-refinements/review.html).
Do not put new trials, rejected candidates or review logs in the curated key gallery.

The [September 9 final review](../../development/visual-novel/reviews/graphics/final-reconciliation.md)
records 435 accepted dimensions and 111 explicitly inapplicable dimensions across
all 78 images. It links fresh source inspections of the human/CG, background and
familiar sets, plus the final Sage and familiar native comparisons. Earlier runtime
observations remain explicitly historical and limited to their inspected scope;
these counts do not claim every dialogue frame or release platform was reviewed.

From `visual-novel/`, run the current guards after an art change:

```sh
python3 scripts/check_assets.py
python3 scripts/graphics_review.py sync
python3 scripts/graphics_review.py status --strict
python3 scripts/project.py lint
```

`sync` refreshes paths and usage information without approving artwork. New pixels
or changed rendering need the relevant source or native scene inspection before
recording acceptance. Native framing is required when a sprite silhouette changes.
The [build instructions](../README.md) distinguish local review exports from
release approval; rebuilding a package does not renew unrelated listening or
platform checks.
