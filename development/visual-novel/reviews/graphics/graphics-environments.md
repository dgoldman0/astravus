# Production environment review and corrections

The author's review reopened the first three treehouse variants because their weather, light and furnishings barely changed. That earlier internal acceptance is superseded. The installed replacement now has four source-timed states: early daylight, early rainy afternoon, later daylight, and later remembrance in rain. Fixed construction stays coherent while the room's use and dressing evolve.

## Authority and chronology

[revision/latest.md](../../../../revision/latest.md), in the passage beginning “One of our favorite places to explore,” establishes an upper room among old-oak branches, a ladder, open windows with fabric curtains, a separate lower hollow entrance, drawings and imaginary maps, treasure chests, cushions and a small shared table. [Treehouse.png](../../../../revision/Treehouse.png) is the author's two-level refuge reference. Measured dimensions, compass bearings, precise furniture coordinates and camera positions are adaptation choices, not additional lore.

The source later says “As we grew older,” introduces the shared engineering work, and eventually brings Calista and Cassia back to the treehouse after Joren's death. They add drawings/messages and continue using the refuge; the later annual gathering is not evidence that the earlier grief scene occurs decades afterward. The new dressing shows ongoing use and rearrangement, without inventing abandonment or structural decay.

| State and story use | Visible state | Chronology constraint |
| --- | --- | --- |
| `treehouse-shaded.png`, early refuge in `script.rpy` | Green afternoon canopy, brighter indirect window/floor fill, original near table, familiar cushions and five generic early wall drawings. | No later waterwheel/remembrance paper appears before the project. |
| `treehouse-rain.png`, early rainy afternoons | Same early furnishings; neutral overcast air, mist, wet bark highlights and restrained varied rain outside; cooler/dimmer room fill with warm lamps. | Rain is outside the open bays and behind the rails; sheltered cushions, papers and table remain dry. |
| `book-one/treehouse-later.png`, chapter 24 dispute and chapter 28 grief | Daylight canopy, worktable moved toward the right window, two low stools, drawing board, map holder, rearranged indigo/rust textiles and different storage use. | Later childhood receives evolved furnishings before the death. Early generic wall drawings remain; memorial papers do not appear early. |
| `book-one/treehouse-memory.png`, chapter 31 remembrance | Later furnishings under rainy afternoon light, plus the existing later wall drawings/messages and remembered waterwheel. | No old-table paper overlay is applied after the table has moved. The new table already carries maps/drawing supplies. |

Only the load-bearing trunk, doors, window positions, rail/post system and connected access are fixed construction constraints. Tables, stools, storage, cushions, blankets, drawings, wear and light may change with story time. A room should remain recognizable without being frozen forever.

## Production method and reviewed outputs

[build_treehouse_states.py](../../../../visual-novel/scripts/build_treehouse_states.py) assembles immutable original room/paper sources, the bounded later furnishing layer, and [relight_treehouse_states.py](../../../../visual-novel/scripts/relight_treehouse_states.py)'s explicit lighting/weather states. It replaces the first near-identical variant producer as the current room-state workflow. [environment-edits.json](../../../../visual-novel/docs/environment-edits.json) records actual source bytes, scripts, operations, output hashes and independent changed-pixel counts. Later furnished outputs also reference [treehouse-furnishings.json](../../../../visual-novel/docs/treehouse-furnishings.json) and the generated-material register; retained material is limited to furniture and its vacated floor footprint.

The whole room receives color and midtone changes. Those receipts therefore do **not** claim unchanged interior pixels. Fixed architectural geometry is not resampled; furniture is explicitly allowed to move. Exterior grading follows hand-defined openings and controlled edge extensions. Rain uses separate fixed seeds, varied lengths and opacity; the moved furniture's alpha masks out any newly occluded window region. Weather never uses the old table position as an assumed permanent opening.

The initial new day grade was rejected for gray/sepia foliage; the first rain was rejected for bright uniform white strings. The reviewed revision restores restrained leaf/shadow green, reduces streak density and opacity, and pulls the weather boundary above the right cushions. Root and a separate reviewer inspected the four full frames and native window crops. They found distinct daylight/rain states, retained painterly depth, no new visible seam/support defect, and readable furniture progression. This is scoped art acceptance, not user approval or a substitute for runtime placement checks.

| Installed output | SHA256 |
| --- | --- |
| Early daylight | `ed727c67e4e6628eef1e2ba9820b70a1d98cd32b4d71e4c04100f4508e9d16d3` |
| Early rain | `9a21aab8edb8f0424464e4106cf5e8700b62d35de806ab90c38b1d14624ea456` |
| Later daylight | `25bfec7ea7a1366a0e62c51f044eee3d6c066efef2dfff16c619cb80eb5e718a` |
| Later memory rain | `6333e29fb28cdd941de01093e0acd8918d7c18dcf5f33898ff0f25efd5016543` |

One editable GIMP document, `build/graphics/environments/states/treehouse-states.xcf`, contains the original room, separate early drawings, later furniture, remembrance drawings, and four separate translucent color/weather correction layers. Only one lighting state should be visible; enable furniture and remembrance layers appropriate to that state. The XCF sets explicit legacy Normal blending, avoiding GIMP's different default blend space. All four selectable states were opened and flattened by installed GIMP: early day, early rain and later day matched the runtime pixels exactly; remembrance differed by at most one 8-bit channel unit on 98 pixels. Runtime PNGs come from the direct reproducible operator, not a screenshot. Recreate with `python3 scripts/build_treehouse_states.py --xcf`; add `--install` to replace the selected files in place. Old runtime versions belong in Git, not parallel installed copies.

## Related views and supports

| View | Scoped finding and treatment |
| --- | --- |
| `backgrounds/garden.png` | Retained governing exterior: massive trunk at right, upper room to its left, ladder/landing linking the upper entrance to the lower refuge, separate lower door, seating circle and left gate/path. It does not mistake the lower hollow door for the upper treehouse. |
| `theme-morning-outlook.png` | Retained environment. Calista is in the foreground; the same broad upper/lower arrangement and connected access remain behind her. Foreground character size does not measure the distant door. |
| `treehouse-friends.png` | Early seated group is supported by cushions/floor around the reachable near table. Accepted local near-fork details remain. Current CG already has warm backlit green daylight, so it is compatible with the early dry state and receives no unnecessary second grade. Character edits are recorded separately. |
| `theme-treehouse-arrival.png` | Early standing trio in the upper room; Joren's hand meets the near post and floor continues below the crop. Offscreen foot contact is not certified. Current accepted daytime foliage is retained after direct comparison with the new dry state. |
| `cassia-comfort.png` | Later seated grief scene. The first nearby-fork-only night treatment is superseded by matching later furnishings and afternoon window light. Figures, joined hands, outfits and their supporting seat stay outside the environmental edits. The new table/stools/floor and complete daylight bays received full/native independent review. The first partial bay grade was rejected for cyan islands and hard boundaries; explicit foliage contours now cover those gaps while preserving warm lamp/curtain edges. |
| `theme-sketch-laughter.png` | Scoped keep after full/native inspection: only a small strip of soft leaves/sky, curtain and open rail is visible. No identifiable exterior fork junction requires alignment. Papers, hands, maps and cup meet the table. |
| `theme-evening-reading.png` | Scoped keep after full/native inspection: seated Calista's book rests on her lap beside an open rail and lamp. Both ends and the distinguishing junction of the visible straight exterior branch lie outside the crop. Warm near bark and cool distant foliage fit the evening context. |
| `book-one/memory-mural-v2.png` | The pictured treehouse belongs to a painted memory mural; it is not a new physical architecture reference. |

The final comfort output is `e656c47c19a9c9ef5f273c041d149db9078e58d99dc63a755f759d2c0a9c825e`. Its recipe is `treehouse-comfort-later-daylight`; [relight_treehouse_comfort.py](../../../../visual-novel/scripts/relight_treehouse_comfort.py) rebuilds it from immutable CG paint plus retained near-branch and furniture layers. `build/graphics/environments/states/cassia-comfort.xcf` retains four editable layers. The faces/joined hands have zero changed pixels, and all other changes lie in the union of the three permitted environment layers. Installed GIMP opened and flattened its four layers; the export differed from the runtime image by at most one 8-bit channel unit on 426 pixels. Root then accepted a fresh live chapter-28 capture with the final daylight/furniture output. This does not substitute for unrelated runtime dimensions.

## Nearby exterior rig and its limits

[project_treehouse_exterior.py](../../../../visual-novel/scripts/project_treehouse_exterior.py) and [treehouse-exterior-rig.json](../../../../visual-novel/docs/treehouse-exterior-rig.json) retain two separate original painted fork clusters at production depths of 7.0 and 8.5 model units. They project through a simple camera into protected CG openings. Each CG keeps its richer original distant foliage. The three tracked RGBA materials in `art/production/*-near-exterior.png` contain those bounded nearby details; the daylight versions use restrained warm branches, a reduced leaf fringe, modest focus softening and matched broad illumination.

The depth coordinates support limited parallax; they do not reconstruct the whole building. A mistaken arrival guide once paired different rail locations, so its former 153-pixel residual was invalid evidence and was removed. No current claim of architectural truth rests on that residual. Visible opening/support relationships are inspected directly; unseen sides of the building are not certified.

Actual review rejected a smeared mirrored canopy, a generated distant plate that flattened the original foliage, and initial daytime layers with cyan rims and leaf-stencil artifacts. Those rejected materials were not shipped. Final nearby layers received full-frame and independent native inspection. The new day/weather states preserve the same nearby motifs while allowing actual environmental light to change.

## Matrix evidence and remaining runtime scope

- `setting_geometry`: visible fixed shell, separate upper/lower entrances and connected access inspected. Furniture is a stage-dependent state, not a permanent spatial invariant.
- `lighting_style_detail`: the exact four new background hashes above received full/native inspection after initial grades failed. Old three-variant art/time acceptance is superseded.
- `scene_truth_action`: early generic drawings, later work supplies, memory-only wall papers and afternoon rain now follow actual source/runtime chronology. Named character identity is reviewed separately.
- Empty backgrounds have no named-actor identity/anatomy/stature dimension; figures within a child's drawing are not newly present actors.
- `runtime_compositing`: moving the table requires checking Shadow's tabletop support, Barkley's stool clearance, later sprites and the CG/background transitions. Root owns those targeted runtime captures; its final 15-capture state suite was rerun after installation and includes the corrected comfort scene. Asset pixel verification alone cannot pass those placements.

For future changes, keep construction and camera anchors explicit, but let furnishings and weather evolve when the text does. Reuse existing strong paint where it fits. New camera sides require appropriate geometry/material rather than a stretched crop. Inspect native edges and whole-scene storytelling before renewing the exact file's review.
