# Rejected local 3D attempt

**Rejected by the author on 6 September 2026. The geometry, architecture and dimensions in this directory are not a foundation for Lumen’s design.**

The build was stopped after the author identified its departure from the visual novel. Its files remain here as development evidence. The wiki, manuscript and VN have not been changed to accommodate it. The earlier source inventory remains useful; this model’s interpretation of those sources does not follow from that inventory.

## Direct comparison with the VN

| Scene | Primary visual reference | Rejected render |
|---|---|---|
| Pond | [VN garden pond](../../../visual-novel/game/images/backgrounds/book-one/garden-pond.png) | [Pond render](renders/pond.png) |
| Shared room | [VN family home](../../../visual-novel/game/images/backgrounds/family-home.png) | [Home render](renders/home.png) |
| Garden and oak | [VN garden](../../../visual-novel/game/images/backgrounds/garden.png) | [Garden render](renders/garden.png) |
| Upper refuge | [VN treehouse interior](../../../visual-novel/game/images/backgrounds/treehouse-shaded.png) | [Treehouse render](renders/treehouse.png) |

The pond’s broad, irregular paving meets the water at a low stone edge. The drop is on the water side. The model instead exposes a continuous outer wall around a regular oval, creating a raised basin. Its 6.4 × 5 m footprint and constant section were assigned without establishing their compatibility with the visual references. Sparse planting and an opaque surface also remove the shallow, enclosed character of the source. The [rescue](../../../visual-novel/game/images/cg/book-one/pond-rescue.png) supplies additional evidence for the relationship between the bank, water and children.

The shared room has curved timber framing overhead, deep openings, built-in furniture and a planted passage receding beside the fountain. The model uses a rectangular shell, applied arches and isolated furniture. Its exposed staircase changes the passage seen in the VN. The arrangement of boxes in the overview does not establish the continuous inhabited architecture.

The oak is a massive branching body that shapes and supports the refuges. The lower sitting area curves around its base. The upper room contains a substantial diagonal trunk and opens through broad timber bays. The model substitutes a ring of narrow trunk segments, a rectangular raised room and a stage with separate benches. The blank foreground wall further obscures the lower refuge. These errors remain even if the camera is moved.

The working rooms also require individual reconstruction. The [workshop](../../../visual-novel/game/images/backgrounds/book-one/workshop.png) has a compact arrangement of bench, drawers, side work surfaces, a tall left window and a right doorway. The [music room](../../../visual-novel/game/images/backgrounds/book-one/music-room.png) frames its piano, harp and sitting area within a curved enclosure. The [library](../../../visual-novel/game/images/backgrounds/book-one/library.png) has wraparound shelving, two left windows and a deep passage beyond the map table. [Sage’s room](../../../visual-novel/game/images/backgrounds/book-one/sage-room.png) has a broad round sleeping alcove behind the story circle. Giving each of these spaces the same rectangular room generator discards the architecture that distinguishes them.

## Why the checks did not catch this

The automated checks test sampled clearance, floor support and a few sightlines in the meshes supplied to them. They cannot establish that those meshes represent the VN’s architecture. The room schedule records assigned dimensions; it does not validate those dimensions. Camera landmark comparisons cover isolated feature positions and cannot validate silhouettes, sections, enclosure or relative scale.

The next reconstruction must establish those visible forms in an individual scene before extending connections around it. Begin with the pond’s shoreline, paving and water section; compare the whole rendered view with the source, including the rescue view. Keep uncertain scale explicit. Reconstruct the home and both oak views with the same discipline before fitting them into a connected local model. Additional rooms and paths must work around those reconstructed spaces.

The scripts, Blender file and interactive viewer in this directory retain the rejected experiment. Camera-fit proposals are unadopted. No source alteration is justified by this model’s failure.
