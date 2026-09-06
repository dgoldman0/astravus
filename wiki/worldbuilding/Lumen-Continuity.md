# Lumen: Canon Decisions and Adaptation Compatibility

**World specification version 1, September 2026.** This is the change and compatibility record for [Lumen](Lumen.md), its [population](Lumen-Demographics.md), [atlas](Lumen-Atlas.md), [systems](Lumen-Systems.md), and [artificial gravity](Artificial-Gravity.md).

## Authority and scope

The wiki is the canonical home of world details. The existing [latest manuscript](../../revision/latest.md), aligned [timeline](../TIMELINE.md), and [visual novel](../../visual-novel/docs/ADAPTATION.md) supply the narrative constraints this specification was developed to preserve.

Use four distinct statuses:

| Status | Meaning |
| --- | --- |
| **Inherited** | Already established in the story, current wiki, or an explicitly identified author/production reference. Source facts and production facts remain distinguishable. |
| **New working canon** | A deliberate addition in this specification, now the default for further world development. Rounded figures are not newly discovered source measurements. |
| **Modelling target** | Coordinates, local dimensions, allocations or camera arrangements to test. Refine these to preserve inherited scenes and visual landmarks. |
| **Open** | Not settled here. Do not fill it by treating illustrative prose, a dream, or a generated background as an engineering fact. |

This version updates the wiki and adds author-facing [Blender scale studies](../../world/lumen/README.md). It makes **no edits to `revision/latest.md`, Ren'Py story text, existing VN image assets, or VN review manifests**. The new renders are modelling evidence, not approved replacement backgrounds. Existing production references and their review requirements continue to govern the VN.

The specification is written as a concrete starting version, with explicitly adjustable modelling targets. Subsequent choices belong here and in the relevant canonical page; they should not create competing numerical canons in a Blender file and the wiki.

## Decisions and wiki refinements

| ID | Decision | Status and reason | Downstream effect |
| --- | --- | --- | --- |
| D01 | Book I uses approximately 10,000 embodied residents, with a representative C+10 layout. | New working canon. Supports a substantial but shared community. | No dialogue change. Population is separate from fully transcended minds and familiars. |
| D02 | Lumen's founding is around C−100; growth continues across the story. | New working canon, approximate. Allows a locally born majority and mature transplanted vegetation. | No named character receives a new exact birthday or birthplace. |
| D03 | Reference main body is about 4.8 × 2.8 × 1.8 km, containing a terraced central city and adjoining chambers. | New working canon. Exterior and internal dimensions were previously unspecified. | Preserve local shots; test exact chamber shapes in blockout. |
| D04 | Ordinary habitation has dependable nominal 1 g and common down. | Author-directed premise; 1 g is the new working default. Replaces the old mandatory 0.1–0.4 g regime. | Existing walking, climbing, pets, rain and sport need no special low-g treatment. |
| D05 | The VSB explanation is a superseded speculative mechanism, not a constraint or demonstrated physical technology. | Wiki refinement implementing the gravity decision. | Remove obligatory low-g transit, emotional gravity instability and prescribed violent failure behavior. Do not tie Joren's accident to gravity. |
| D06 | Grown living structure coexists with manufactured tools, timber and construction. | Reconciles wiki shorthand with explicit manuscript action. | Preserve welding, screws, scaffolding and the patched treehouse. |
| D07 | Maintained daylight and weather coexist with evening bioluminescence. | New operating detail around inherited sunlight, sky, rain and plants. | Preserve existing light and weather variants. |
| D08 | Maia stewards a broad garden with a family-adjacent working area and accessible wooded margins. | New spatial interpretation preserving the wiki's placement of both trees in the garden. | Keep Echoes and the treehouse oak distinct; no relocation scene. |
| D09 | Central Plaza includes connected gathering terraces and courts. | New spatial interpretation of inherited community-wide occasions and VN architecture. | Keep the established square and stage camera; add capacity beyond the frame. |
| D10 | Radiant Fields belongs to the period after C+125. | Inherited from the aligned event and Book IV; corrects the overview's “Mid Story” placement. | No relocation of the scene. Earlier recreation is not automatically Luxa. |
| D11 | A constellation is an adult romantic/peer relationship, distinct from family and household. Only the adult partners are members. | Author clarification, already present in the VN glossary; corrects the wiki's conflicting definitions, child/familiar membership claims and the first specification draft's conflation. | Correct wiki definitions, bios, event summaries and indexes. Keep the VN's correct definition. Two narrow manuscript wording refinements are proposed below; family and partnership membership are counted separately. |
| D12 | Longevity supports centuries of life, with individually variable transcendence. | Replaces an unsupported wiki “average lifespan” range with the established qualitative rule. | Calista's post-125 transition and Theron's 400+ years both remain possible. |
| D13 | Lumen's overview quotes the current manuscript's final first-person wording. | Wiki quotation correction; the older appended attribution was not the current text. | No change to the manuscript's ending or its interpretation. |

## Manuscript and visual novel compatibility register

**Physical-layout changes requiring manuscript scene edits: none identified. Required Ren'Py storyline edits: none identified. Required existing image replacements: none identified.** The separate terminology record marks two proposed manuscript refinements; they do not change events. These conclusions now include initial route, scale and camera studies. They do not prove that every image can be matched by one completed mesh; the table distinguishes those first checks from remaining detailed work.

| ID | Existing constraint and source | How the specification accommodates it | Adjustment / verification status |
| --- | --- | --- | --- |
| C01 | [Manuscript opening](../../revision/latest.md#earliest-memories): young Lumen, locally born majority, five adult partners raising a wider family. | Modest founding settlement, broad first generation, varied households and separate adult-partnership membership. | No scene change. Manuscript terminology refinement E01 proposed. Detailed demographics remain illustrative. |
| C02 | [Family home](../../revision/latest.md#earliest-memories): central table, branching halls, individual rooms, workshop, music room and library. | Allocate a large domestic grouping with real private rooms and small professional spaces. | No edit required. Detailed floor plan must preserve sibling-room adjacency. |
| C03 | [Treehouse](../../revision/latest.md#early-friendships) and [location register](../../visual-novel/docs/location-continuity.json), `maia_treehouse`. | Oak, upper room, ladder/landing, separate lower hollow, open bays, patched timber and canopy remain. | **Initial scale/access study complete.** A 5 m upper-floor target fits both levels and human-scale openings; exterior/interior landmark arrangement is retained. Detailed camera reconstruction remains open. No source or image edit. |
| C04 | [Echoes discovery](../events/Tree-of-Echoes-Discovery.md): wooded approach, separate ancient transplanted tree. | A different clearing within Maia's larger garden landscape. | No edit required. A literal talking tree or new spiritual effect is not added. |
| C05 | Pond, rescue, planting and waterwheel; register `garden_pond`. | Low basin, dry working bank, supplied flow for the small wheel; other garden ponds remain possible. | **Initial bank/water scale study complete.** Detailed shoreline and pose fitting remain open. No edit identified; the existing pond review remains authoritative for production images. |
| C06 | [Festival](../../revision/latest.md#earliest-memories), memorial and annual remembrance; register `central_plaza`. | One square plus surrounding occupied terraces/courts, with later capacity added outside the established view. | **20,000 m² gathering reservations measured; initial composition tested.** Detailed crowd circulation and camera reconstruction remain open. No source/image edit identified. The smaller storytelling courtyard stays separate. |
| C07 | Maia's flowers feature in the festival. | Garden approaches and curated displays connect the broader garden to the civic event. | No edit required; the entire 17.6 ha garden is not squeezed into the square. |
| C08 | Rainy treehouse and later studio scenes; VN open-bay geometry. | Managed rain occurs outside shelter, beneath the broader enclosing body. | No edit required. No window glass added to the treehouse. Weather and lived-in dressing may change while architecture remains coherent. |
| C09 | Construction areas use machinery, welding and holographic blueprints. | Guided structural growth, conventional fabrication and enclosed fit-out zones coexist. | No edit required. Metalwork and manual controls remain. |
| C10 | [Dome adventure](../events/Dome-Climbing-Adventure.md); [VN ascent](../../visual-novel/game/friendships_book_one.rpy), `chapter_dome_ascent`. | Internal scaffold platform overlooking the shared basin, with breathable air and ordinary gravity. | **Initial mesh sightlines tested:** home roof, central square and part of the planted garden are visible from near the parapet. Recheck with detailed architecture/foliage. No source or background edit. |
| C11 | Joren dies during a routine expedition to a nearby moon. | Arrival and expedition facilities serve local craft; protective systems are not infallible. | No edit required; cause remains an unspecified malfunction. The dome outing stays a separate successful adventure. |
| C12 | Calista and Aris create their own home; Kael, Sage and Sol have a separate household. | Reserve distinct nearby sites with later occupancy. | No scene change; E02 clarifies household language. Do not reuse the childhood home as the literal address of every household. |
| C13 | Natural-looking light, sunflowers, a solar-powered model car, evening bioluminescence. | Maintained directional daylight powers photosensitive plants/devices; dimmer biological light serves evenings. | No terminology edit required. “Sunlight” remains ordinary resident language. |
| C14 | Observation deck looks into space; Lyra sends a return message. | Protected exterior viewing aperture, arrival routes and communications. | No edit required. No instantaneous interstellar travel/communication inferred. |
| C15 | [Radiant Fields](../events/Radiant-Fields-Luxa.md) after 125, including arena and practice field. | Later growth chambers beyond the original construction edge; ordinary-gravity Luxa. | No source/VN edit required. **New later-book art needed when those books are adapted**, not replacement of Book I art. |
| C16 | [Gradual revelation](../../visual-novel/docs/ADAPTATION.md#revelation-and-chronology): early Lumen feels like a world before being identified as a ship. | Canopies, local ceilings and intimate framing obscure the whole vessel in early scenes. | No edit required. **A future full-world opening shot would need adjustment** if it spoiled the reveal; this atlas is author-facing. |
| C17 | Dream beach, Nyx library, painted memories and children's imagined maps. | Their representation remains memory, dream, art or play as specified in each scene. | No edit required. Do not add an ocean aboard Lumen from these alone. |

## Proposed manuscript terminology refinements

The separate [constellation alignment record](../CONSTELLATION_ALIGNMENT.md#manuscript-wording-proposals) owns E01 and E02, the two proposed manuscript terminology refinements. They remain unapplied and do not arise from physical layout. The VN glossary already uses the correct adult romantic/peer definition.

## Blockout adjustment record

The terminology corrections were committed separately as `b92817f`. The following are changes to the physical model's initial targets, not narrative or image revisions.

| ID | Constraint / initial conflict | Adjustment and evidence | Status / canon impact |
| --- | --- | --- | --- |
| B01 | Treehouse exterior has a substantial raised room and lower refuge with human-sized access; the initial 7 m floor target made the ladder unnecessarily tall relative to those openings. | Use a 5 m local upper floor, connected landing, 1.1 m doorway and a real passage through the trunk. Compare the [exterior](../../world/lumen/renders/treehouse.png) and [interior](../../world/lumen/renders/treehouse_interior.png) studies to the registered references. | **Resolved without source change.** Adjustable local measurement refined; neither entrance nor level removed. Fine camera fitting remains open. |
| B02 | From the rear of the dome platform, the parapet blocked the downward ray toward the neighborhood. | Move the camera 9 m toward the front, within the same platform. Rays then reach the childhood home roof and square; 11/25 sampled garden patches are visible through sparse canopy proxies. See [dome study](../../world/lumen/renders/dome.png). | **Resolved without source change.** Platform and neighborhood coordinates retained. Camera placement is a production target, not new dialogue canon. |
| B03 | A camera attempting to show the broad square made the established performance area feel too distant. | Frame the tree, passage and closer center-right stage within the broad complex. Reserve most capacity behind and beside this view; verify 20,000 m² of net gathering rectangles. See [performance](../../world/lumen/renders/plaza.png) and [capacity plan](../../world/lumen/renders/plaza_plan.png). | **Resolved without source change.** Preserves the familiar composition while accommodating community-wide occasions. Detailed circulation still open. |
| B04 | The pond requires a reachable edge and shallow water alongside enough dry space for the rescue and planting scenes. | Test a 0.35 m water depth, waterline 0.12 m below the working bank and low 0.06 m coping. Keep the left inlet and right lily group. See [pond study](../../world/lumen/renders/pond.png). | **Initial scale study complete; no edit identified.** These are adjustable dimensions, not a replacement for the existing pairwise shoreline and pose review. |

The [measurement report](../../world/lumen/validation.json) records the tested wiki-data hash. Body and net-area packing checks do not establish structural strength, food yield, pressure safety or a completed room inventory. The model's simplified building masses and vegetation make the sightline results provisional for later detailing.

## Existing visual references

The original [Lumen panorama](../../visuals/lumen-life.png) supports layered inhabited terraces, organic enclosure and warm light among teal foliage. It is a draft visual reference, not a measured exterior or a Book I opening shot. The selected [dome view](../../visual-novel/game/images/backgrounds/book-one/dome.png) supports an internal overlook. The [festival view](../../visual-novel/game/images/backgrounds/book-one/festival.png) supplies the familiar plaza composition.

The machine-readable [VN register](../../visual-novel/docs/location-continuity.json) includes later author guidance allowing furnishings and dressing to change across time. Preserve architectural access and landmarks without freezing every cushion and map through decades. Do not infer absent geometry from cropped-out areas.

This wiki specification does not alter hashes, approve images, or replace the VN's existing [location review](../../visual-novel/docs/LOCATION_CONTINUITY.md). A future asset edit still needs an actual visual review and renewed provenance.

## If a conflict appears during modelling

First try a different camera, a compatible off-screen continuation, or a change to a modelling target. Do not use a camera explanation to disguise physically disconnected floors, doors or water surfaces. If an inherited reference still cannot fit, add a row here before revising it:

`ID | exact source passage / asset / scene | physical conflict | alternatives attempted | smallest proposed edit | canon impact | status`

Use **proposed**, **implemented**, or **resolved without source change** for an actual adjustment. Record source changes and visual replacements separately. A new illustration of an unpictured dock is additional coverage; replacing the treehouse door or rewriting the dome climb is an adjustment.

## Remaining work

- Subdivision of the measured neighborhood into actual homes, rooms and public spaces; detailed reconstruction of the selected treehouse, pond, plaza and dome views.
- A complete circulation graph, including level changes and goods/care access.
- Diet, cultivated yields, energy/fuel budget, heat rejection, water inventory and reserves.
- Structural spans, pressure boundaries, shielding thickness and overall mass.
- Vehicle design, propulsion performance and actual route durations beyond Lumen.
- Sanctuary biology, population of familiars, founding collective consciousness and the biological endpoint of transcendence.

These open physical items do not currently require changing either narrative's events. Keep the two terminology proposals above separate from spatial compatibility. Resolve further details through the wiki and test the resulting model before presenting engineering closure or exact reconstruction as established.
