# Bounded hair-edge cleanup

The native dark-scene review exposed bright yellow/green speckles around Lyra's
fine curls. The shader now looks slightly farther into nearby green backing for
**color despill only**, while retaining the original alpha-key calculation.
This reduces a small amount of remaining green contamination without changing
the source artwork or deliberately erasing fine hair strands.

The production owner and independent reviewer inspected the paired bright/dark
Lyra crops, complete 1920-pixel scene frames, and native Selene/Cassia comparisons.
They found a modest improvement with preserved curls, green irises and white hair.
Strong golden painted outlines remain on Lyra; a pale outer edge remains on some
Selene curls in both versions. This is not a claim that all fringing or every
source-lighting mismatch is resolved. Further color suppression cannot safely
substitute for inspecting the painting's intended rim light.

The focused native `character_framing_review` ran after the shader change:
2/2 assertions passed, all 26 silhouettes retained the shared framing contract,
wardrobe heights stayed within 3 pixels and feet within 2 pixels of the baseline.
This geometry result is separate from the actual edge inspection.

| Representative native sprite | Changed color pixels | Alpha / red / blue | Opaque interior changes |
|---|---:|---|---:|
| Lyra young | 694 | Identical | 0 |
| Cassia young | 1,451 | Identical | 0 |
| Selene everyday | 1,168 | Identical | 0 |

Only green changed in those comparisons. Opaque interior means alpha at least
254, eroded by a 15×15-pixel square to exclude nearby silhouette edges. This
measurement supports preservation of internal colors; the independent face and
hair inspection provides the visual judgment.

`../development/visual-novel/archive/local/graphics-workspace/review/fringe-measurements.json` binds the old/current
shader hashes, selected source hashes, actual native render hashes, measurements
and full bright/dark captures. Current comparison images are in that same review
directory. The old shader remains recoverable through Git; the temporary native
comparison inputs under `/tmp/graphics-fringe-baseline` are diagnostic scratch.

Reproduce the current native frames with:

```sh
python3 scripts/project.py test --headless --suite character_framing_review
```

This was a Linux/Xvfb native render. It does not establish WebGL performance,
browser edge quality, People portrait cropping or every scene's physical support
plane. Those remain separate runtime checks.
