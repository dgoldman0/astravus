# Location continuity — 0.1-alpha

The closing film introduced new views of familiar places without keeping a shared record of their physical layout. Matching wood, foliage and painterly style did not preserve the building. The location register now records **which place and camera each picture represents**, the landmarks that must remain, and the exact pixels that were visually checked.

[location-continuity.json](location-continuity.json) is the working register. It currently covers **29 images across seven locations**. [check_assets.py](../scripts/check_assets.py) checks it alongside the generation manifests. The register deliberately distinguishes **source facts** from **production landmarks**: a useful fixed arrangement for these illustrations does not become new architectural canon in the story.

## What establishes the treehouse

The [manuscript](../../revision/latest.md) describes an old oak in the far corner of Maia's garden, a raised room among sturdy branches, an old ladder, a wooden roof under the canopy, simple open windows with fabric curtains, cushions, drawings, treasure boxes and a small table. **The lower hollow has a second secret entrance.** A ground-level door is therefore supported; the error is letting that entrance replace, or become confused with, the upper room.

[Treehouse.png](../../revision/Treehouse.png) supplies the author's original two-level refuge. The selected [dry interior](../game/images/backgrounds/treehouse-shaded.png) governs the production room, and the [garden exterior](../game/images/backgrounds/garden.png) governs how that room and the lower refuge join. These are the authority already recorded in [ART_DIRECTION.md](ART_DIRECTION.md), not a new measured blueprint.

For the exterior garden camera, preserve the **massive trunk on the right**, the **broad upper room projecting to its left**, the **arched upper entrance at the trunk end**, and a **ladder connecting the lower refuge to the upper landing**. Below is a rounded platform with cushions, low tables, maps and chests, beside the separate hollow entrance. Planting beds border the platform; they do not occupy its floor.

For the familiar interior camera, preserve the **large diagonal trunk at left**, the **arched entrance behind it**, and the **open viewing bays, branch rails and rust curtains across the right**. The low round map table is near the right foreground. A close camera may crop a landmark; a weather change must not move it. Rain stays outside the sheltered room, without new glass panes.

No exact dimensions, load calculations or compass directions are established here. Human scale must nevertheless be credible: children must fit through the same door into the same shared room, the ladder must meet a real landing, and every standing or seated figure needs a plausible supporting surface.

## Specific review findings

The final selected compositions have been inspected against their source and production references. This closes their **location** findings only; the separate character, artistic-quality and runtime checks still govern release approval. Further pixel edits invalidate these location hashes.

| Finding | Image | Inspected repair |
| --- | --- | --- |
| TH-01 | [Theme arrival](../game/images/cg/book-one/theme-treehouse-arrival.png) | Restores a close welcoming trio within the broad upper room: large left trunk, single arched entrance behind the girls, open right bays and near map table. Joren rests a hand on a window-bay post. The camera is `upper_interior_close`; people are no longer shrunk to show the entire room. |
| TH-02 | [Morning outlook](../game/images/cg/book-one/theme-morning-outlook.png) | The massive oak, raised broad room, upper entry/ladder, separate lower hollow and sitting refuge remain behind Calista. Her large foreground portrait is nearer the camera on the garden route, preserving hopeful warm light without making her enormous beside a distant doorway. |
| TH-03 | [Friends on the path](../game/images/cg/book-one/theme-path-friends.png) | The earlier garden-only assignment was unsupported. This exploration shot depicts a distinct Lumen neighborhood walkway, consistent with Book I's interconnected paths. The close trio, timber walking surface, branch rails and planted edges preserve the stronger original composition. The distant dwellings are not identified as Maia's oak treehouse. |

These records do not introduce a different story event or turn production landmarks into a measured canonical blueprint.

| Other treehouse image | Review |
| --- | --- |
| [Garden exterior](../game/images/backgrounds/garden.png) | Governing view of both levels, connected ladder and lower seating refuge. |
| [Dry interior](../game/images/backgrounds/treehouse-shaded.png), [rainy interior](../game/images/backgrounds/treehouse-rain.png), [remembrance interior](../game/images/backgrounds/book-one/treehouse-memory.png) | Preserve the same camera, trunk, entrance, bays, railings, table and cushions. Weather and new drawings are the intended differences. |
| [Friends around the table](../game/images/cg/book-one/treehouse-friends.png) | Closer composition retains the left trunk, entrance behind and right viewing bays. The table's different screen position follows the camera framing. |
| [Cassia and Cali together](../game/images/cg/book-one/cassia-comfort.png) | Seated beside the trunk; the original entrance, bays and near table remain visible. |
| [Sketch and laughter](../game/images/cg/book-one/theme-sketch-laughter.png) | Tight crop of faces and the map table, with compatible timber and an open bay behind. This crop does not prove the off-screen floor plan. |
| [Evening sketchbook](../game/images/cg/book-one/theme-evening-reading.png) | Cali sits with the sketchbook on her lap beside cushions, a shelf and an open rail. It does not add a new writing desk or glazing. |
| [Garden mural](../game/images/backgrounds/book-one/memory-mural-v2.png) | The small treehouse/adventure imagery is visibly painted. It is a memory on the wall and is not a reference for the physical building. |

## Pond and plaza checks

The [pond](../game/images/backgrounds/book-one/garden-pond.png), [working bank](../game/images/backgrounds/book-one/garden-work-area.png), planting-compromise CG, rescue/recovery CGs and water-wheel views retain the shallow stone basin, timber boundary, plant groups and accessible dry bank. Rescue poses have support on the low bank; recovery and pot work happen on dry ground. The miniature wheel stays a children's project. Reusing one basin is a production choice: the manuscript mentions multiple ponds and does not say that every pond event occurs in one precisely identified basin.

The [festival](../game/images/backgrounds/book-one/festival.png), [memorial](../game/images/backgrounds/book-one/memorial-plaza.png) and [annual remembrance](../game/images/backgrounds/book-one/remembrance-plaza.png) now share the same large tree and curved staircase at left, rear central passage, surrounding arcaded terraces and center-right dais. Substantial gathered crowds occupy each occasion. Lighting, lanterns, instruments, flowers and messages change with the event; the square's plan does not.

Cassia's smaller [storytelling courtyard](../game/images/backgrounds/community-courtyard.png) is a separate venue. Its intimate circle and rounded arches must not be substituted for the community-wide central plaza.

## Working on a new or revised shot

1. **Assign the place and view before generating.** Select a `location_id` and a `view_id` from the register, then record the story scene or closing-theme cue that uses it. If a camera angle is new, explicitly describe its relation to the established landmarks instead of calling it merely “another treehouse view.”
2. **Use the canonical environment as the edit base.** Supply character references separately for faces, age, clothes and pose. A recently generated character scene does not automatically become the building reference for the next one.
3. **Include the required landmarks in the edit prompt.** Describe the door's destination, ladder landing, floor level, trunk side, railing and visible furniture. Allow a crop to hide features; do not silently shrink, mirror or rebuild them. For weather edits, hold the camera and structure fixed.
4. **Inspect the actual result against the canonical views.** Trace access from ground to ladder to landing to door to room. Check feet, knees and hands against the supporting surfaces; check that a doorway accommodates the depicted child. Review the actual in-game/video crop as well as the full image.
5. **Replace the selected asset and record its provenance.** Keep generated reference chains in the existing manifests. Author-approved local iris retouches require their explicit source hash, reproducible recipe and proof that outside pixels are unchanged. Git holds previous versions; do not add before/after asset copies to the game.
6. **Renew the visual review explicitly.** Only after inspecting the replacement, update `reviewed_sha256`, `reviewed_reference_signature`, `review_status` and the review notes. The reference signature records the canonical environment images used for the review; changing one invalidates its dependent reviews too. Resolve any finding with a concrete description of the repair. Do not copy new manifest hashes into the review register merely to make the checker pass.
7. **Run `python3 scripts/check_assets.py`.** The guard rejects changed pixels or canonical references with stale reviews, unresolved issues, missing source/reference files, source anchors that disappeared, changed theme cue assignments, and unregistered images matching the recurring-location patterns. Seven regression tests cover the current-review path and the stale/new/changed-reference failures. A newly named recurring view must also be registered even if its filename does not match those patterns.

The checker establishes that reviewed pixels and assignments have not silently changed. It cannot judge a new picture's geometry, infer its location from pixels, or prove continuity for architecture outside a crop. Those remain explicit visual-review responsibilities.
