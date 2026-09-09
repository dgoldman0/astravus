# Barkley matte follow-up

`matrix_release` and root, 2026-09-05. The final dispute frame showed a few
small green flecks in Barkley's tail edge. Native source inspection found
contaminated pixels roughly 9–14 source pixels from confidently green backing,
beyond the shared shader's tighter neighborhood. A supplemental shader applies
only to Barkley, after the existing green key. It probes nearby backing and
adjusts only green-dominant source pixels; ordinary gold fur has red greater
than green and bypasses this pass. The human shader and all source paintings
remain unchanged.

The independent root reviewer and implementation reviewer inspected the actual
native `test-results/barkley-edge/dispute-support.png` and `people-barkley.png`,
including paired unscaled Barkley crops. Green tail flecks diminish; coat, face,
paws, strands and the portrait's full outline remain readable. Only 36 pixels
of the 1738×977 dispute capture changed from the prior final state, all within
Barkley's edge. Pixels outside that edge were identical. This is a modest,
accepted improvement; a fine painted gold rim remains and is not advertised as
a perfect matte. The additional key can change contaminated edge opacity, so
this does **not** claim identical alpha as the earlier human color-only pass did.

The dedicated `barkley_edge_review` native testcase passed four assertions,
capturing the dark-floor placement and actual People portrait without running
the whole story again. `../development/visual-novel/archive/local/graphics-workspace/barkley-edge.log` records the run.
[graphics-runtime-reconciliation.json](graphics-runtime-reconciliation.json)
binds current source/runtime hashes, both captures and the inspected prior view.
The result is Linux/Xvfb native evidence; WebGL quality/performance and other
platforms remain separate checks.
