# Lumen: Book I spaces and connections

**Source inventory · 6 September 2026 · no new floor plan or dimensions adopted**

This is the spatial program recovered from a complete read of Book I in [latest.md](../../revision/latest.md), the full current VN narrative, and inspection of its location images. The [Lumen article](Lumen.md) remains the canon overview. The inventory records existing requirements and explicit uncertainties; it does not make every illustration detail canon.

The recent `household-spaces.svg` and `neighborhood.svg` studies omitted essential parts of the home and its surroundings. **They are withdrawn as layout bases.** Adding “more rooms beyond view” did not account for the missing workshops, music room, library, adult retreats and lower treehouse spaces. Their broad privacy intentions can be reconsidered after the complete program is placed.

## What the household actually needs

The home supports shared life, independent interests, privacy and practical work. Its program includes the central gathering room and fountain; branching internal halls; Cali’s, Kael’s and Lyra’s distinctive private rooms; private provision for all five adults; cooking and serving; drawing, painting and unfinished projects; Arin’s workshop; Selene’s music room; Dorian’s library; Sage’s room; ordinary household outdoor space and garden work; and supporting washing/storage needs. **These are functions and spaces, not a count of separate bedrooms or detached buildings.** Sage’s illustrated room, for example, combines a sleeping alcove with a cushioned gathering area. The other adults’ private arrangements must be accounted for without assuming how they sleep or which work rooms double as personal retreats.

The text places the children’s private rooms within the home and gives their relative adjacency. Selene’s room is reached along a hall, and the fountain is audible beyond Sage’s door. Arin’s workshop and Dorian’s library belong in the family’s daily spatial program, even while their precise attachment and entrances remain unresolved. Soren’s workshop is another place, associated with Joren’s home. The construction machinery room is another again. A single generic “workshop” cannot satisfy all three.

Maia’s garden is ordinary semi-private household space. Its planting bed has an explicit sightline to the oak ladder. The treehouse’s upper room, ladder/landing, lower hollow with a second entrance, and furnished lower refuge all matter. The author’s broader shared woods and open plains must meet this close garden relationship intelligently. Shared surroundings do not erase the household garden or the children’s intimate refuge. The Tree of Echoes is a separate destination reached through thicket into a clearing.

## Scope and authority

Read end to end: `script.rpy`, `family_book_one.rpy`, `friendships_book_one.rpy`, and the Book I portion of `revision/latest.md` (lines 1–514 at this audit). Cross-checked the 32-scene registry, People/glossary text, image definitions, closing-theme image assignments, existing Book I coverage map and location continuity records. All 49 registered location/state/action/closing-theme images below were visually inspected for spatial content. Character sprite libraries, marketing assets, audio and full runtime playback are outside this spatial audit.

The full prose read here is **Book I**, not Books II–IV. Their later homes, art center, cafe, integration events, observation spaces and Radiant Fields need an extension of this register before a whole-life or whole-vessel layout is called complete. Existing wiki facilities appear in a separately labeled group below; their presence in a general wiki article does not date each room to Cali’s childhood. In particular, the Sanctuary article calls its more detailed room list “likely.”

Current author direction controls the design; current VN images are the primary visual guides; manuscript and VN actions constrain what must fit. The wiki holds established canon and the open design record. Older outside illustrations, provisional diagrams and invented story-within-story worlds cannot fill gaps as if they were measured evidence. Proposed numeric area allowances must be reconsidered against the full program, rather than used to squeeze it down to the previous sketch.

## Using this record

The versioned [space-inventory.json](lumen-study/space-inventory.json) contains the curated records, evidence anchors, scene mappings, image observations and source fingerprints. This page is generated from it by [space_inventory.py](lumen-study/space_inventory.py). Query from the repository root:

```sh
python3 wiki/worldbuilding/lumen-study/space_inventory.py --group Household
python3 wiki/worldbuilding/lumen-study/space_inventory.py workshop
python3 wiki/worldbuilding/lumen-study/space_inventory.py --id sage_room
python3 wiki/worldbuilding/lumen-study/space_inventory.py --scene family_rhythm
python3 wiki/worldbuilding/lumen-study/space_inventory.py --unplaced
python3 wiki/worldbuilding/lumen-study/space_inventory.py --check
```

Queries return matching records, exact source passages with current line locations, relevant images and connections. This is local keyword/identifier retrieval, not semantic search. For an unfamiliar concept, search the original prose, scripts and wiki as well; a missing match in this register is not evidence that a detail does not exist. No network, model, API key or vector service is required.

The checker detects changed source text/pixels, missing evidence anchors, missing scene coverage, and new or reassigned background/CG/theme images. It checks only the Book I slice of `latest.md`; later-book changes are outside this inventory’s audit scope. A passing check proves traceability and identifier coverage, **not** that every implication was understood or that a drawing fits the story. Inspect sources and images before manually renewing their fingerprints; `--write` only regenerates this page and never renews evidence automatically.

Before the next layout, each required space must be placed, explicitly allowed for outside the modeled slice, or deliberately combined with another compatible use. Record the reason and keep unresolved attachments visible. Compare source actions and cameras after those connections exist. Reserve supporting service/root/structure volumes, but do not turn inference into new canon. Any required story or asset change receives its own entry in the [design adjustment register](Lumen-Design-Study.md#compatibility-and-adjustment-register).

## Remaining design work

The next physical study should work from this whole household-and-neighborhood program: determine plausible connections and overlaps; retain the garden/ladder sightline and both treehouse levels; connect local shared places without cutting through private space; and test child-height VN views. Then revisit population, usable surfaces, the community gathering constraint and the larger distributed living body. Current anatomy and numerical probes remain proposals. No room dimensions, new professional rooms, private-property boundaries or revised story scenes are approved by this inventory.

## Current author decisions

- Artificial gravity is accepted; keep familiar story actions and visual design. Mechanism remains open.
- Lumen is young and inhabited through a substantial living body, not one flat city under a dome.
- Compare roughly 6,000 and 18,000 embodied childhood residents, with about 18,000 as the childhood upper limit; exact census and later growth remain open.
- Maia’s garden is an ordinary household garden, with semi-private household outdoor life.
- Broader woods/forest and open plains around the treehouse area are more shared; distinguish personal, household, nearby-household and wider-community use.
- A constellation is an adult romantic/peer relationship, not a family, household or housing unit.
- Existing VN visuals dominate older outside art. Preserve the VN and latest.md with minimal refinements, and mark any required adjustments.

## Complete scene coverage

All 32 scenes have records below. Listed spaces include on-screen settings, narrated destinations, remembered places and requirements introduced by the scene; inclusion is not a claim that the cast visits every listed place during it. Images at different times/weather can represent the same location. The source link opens the corresponding scene entry.

| # | Scene | Spaces and requirements |
|---|---|---|
| 1 | [First memory](../../visual-novel/game/script.rpy#L18) (`first_memory`) | [Sanctuary and First Breath welcome](#sanctuary); [Cali's childhood home](#home); [Shared central room](#central_room); [Internal halls and thresholds](#home_halls); [Private provision for Maia, Arin, Selene, Dorian and Sage](#adult_retreats); [Cali's private room](#cali_room); [Kael's private room](#kael_room); [Lyra's private room](#lyra_room); [Arin's workshop](#arin_workshop); [Selene's music room](#selene_music); [Maia's household garden](#maia_garden); [Community halls, paths and planted walkways](#community_routes) |
| 2 | [A small beginning](../../visual-novel/game/script.rpy#L58) (`garden`) | [Maia's household garden](#maia_garden); [Sunflower bed and daily garden learning](#planting_patch); [Washing, clothing, storage and household servicing](#domestic_support); [Oak ladder, landing and upper entrance](#treehouse_access); [Oak lower hollow and second entrance](#treehouse_hollow) |
| 3 | [Room for both](../../visual-novel/game/family_book_one.rpy#L24) (`plant_disagreement`) | [Maia's household garden](#maia_garden); [Dry pond bank and plant-arranging area](#pond_bank); [Garden ponds and the shallow rescue basin](#garden_ponds) |
| 4 | [The scattered pieces](../../visual-novel/game/family_book_one.rpy#L71) (`workshop_first`) | [Arin's workshop](#arin_workshop) |
| 5 | [A color you can hear](../../visual-novel/game/family_book_one.rpy#L120) (`music_first`) | [Internal halls and thresholds](#home_halls); [Selene's music room](#selene_music) |
| 6 | [Routes through a story](../../visual-novel/game/family_book_one.rpy#L188) (`dorian_stories`) | [Dorian's library and reading area](#dorian_library); [Stories, dreams, maps and painted worlds](#imagined_places) |
| 7 | [Three ways forward](../../visual-novel/game/family_book_one.rpy#L228) (`sage_story`) | [Sage's room](#sage_room); [Shared central room](#central_room); [Stories, dreams, maps and painted worlds](#imagined_places) |
| 8 | [The days between](../../visual-novel/game/family_book_one.rpy#L286) (`family_rhythm`) | [Cali's childhood home](#home); [Shared central room](#central_room); [Internal halls and thresholds](#home_halls); [Cali's private room](#cali_room); [Kael's private room](#kael_room); [Lyra's private room](#lyra_room); [Private provision for Maia, Arin, Selene, Dorian and Sage](#adult_retreats); [Cooking, preparation and serving space](#kitchen); [Maia's household garden](#maia_garden); [Sunflower bed and daily garden learning](#planting_patch); [Arin's workshop](#arin_workshop); [Selene's music room](#selene_music); [Dorian's library and reading area](#dorian_library); [Sage's room](#sage_room); [Stories, dreams, maps and painted worlds](#imagined_places) |
| 9 | [The Tree of Echoes](../../visual-novel/game/family_book_one.rpy#L385) (`tree_echoes`) | [Community halls, paths and planted walkways](#community_routes); [Tree of Echoes approach and clearing](#echoes_grove) |
| 10 | [The shallow water](../../visual-novel/game/family_book_one.rpy#L438) (`pond_scare`) | [Garden ponds and the shallow rescue basin](#garden_ponds); [Dry pond bank and plant-arranging area](#pond_bank); [Community halls, paths and planted walkways](#community_routes); [Cali's childhood home](#home); [Washing, clothing, storage and household servicing](#domestic_support) |
| 11 | [A little too much](../../visual-novel/game/family_book_one.rpy#L477) (`soup_experiment`) | [Cooking, preparation and serving space](#kitchen); [Shared central room](#central_room); [Maia's household garden](#maia_garden) |
| 12 | [Wishes in the light](../../visual-novel/game/family_book_one.rpy#L516) (`festival_lights`) | [Central Plaza, approaches and occupied galleries](#central_plaza); [Plaza stage and floral/display space](#plaza_stage); [Maia's household garden](#maia_garden) |
| 13 | [An invitation](../../visual-novel/game/script.rpy#L101) (`meeting_cassia`) | [Community storytelling courtyard](#courtyard); [Community halls, paths and planted walkways](#community_routes); [Stories, dreams, maps and painted worlds](#imagined_places) |
| 14 | [Room for another story](../../visual-novel/game/friendships_book_one.rpy#L9) (`cassia_home`) | [Cassia's home](#cassia_home); [Cultivation, circulation and maintenance systems](#living_systems) |
| 15 | [Something worth finding](../../visual-novel/game/script.rpy#L140) (`meeting_joren`) | [Outer construction zones and passages](#construction_paths) |
| 16 | [Things we could make](../../visual-novel/game/friendships_book_one.rpy#L61) (`joren_home`) | [Joren's home](#joren_home); [Soren's systems workshop](#soren_workshop) |
| 17 | [Beyond the familiar paths](../../visual-novel/game/friendships_book_one.rpy#L88) (`kaleb_walk`) | [Kaleb’s guided exploration route](#kaleb_walk); [Community halls, paths and planted walkways](#community_routes); [Outer construction zones and passages](#construction_paths); [Joren's home](#joren_home); [Soren's systems workshop](#soren_workshop); [Cali's childhood home](#home); [Shared central room](#central_room); [Household drawing and painting provision](#home_painting) |
| 18 | [Our place in the branches](../../visual-novel/game/script.rpy#L176) (`treehouse`) | [Maia's household garden](#maia_garden); [Oak ladder, landing and upper entrance](#treehouse_access); [Oak treehouse: upper room](#treehouse_upper); [Oak lower hollow and second entrance](#treehouse_hollow); [Furnished refuge beneath the oak](#treehouse_lower_sitting); [Shared woodland, open ground and nearby households](#local_landscape); [Stories, dreams, maps and painted worlds](#imagined_places) |
| 19 | [A story under the rain](../../visual-novel/game/script.rpy#L226) (`rain_refuge`) | [Oak treehouse: upper room](#treehouse_upper); [Stories, dreams, maps and painted worlds](#imagined_places) |
| 20 | [Something that turns](../../visual-novel/game/friendships_book_one.rpy#L111) (`waterwheel`) | [Arin's workshop](#arin_workshop); [Miniature waterwheel test site](#waterwheel_site); [Garden ponds and the shallow rescue basin](#garden_ponds); [Dry pond bank and plant-arranging area](#pond_bank) |
| 21 | [The unfinished world](../../visual-novel/game/friendships_book_one.rpy#L157) (`outer_exploration`) | [Arin's workshop](#arin_workshop); [Outer construction zones and passages](#construction_paths); [Construction tools and machinery room](#construction_room); [Shared central room](#central_room) |
| 22 | [A place beside us](../../visual-novel/game/friendships_book_one.rpy#L195) (`lyra_included`) | [Maia's household garden](#maia_garden); [Oak ladder, landing and upper entrance](#treehouse_access); [Community halls, paths and planted walkways](#community_routes) |
| 23 | [The view from above](../../visual-novel/game/friendships_book_one.rpy#L220) (`dome_ascent`) | [Outer construction zones and passages](#construction_paths); [Unfinished dome: scaffold climb and overlook](#dome_platform); [Cali's childhood home](#home); [Community halls, paths and planted walkways](#community_routes) |
| 24 | [Which way we go](../../visual-novel/game/friendships_book_one.rpy#L250) (`treehouse_dispute`) | [Oak treehouse: upper room](#treehouse_upper) |
| 25 | [The news](../../visual-novel/game/friendships_book_one.rpy#L293) (`loss`) | [Shared central room](#central_room); [Cali's childhood home](#home); [Nearby moon research expedition](#moon_expedition); [Oak treehouse: upper room](#treehouse_upper) |
| 26 | [What comfort can do](../../visual-novel/game/friendships_book_one.rpy#L317) (`family_grief`) | [Shared central room](#central_room) |
| 27 | [What the hand remembers](../../visual-novel/game/friendships_book_one.rpy#L340) (`painting_grief`) | [Shared central room](#central_room); [Household drawing and painting provision](#home_painting); [Washing, clothing, storage and household servicing](#domestic_support); [Stories, dreams, maps and painted worlds](#imagined_places) |
| 28 | [Between the two of us](../../visual-novel/game/friendships_book_one.rpy#L363) (`cassia_grief`) | [Oak treehouse: upper room](#treehouse_upper); [Unfinished dome: scaffold climb and overlook](#dome_platform) |
| 29 | [The names we carry](../../visual-novel/game/friendships_book_one.rpy#L394) (`community_memorial`) | [Central Plaza, approaches and occupied galleries](#central_plaza); [Plaza stage and floral/display space](#plaza_stage); [Soren's systems workshop](#soren_workshop); [Cultivation, circulation and maintenance systems](#living_systems) |
| 30 | [A place to remember](../../visual-novel/game/friendships_book_one.rpy#L415) (`mural_remembrance`) | [Maia's household garden](#maia_garden); [Garden mural and remembrance place](#garden_mural); [Stories, dreams, maps and painted worlds](#imagined_places) |
| 31 | [The rain returns](../../visual-novel/game/friendships_book_one.rpy#L432) (`treehouse_remembrance`) | [Oak treehouse: upper room](#treehouse_upper); [Garden mural and remembrance place](#garden_mural); [Unfinished dome: scaffold climb and overlook](#dome_platform) |
| 32 | [What remains](../../visual-novel/game/friendships_book_one.rpy#L449) (`annual_remembrance`) | [Central Plaza, approaches and occupied galleries](#central_plaza); [Plaza stage and floral/display space](#plaza_stage); [Oak treehouse: upper room](#treehouse_upper); [Garden mural and remembrance place](#garden_mural) |

## Spaces and functions

45 records, including provisions, groups of spaces, remote destinations and fictional settings. This is not a room count. All physical records currently remain **unplaced** in a complete reconstructed layout.

### Household

<a id="home"></a>
#### Cali's childhood home

`home` · Basis: **story** · Model: **unplaced**

A connected home for five parents and three children during the later household scenes, with three familiars. Shared life includes making, music, reading, cooking, care, play and private retreat. The central-room background shows only part of it.

**Use and privacy:** Household and invited guests.

**Location and connection status:** Within Lumen; Maia’s garden folds around it. Internal halls branch to other parts of the home.

**Still to resolve:** Complete extent, levels and room sizes. Do not infer a detached building, a wealthy estate, or eight separate houses from the number of residents.

**Evidence:** [revision/latest.md:21](../../revision/latest.md#L21); [revision/latest.md:69](../../revision/latest.md#L69); [visual-novel/game/script.rpy:52](../../visual-novel/game/script.rpy#L52).

**Scene links:** `first_memory`, `family_rhythm`, `pond_scare`, `kaleb_walk`, `dome_ascent`, `loss`.

<a id="central_room"></a>
#### Shared central room

`central_room` · Basis: **story** · Model: **unplaced**

Round wooden meal/project table; chairs and sofas; reading and conversation areas; books, drawings and unfinished work; ceiling light panels; small indoor fountain; familiar resting places. Meals, knowledge quests, maps, grief and painting share this room over time.

**Use and privacy:** Household; friends visit.

**Location and connection status:** Inside the home, connected to branching halls. The VN shows a garden threshold and a separate corridor opening.

**Still to resolve:** Allow activities and circulation around furnishings; the round table is not the entire room. Overall dimensions and destinations of every arch remain unmeasured.

**Evidence:** [revision/latest.md:61](../../revision/latest.md#L61); [revision/latest.md:65](../../revision/latest.md#L65); [visual-novel/game/script.rpy:171](../../visual-novel/game/script.rpy#L171).

**Scene links:** `first_memory`, `sage_story`, `family_rhythm`, `soup_experiment`, `kaleb_walk`, `outer_exploration`, `loss`, `family_grief`, `painting_grief`.

**VN images:** [family-home.png](../../visual-novel/game/images/backgrounds/family-home.png); [family-home-painting.png](../../visual-novel/game/images/backgrounds/book-one/family-home-painting.png); [home-dusk.png](../../visual-novel/game/images/backgrounds/book-one/home-dusk.png); [family-embrace.png](../../visual-novel/game/images/cg/book-one/family-embrace.png).

<a id="home_halls"></a>
#### Internal halls and thresholds

`home_halls` · Basis: **story** · Model: **unplaced**

Branching hallways with bioluminescent planting and touch-responsive living murals connect the home. Music is heard through doors; the children and familiars move between rooms.

**Use and privacy:** Household circulation.

**Location and connection status:** Branch from the central room; Selene’s door is reached along a hall.

**Still to resolve:** Exact branches, level changes, door positions and acoustics. Keep household circulation distinct from public through-routes.

**Evidence:** [revision/latest.md:69](../../revision/latest.md#L69); [revision/latest.md:69](../../revision/latest.md#L69); [visual-novel/game/family_book_one.rpy:125](../../visual-novel/game/family_book_one.rpy#L125).

**Scene links:** `first_memory`, `music_first`, `family_rhythm`.

**VN images:** [family-home.png](../../visual-novel/game/images/backgrounds/family-home.png).

<a id="cali_room"></a>
#### Cali's private room

`cali_room` · Basis: **story** · Model: **unplaced**

Bed in an alcove, pillows and quilt; drawings, creations, book/trinket shelves; a desk beside a window for sketching and reading; space for Shadow. Morning light changes on the walls.

**Use and privacy:** Personal.

**Location and connection status:** Within the home, between Kael’s room and Lyra’s room in the prose’s adjacency description.

**Still to resolve:** Shape, orientation and window outlook. No dedicated VN bedroom background; the closing-theme sketchbook shot is in the treehouse and must not replace this room.

**Evidence:** [revision/latest.md:73](../../revision/latest.md#L73); [revision/latest.md:73](../../revision/latest.md#L73); [revision/latest.md:205](../../revision/latest.md#L205).

**Scene links:** `first_memory`, `family_rhythm`.

<a id="kael_room"></a>
#### Kael's private room

`kael_room` · Basis: **story** · Model: **unplaced**

Maps, exploratory models, loft bed and a blanket fort underneath; reading/planning and Barkley’s company.

**Use and privacy:** Personal.

**Location and connection status:** Next to Cali’s room within the home.

**Still to resolve:** Dimensions and access; the loft is furniture-scale vertical use, not evidence for a whole additional residential deck.

**Evidence:** [revision/latest.md:77](../../revision/latest.md#L77); [revision/latest.md:77](../../revision/latest.md#L77).

**Scene links:** `first_memory`, `family_rhythm`.

<a id="lyra_room"></a>
#### Lyra's private room

`lyra_room` · Basis: **story** · Model: **unplaced**

Bed, shelves, educational games, drawings, projects and collections of stones, feathers and pressed flowers; room for Nibble’s company.

**Use and privacy:** Personal.

**Location and connection status:** On the other side of Cali’s room from Kael’s.

**Still to resolve:** Dimensions, storage arrangement and window/door placement.

**Evidence:** [revision/latest.md:81](../../revision/latest.md#L81).

**Scene links:** `first_memory`, `family_rhythm`.

<a id="adult_retreats"></a>
#### Private provision for Maia, Arin, Selene, Dorian and Sage

`adult_retreats` · Basis: **story** · Model: **unplaced**

The prose says each person has a private space. Carry all five adults in the residential program as well as the children. Sage has an explicitly described room; the other adults’ retreat arrangements are not individually described.

**Use and privacy:** Personal; sharing by invitation.

**Location and connection status:** Within the home. Possible overlap with named work/quiet rooms remains open; Sage’s VN room visibly includes a sleeping alcove.

**Still to resolve:** Which work rooms also serve as private retreats, and which adults have separate sleeping/retreat areas. This is not a claim of five additional bedrooms on top of all work rooms. A romantic constellation does not determine sleeping arrangements.

**Evidence:** [revision/latest.md:73](../../revision/latest.md#L73); [revision/latest.md:149](../../revision/latest.md#L149); [visual-novel/game/script.rpy:32](../../visual-novel/game/script.rpy#L32).

**Scene links:** `first_memory`, `family_rhythm`.

**VN images:** [sage-room.png](../../visual-novel/game/images/backgrounds/book-one/sage-room.png).

<a id="kitchen"></a>
#### Cooking, preparation and serving space

`kitchen` · Basis: **story** · Model: **unplaced**

Fresh bread, prepared breakfasts and collaborative dinners; Lyra and Maia make a second pot of soup while the family waits. Needs working surfaces, ingredients, utensils, cooking and washing access, with space to work together.

**Use and privacy:** Household.

**Location and connection status:** Part of household life and connected to the central meal table. The scenes reuse the central-room background.

**Still to resolve:** Separate kitchen versus connected cooking area; equipment, pantry and exact route to garden. Do not treat meals as delivered automatically or claim the background proves the kitchen is at the table.

**Evidence:** [revision/latest.md:207](../../revision/latest.md#L207); [revision/latest.md:303](../../revision/latest.md#L303); [visual-novel/game/family_book_one.rpy:501](../../visual-novel/game/family_book_one.rpy#L501).

**Scene links:** `family_rhythm`, `soup_experiment`.

<a id="home_painting"></a>
#### Household drawing and painting provision

`home_painting` · Basis: **story** · Model: **unplaced**

Cali sketches at her bedroom desk and the shared table; the friends spread maps there. Later she paints through grief, washes a brush and leaves work for the next morning. Storage and unfinished-work space matter.

**Use and privacy:** Personal and household activity.

**Location and connection status:** Distributed within the home; the VN explicitly stages grief painting in the central room’s painting state.

**Still to resolve:** Where wet work dries and materials are kept. No dedicated childhood painting studio is established; do not import the later adult home’s painting room.

**Evidence:** [revision/latest.md:73](../../revision/latest.md#L73); [visual-novel/game/script.rpy:171](../../visual-novel/game/script.rpy#L171); [visual-novel/game/friendships_book_one.rpy:360](../../visual-novel/game/friendships_book_one.rpy#L360).

**Scene links:** `kaleb_walk`, `painting_grief`.

**VN images:** [family-home-painting.png](../../visual-novel/game/images/backgrounds/book-one/family-home-painting.png).

<a id="arin_workshop"></a>
#### Arin's workshop

`arin_workshop` · Basis: **story** · Model: **unplaced**

A recurring, equipped working room: benches, floor working space, tools, screws/parts storage, stool, gadgets and ongoing projects. Supports the spilled-screws scene, irrigation prototype and collaborative waterwheel fabrication with wood shaping and fitting.

**Use and privacy:** Arin, household learners and invited friends; wider access unspecified.

**Location and connection status:** Closely associated with home life; the VN opening hears its hum and the daily montage returns here. Its doorway opens to further planted interior space in the art.

**Still to resolve:** Exact attachment to the dwelling and work/service access. Do not replace it with Soren’s workshop, the construction equipment room or a generic community workroom. Preserve both personal experimentation and useful engineering.

**Evidence:** [revision/latest.md:111](../../revision/latest.md#L111); [revision/latest.md:231](../../revision/latest.md#L231); [visual-novel/game/family_book_one.rpy:80](../../visual-novel/game/family_book_one.rpy#L80); [visual-novel/game/friendships_book_one.rpy:117](../../visual-novel/game/friendships_book_one.rpy#L117).

**Scene links:** `first_memory`, `workshop_first`, `family_rhythm`, `waterwheel`, `outer_exploration`.

**VN images:** [workshop.png](../../visual-novel/game/images/backgrounds/book-one/workshop.png); [workshop-waterwheel.png](../../visual-novel/game/images/backgrounds/book-one/workshop-waterwheel.png).

<a id="selene_music"></a>
#### Selene's music room

`selene_music` · Basis: **story** · Model: **unplaced**

A real music/teaching room, with piano and shared seat, harp, flute and provision for the other instruments named in prose, including drums. Space for listeners, practice and familiars. The art shows a piano, harp, seating and a doorway.

**Use and privacy:** Selene, household and invited learners.

**Location and connection status:** Within the home’s soundscape; the VN explicitly approaches Selene’s door along a hall.

**Still to resolve:** Acoustic/privacy control and room dimensions; possible relationship to Selene’s personal retreat. Sound must still reach the home in the existing scenes.

**Evidence:** [revision/latest.md:237](../../revision/latest.md#L237); [revision/latest.md:237](../../revision/latest.md#L237); [visual-novel/game/family_book_one.rpy:125](../../visual-novel/game/family_book_one.rpy#L125).

**Scene links:** `first_memory`, `music_first`, `family_rhythm`.

**VN images:** [music-room.png](../../visual-novel/game/images/backgrounds/book-one/music-room.png); [flute-playing.png](../../visual-novel/game/images/cg/book-one/flute-playing.png); [flute-rest.png](../../visual-novel/game/images/cg/book-one/flute-rest.png).

<a id="dorian_library"></a>
#### Dorian's library and reading area

`dorian_library` · Basis: **story** · Model: **unplaced**

Books and scrolls, a reading/storytelling area, lamps, maps that siblings spread out and trace, table, shelves and window seat/outlook. The VN gives it its own large furnished room and visible corridor connection.

**Use and privacy:** Dorian and household readers; further access unspecified.

**Location and connection status:** A recurring destination in the family routine. Its exact connection to the home’s central room is not mapped.

**Still to resolve:** Exact attachment, archive extent and use by outside listeners. Do not reduce it to the central room’s bookshelf or identify it as the whole community archive.

**Evidence:** [revision/latest.md:137](../../revision/latest.md#L137); [revision/latest.md:139](../../revision/latest.md#L139); [revision/latest.md:241](../../revision/latest.md#L241); [visual-novel/game/family_book_one.rpy:193](../../visual-novel/game/family_book_one.rpy#L193).

**Scene links:** `dorian_stories`, `family_rhythm`.

**VN images:** [library.png](../../visual-novel/game/images/backgrounds/book-one/library.png).

<a id="sage_room"></a>
#### Sage's room

`sage_room` · Basis: **story** · Model: **unplaced**

Soft cushions, blankets and candlelight; room for Sage with the three siblings, storytelling, comfort and minor care. The VN art includes a sleeping alcove, low table and broad cushioned gathering area.

**Use and privacy:** Personal room welcoming the children; care and quiet company.

**Location and connection status:** In the home; the fountain can be heard beyond Sage’s door.

**Still to resolve:** Precise adjacency and degree of acoustic/visual privacy. This household room does not establish that professional transition counseling always happens here.

**Evidence:** [revision/latest.md:149](../../revision/latest.md#L149); [revision/latest.md:153](../../revision/latest.md#L153); [visual-novel/game/family_book_one.rpy:271](../../visual-novel/game/family_book_one.rpy#L271).

**Scene links:** `sage_story`, `family_rhythm`.

**VN images:** [sage-room.png](../../visual-novel/game/images/backgrounds/book-one/sage-room.png).

<a id="domestic_support"></a>
#### Washing, clothing, storage and household servicing

`domestic_support` · Basis: **inference** · Model: **unplaced**

Hands are washed after planting; a brush is washed after painting; wet clothing follows the pond incident. Tools, food, bedding, art, collections and familiar supplies must be stored. These actions require provision even where rooms are not described.

**Use and privacy:** Household; service access as needed.

**Location and connection status:** Support for the household and its outdoor/work areas; not yet assigned to rooms.

**Still to resolve:** Bathrooms, bathing, laundry, drying, pantry, cleaning and maintenance arrangements. These are design provisions to resolve, not a newly canonical list of conventional utility rooms.

**Evidence:** [visual-novel/game/script.rpy:89](../../visual-novel/game/script.rpy#L89); [visual-novel/game/friendships_book_one.rpy:360](../../visual-novel/game/friendships_book_one.rpy#L360); [visual-novel/game/family_book_one.rpy:459](../../visual-novel/game/family_book_one.rpy#L459).

**Scene links:** `garden`, `pond_scare`, `painting_grief`.

### Gardens and refuges

<a id="maia_garden"></a>
#### Maia's household garden

`maia_garden` · Basis: **story-and-author** · Model: **unplaced**

Garden around the home with flowers, fruit, herbs/spice, insects, soil, pots, paths, living lights and ponds. A place to cultivate, learn, linger and remember. The author explicitly says this is an ordinary household garden, not a sign of unusual wealth.

**Use and privacy:** Ordinary household outdoor space; semi-private.

**Location and connection status:** Around the home; paths continue beyond its wall. Its wooded edge meets the more shared treehouse surroundings.

**Still to resolve:** Exact boundary and area, relationship among ponds and routes, and how it meets local shared land. The broader forest is not all private garden; the garden is not all public park.

**Evidence:** [revision/latest.md:85](../../revision/latest.md#L85); [visual-novel/game/script.rpy:52](../../visual-novel/game/script.rpy#L52); [visual-novel/game/script.rpy:52](../../visual-novel/game/script.rpy#L52).

**Scene links:** `first_memory`, `garden`, `plant_disagreement`, `family_rhythm`, `soup_experiment`, `festival_lights`, `treehouse`, `lyra_included`, `mural_remembrance`.

**VN images:** [garden-close.png](../../visual-novel/game/images/backgrounds/garden-close.png); [garden.png](../../visual-novel/game/images/backgrounds/garden.png); [garden-wonders.png](../../visual-novel/game/images/backgrounds/book-one/garden-wonders.png); [theme-nibble-moment.png](../../visual-novel/game/images/cg/book-one/theme-nibble-moment.png); [theme-morning-outlook.png](../../visual-novel/game/images/cg/book-one/theme-morning-outlook.png).

<a id="planting_patch"></a>
#### Sunflower bed and daily garden learning

`planting_patch` · Basis: **story** · Model: **unplaced**

Planting patch beside a path; soil, marker stone, watering can, pots and seedlings; enough dry standing/kneeling space for Maia and Cali. The wider garden supports harvesting and insect observation too.

**Use and privacy:** Household and invited learners.

**Location and connection status:** Within Maia’s garden. Cali can see the oak ladder from this patch.

**Still to resolve:** Precise bed and ladder position; preserve the explicit sightline while reconciling close and wide garden views.

**Evidence:** [visual-novel/game/script.rpy:65](../../visual-novel/game/script.rpy#L65); [visual-novel/game/script.rpy:96](../../visual-novel/game/script.rpy#L96); [revision/latest.md:217](../../revision/latest.md#L217).

**Scene links:** `garden`, `family_rhythm`.

**VN images:** [garden-close.png](../../visual-novel/game/images/backgrounds/garden-close.png); [garden-wonders.png](../../visual-novel/game/images/backgrounds/book-one/garden-wonders.png); [theme-garden-opening.png](../../visual-novel/game/images/cg/book-one/theme-garden-opening.png); [theme-insect-discovery.png](../../visual-novel/game/images/cg/book-one/theme-insect-discovery.png).

<a id="pond_bank"></a>
#### Dry pond bank and plant-arranging area

`pond_bank` · Basis: **story** · Model: **unplaced**

A place to carry and arrange pots, compare sunlight and pond reflections, kneel to help Lyra and sit with her afterward. Work occupies broad supported dry ground, with reachable water and a path back home.

**Use and privacy:** Garden users.

**Location and connection status:** Beside the pond; the arrangement can be viewed from across the water.

**Still to resolve:** Shared-basin camera geometry remains a later reconstruction task. Do not mistake the garden work area for another enclosed workshop.

**Evidence:** [visual-novel/game/family_book_one.rpy:63](../../visual-novel/game/family_book_one.rpy#L63); [visual-novel/game/family_book_one.rpy:472](../../visual-novel/game/family_book_one.rpy#L472).

**Scene links:** `plant_disagreement`, `pond_scare`, `waterwheel`.

**VN images:** [garden-pond.png](../../visual-novel/game/images/backgrounds/book-one/garden-pond.png); [garden-work-area.png](../../visual-novel/game/images/backgrounds/book-one/garden-work-area.png); [waterwheel.png](../../visual-novel/game/images/backgrounds/book-one/waterwheel.png); [garden-compromise.png](../../visual-novel/game/images/cg/book-one/garden-compromise.png); [pond-rescue.png](../../visual-novel/game/images/cg/book-one/pond-rescue.png); [pond-comfort.png](../../visual-novel/game/images/cg/book-one/pond-comfort.png); [theme-waterwheel-team.png](../../visual-novel/game/images/cg/book-one/theme-waterwheel-team.png).

<a id="garden_ponds"></a>
#### Garden ponds and the shallow rescue basin

`garden_ponds` · Basis: **story** · Model: **unplaced**

Prose mentions multiple garden ponds. Lyra falls into a small shallow pond; the waterwheel later goes into one of the garden’s ponds. The VN uses one recognizable low stone basin across planting, rescue and wheel shots as a production choice.

**Use and privacy:** Garden users; exact access follows each basin.

**Location and connection status:** Garden landscape; a basin by planting beds in the VN. Number, identity and spacing of prose ponds remain open.

**Still to resolve:** Do not deduce exactly one pond or assign a huge lake. Retain shallow water, reachable low banks, dry recovery space and sensible water circulation.

**Evidence:** [revision/latest.md:289](../../revision/latest.md#L289); [revision/latest.md:417](../../revision/latest.md#L417); [visual-novel/docs/LOCATION_CONTINUITY.md:43](../../visual-novel/docs/LOCATION_CONTINUITY.md#L43).

**Scene links:** `plant_disagreement`, `pond_scare`, `waterwheel`.

**VN images:** [garden-close.png](../../visual-novel/game/images/backgrounds/garden-close.png); [garden-pond.png](../../visual-novel/game/images/backgrounds/book-one/garden-pond.png); [garden-work-area.png](../../visual-novel/game/images/backgrounds/book-one/garden-work-area.png); [waterwheel.png](../../visual-novel/game/images/backgrounds/book-one/waterwheel.png); [pond-rescue.png](../../visual-novel/game/images/cg/book-one/pond-rescue.png); [pond-comfort.png](../../visual-novel/game/images/cg/book-one/pond-comfort.png).

<a id="waterwheel_site"></a>
#### Miniature waterwheel test site

`waterwheel_site` · Basis: **story** · Model: **unplaced**

A portable wooden wheel, supports and paddles made with Arin, then carried to water and watched by friends, Lyra and familiars. Allows installation, adjustment and watching from the bank.

**Use and privacy:** Household and friends.

**Location and connection status:** At a garden pond, reached from Arin’s workshop.

**Still to resolve:** Carrying route and local flow arrangement. This is a small project, not a mill house or Lumen’s principal power plant.

**Evidence:** [revision/latest.md:417](../../revision/latest.md#L417); [visual-novel/game/friendships_book_one.rpy:143](../../visual-novel/game/friendships_book_one.rpy#L143).

**Scene links:** `waterwheel`.

**VN images:** [waterwheel.png](../../visual-novel/game/images/backgrounds/book-one/waterwheel.png); [theme-waterwheel-team.png](../../visual-novel/game/images/cg/book-one/theme-waterwheel-team.png).

<a id="garden_mural"></a>
#### Garden mural and remembrance place

`garden_mural` · Basis: **story** · Model: **unplaced**

A real wall in Maia’s garden, painted gradually by Cali with Cassia’s company. A place to stop and remember amid water, leaves and passing people. Art tools, seating and working space are shown in the VN.

**Use and privacy:** Semi-private garden with visitors and passersby.

**Location and connection status:** In Maia’s garden; the selected image shows planted ground and water nearby.

**Still to resolve:** Exact wall and approach. Painted places and people are part of the artwork; use the surrounding garden and working area as evidence for this physical setting.

**Evidence:** [revision/latest.md:503](../../revision/latest.md#L503); [visual-novel/game/friendships_book_one.rpy:427](../../visual-novel/game/friendships_book_one.rpy#L427).

**Scene links:** `mural_remembrance`, `treehouse_remembrance`, `annual_remembrance`.

**VN images:** [memory-mural-v2.png](../../visual-novel/game/images/backgrounds/book-one/memory-mural-v2.png).

<a id="treehouse_upper"></a>
#### Oak treehouse: upper room

`treehouse_upper` · Basis: **story** · Model: **unplaced**

Broad room built high in an old oak, patched timber and a wooden roof under canopy, open viewing cutouts with fabric curtains, drawings/maps, table, cushions, blankets and treasure chests. Room for friends to plan, argue, sit together and grieve. Furniture and drawings change across years.

**Use and privacy:** Children’s shared refuge; invitation and intimacy matter.

**Location and connection status:** At the far corner/wooded edge of Maia’s garden; overlooks garden flowers and glowing paths. Separate from the Tree of Echoes.

**Still to resolve:** Height, dimensions and complete camera reconciliation. The more shared surrounding woods do not make this intimate refuge a public traffic route.

**Evidence:** [revision/latest.md:385](../../revision/latest.md#L385); [revision/latest.md:391](../../revision/latest.md#L391); [revision/latest.md:393](../../revision/latest.md#L393); [visual-novel/game/friendships_book_one.rpy:446](../../visual-novel/game/friendships_book_one.rpy#L446).

**Scene links:** `treehouse`, `rain_refuge`, `treehouse_dispute`, `loss`, `cassia_grief`, `treehouse_remembrance`, `annual_remembrance`.

**VN images:** [garden.png](../../visual-novel/game/images/backgrounds/garden.png); [treehouse-shaded.png](../../visual-novel/game/images/backgrounds/treehouse-shaded.png); [treehouse-rain.png](../../visual-novel/game/images/backgrounds/treehouse-rain.png); [treehouse-later.png](../../visual-novel/game/images/backgrounds/book-one/treehouse-later.png); [treehouse-memory.png](../../visual-novel/game/images/backgrounds/book-one/treehouse-memory.png); [cassia-comfort.png](../../visual-novel/game/images/cg/book-one/cassia-comfort.png); [treehouse-friends.png](../../visual-novel/game/images/cg/book-one/treehouse-friends.png); [theme-treehouse-arrival.png](../../visual-novel/game/images/cg/book-one/theme-treehouse-arrival.png); [theme-sketch-laughter.png](../../visual-novel/game/images/cg/book-one/theme-sketch-laughter.png); [theme-evening-reading.png](../../visual-novel/game/images/cg/book-one/theme-evening-reading.png); [theme-morning-outlook.png](../../visual-novel/game/images/cg/book-one/theme-morning-outlook.png).

<a id="treehouse_access"></a>
#### Oak ladder, landing and upper entrance

`treehouse_access` · Basis: **story** · Model: **unplaced**

Ladder reaches a real landing at the upper entrance; Joren helps Cassia on the last rung and Cali reaches for her book. Children duck under branches and enter the same room.

**Use and privacy:** Access to shared refuge.

**Location and connection status:** Connects the lower garden/refuge level to the upper room. Visible from the sunflower patch.

**Still to resolve:** Height, slope and landing geometry; do not substitute the lower hollow’s door for this upper entrance.

**Evidence:** [revision/latest.md:391](../../revision/latest.md#L391); [visual-novel/game/script.rpy:182](../../visual-novel/game/script.rpy#L182); [visual-novel/game/script.rpy:96](../../visual-novel/game/script.rpy#L96).

**Scene links:** `garden`, `treehouse`, `lyra_included`.

**VN images:** [garden.png](../../visual-novel/game/images/backgrounds/garden.png); [theme-morning-outlook.png](../../visual-novel/game/images/cg/book-one/theme-morning-outlook.png).

<a id="treehouse_hollow"></a>
#### Oak lower hollow and second entrance

`treehouse_hollow` · Basis: **story** · Model: **unplaced**

A separate lower hollow with a second secret entrance and stored treasures/supplies. Cali plays here before she first climbs to the upper room.

**Use and privacy:** Children’s refuge.

**Location and connection status:** Underneath the upper treehouse; reached at the lower level.

**Still to resolve:** Internal extent and relation to the furnished platform. Do not omit the lower usable space when representing the treehouse.

**Evidence:** [revision/latest.md:395](../../revision/latest.md#L395); [visual-novel/game/script.rpy:96](../../visual-novel/game/script.rpy#L96).

**Scene links:** `garden`, `treehouse`.

**VN images:** [garden.png](../../visual-novel/game/images/backgrounds/garden.png).

<a id="treehouse_lower_sitting"></a>
#### Furnished refuge beneath the oak

`treehouse_lower_sitting` · Basis: **story-and-vn** · Model: **unplaced**

Lower seating and planning areas with cushions, tables, maps, supplies and chests among natural and bioluminescent plants. The VN garden exterior shows a broad rounded timber platform beside the hollow entrance.

**Use and privacy:** Shared by the children and companions.

**Location and connection status:** Below the upper room, adjoining the lower hollow and ladder.

**Still to resolve:** Exact platform extent and number of tables/seats. Neither bare ground nor planting beds can replace the occupied lower refuge.

**Evidence:** [revision/latest.md:395](../../revision/latest.md#L395); [revision/latest.md:397](../../revision/latest.md#L397).

**Scene links:** `treehouse`.

**VN images:** [garden.png](../../visual-novel/game/images/backgrounds/garden.png); [theme-morning-outlook.png](../../visual-novel/game/images/cg/book-one/theme-morning-outlook.png).

<a id="local_landscape"></a>
#### Shared woodland, open ground and nearby households

`local_landscape` · Basis: **author** · Model: **unplaced**

The author calls for broader woods/forest and open plains around the treehouse area, shared more widely than the household garden. Local households need shared places as well as their own inside/outside spaces.

**Use and privacy:** Shared among nearby households, with intimate places within it.

**Location and connection status:** Connects with the wooded garden/treehouse edge and local paths; repeats through inhabited Lumen rather than becoming one flat park.

**Still to resolve:** Extents of woods versus open land, thresholds and connection to other habitats. Keep the garden–ladder sightline; do not move the treehouse far away just to draw a privacy boundary.

**Evidence:** [revision/latest.md:57](../../revision/latest.md#L57); [visual-novel/game/script.rpy:96](../../visual-novel/game/script.rpy#L96).

**Scene links:** `treehouse`.

<a id="echoes_grove"></a>
#### Tree of Echoes approach and clearing

`echoes_grove` · Basis: **story** · Model: **unplaced**

An unfamiliar path through dense thicket/underbrush leads to a clearing containing the ancient transplanted Tree of Echoes, with gnarled branches and hollow trunk. Room to stand close and listen to its creaking.

**Use and privacy:** Community landscape reachable by children.

**Location and connection status:** In Lumen’s broader garden/path landscape; a separate tree from the treehouse oak.

**Still to resolve:** Travel distance and relation to the local woodland. Its age is inherited through transplantation, not the age of young Lumen.

**Evidence:** [revision/latest.md:267](../../revision/latest.md#L267); [revision/latest.md:271](../../revision/latest.md#L271); [visual-novel/game/family_book_one.rpy:403](../../visual-novel/game/family_book_one.rpy#L403).

**Scene links:** `tree_echoes`.

**VN images:** [echoes.png](../../visual-novel/game/images/backgrounds/book-one/echoes.png).

### Community and other homes

<a id="community_routes"></a>
#### Community halls, paths and planted walkways

`community_routes` · Basis: **story-and-vn** · Model: **unplaced**

Varied interconnected paths, halls, turnings and passages with planting, living light, arches, railings and inhabited destinations. Children walk, run, map turns, return home and visit other households. The closing theme also shows a distinct timber neighborhood walkway.

**Use and privacy:** Local and wider shared circulation.

**Location and connection status:** Connects homes, gardens, courts, groves, work and construction at several inhabited heights.

**Still to resolve:** Distances, travel times and full route network. The closing-theme walkway is not Maia’s specific garden path; distant dwellings are not extra treehouses at her oak.

**Evidence:** [revision/latest.md:57](../../revision/latest.md#L57); [revision/latest.md:343](../../revision/latest.md#L343); [visual-novel/game/friendships_book_one.rpy:101](../../visual-novel/game/friendships_book_one.rpy#L101); [visual-novel/docs/location-continuity.json:418](../../visual-novel/docs/location-continuity.json#L418).

**Scene links:** `first_memory`, `tree_echoes`, `pond_scare`, `meeting_cassia`, `kaleb_walk`, `lyra_included`, `dome_ascent`.

**VN images:** [construction-path.png](../../visual-novel/game/images/backgrounds/construction-path.png); [theme-path-friends.png](../../visual-novel/game/images/cg/book-one/theme-path-friends.png).

<a id="courtyard"></a>
#### Community storytelling courtyard

`courtyard` · Basis: **vn** · Model: **unplaced**

Intimate seated storytelling, blankets, sketchbooks and adult gatherings under planted rounded arches. Cassia and Cali meet here and return at subsequent gatherings.

**Use and privacy:** Local shared gathering.

**Location and connection status:** Farther from the household garden; distinct from the larger Central Plaza in the production location register.

**Still to resolve:** Exact route, local households served and capacity. Do not merge this into the community-wide plaza.

**Evidence:** [visual-novel/game/script.rpy:106](../../visual-novel/game/script.rpy#L106); [visual-novel/docs/location-continuity.json:318](../../visual-novel/docs/location-continuity.json#L318).

**Scene links:** `meeting_cassia`.

**VN images:** [community-courtyard.png](../../visual-novel/game/images/backgrounds/community-courtyard.png); [cassia-storytelling.png](../../visual-novel/game/images/cg/book-one/cassia-storytelling.png).

<a id="cassia_home"></a>
#### Cassia's home

`cassia_home` · Basis: **story** · Model: **unplaced**

A distinct home of books, art supplies and handmade crafts; tea and drawings share a table, paper dries above it, Lyron explains the living systems, and Dorian visits. The art shows seating, a planted interior water feature and another room beyond a doorway.

**Use and privacy:** Household and invited visitors.

**Location and connection status:** Reachable by household visits; no exact adjacency to Cali’s home.

**Still to resolve:** Complete domestic program and personal rooms remain undescribed. Thalia’s mediation profession and Lyron’s agricultural work do not locate their workplaces inside this room.

**Evidence:** [revision/latest.md:361](../../revision/latest.md#L361); [visual-novel/game/friendships_book_one.rpy:14](../../visual-novel/game/friendships_book_one.rpy#L14); [visual-novel/game/friendships_book_one.rpy:56](../../visual-novel/game/friendships_book_one.rpy#L56).

**Scene links:** `cassia_home`.

**VN images:** [cassia-home.png](../../visual-novel/game/images/backgrounds/book-one/cassia-home.png).

<a id="joren_home"></a>
#### Joren's home

`joren_home` · Basis: **story** · Model: **unplaced**

A separate domestic home filled with gadgets, maps and prototypes; exploration and invention shape its life. The VN family visit is staged in Soren’s workshop, so that background does not show the entire home.

**Use and privacy:** Household and invited visitors.

**Location and connection status:** Associated with Soren’s workshop; extent and attachment not precisely stated.

**Still to resolve:** Sleeping, cooking, retreat and family spaces must be allowed for when this home is developed. Do not equate its whole domestic program with the workshop.

**Evidence:** [revision/latest.md:381](../../revision/latest.md#L381); [visual-novel/game/friendships_book_one.rpy:104](../../visual-novel/game/friendships_book_one.rpy#L104).

**Scene links:** `joren_home`, `kaleb_walk`.

<a id="central_plaza"></a>
#### Central Plaza, approaches and occupied galleries

`central_plaza` · Basis: **story-and-vn** · Model: **unplaced**

The same major gathering place hosts the Festival of Lights, community mourning and annual remembrance. Gardens/displays, people, circulation, a large tree, curved stair and occupied arcaded terraces surround the square in the VN.

**Use and privacy:** Wider community.

**Location and connection status:** Connected to other routes through arches, stairs and a rear passage beneath a bridge. It is a civic focus, not proof that all city life occupies one central ship compartment.

**Still to resolve:** Whole-community gathering capacity at 6,000 versus 18,000, usable surrounding surfaces and approaches. No offscreen capacity is established merely because galleries appear.

**Evidence:** [revision/latest.md:323](../../revision/latest.md#L323); [revision/latest.md:499](../../revision/latest.md#L499); [revision/latest.md:511](../../revision/latest.md#L511).

**Scene links:** `festival_lights`, `community_memorial`, `annual_remembrance`.

**VN images:** [festival.png](../../visual-novel/game/images/backgrounds/book-one/festival.png); [memorial-plaza.png](../../visual-novel/game/images/backgrounds/book-one/memorial-plaza.png); [remembrance-plaza.png](../../visual-novel/game/images/backgrounds/book-one/remembrance-plaza.png).

<a id="plaza_stage"></a>
#### Plaza stage and floral/display space

`plaza_stage` · Basis: **story-and-vn** · Model: **unplaced**

Selene performs harp on a small stage; Maia’s floral work is displayed beside it in the VN. Lanterns rise into the artificial sky. Later flowers/messages and drawings accompany remembrance at the same dais.

**Use and privacy:** Performers and community audiences.

**Location and connection status:** Within the Central Plaza; stage center-right in the selected wide camera.

**Still to resolve:** Prepare/setup access, storage and precise floral area. The prose phrase “Maia’s garden was a centerpiece” is ambiguous; the VN already stages a floral centerpiece prepared by her and does not relocate the home garden.

**Evidence:** [revision/latest.md:329](../../revision/latest.md#L329); [revision/latest.md:329](../../revision/latest.md#L329); [visual-novel/game/family_book_one.rpy:523](../../visual-novel/game/family_book_one.rpy#L523); [visual-novel/game/family_book_one.rpy:538](../../visual-novel/game/family_book_one.rpy#L538).

**Scene links:** `festival_lights`, `community_memorial`, `annual_remembrance`.

**VN images:** [festival.png](../../visual-novel/game/images/backgrounds/book-one/festival.png); [memorial-plaza.png](../../visual-novel/game/images/backgrounds/book-one/memorial-plaza.png); [remembrance-plaza.png](../../visual-novel/game/images/backgrounds/book-one/remembrance-plaza.png).

### Work and exploration

<a id="soren_workshop"></a>
#### Soren's systems workshop

`soren_workshop` · Basis: **story** · Model: **unplaced**

A distinct workshop full of blueprints, tools and half-finished inventions; bench, assemblies, parts trays and drafting space for Cali’s rover idea. The VN shows a large drafting bench, tool drawers, floor prototype and an arched passage.

**Use and privacy:** Soren, Joren and invited collaborators/learners.

**Location and connection status:** Associated with Joren’s family home; exact attachment is unspecified.

**Still to resolve:** Work/service access, noise and equipment needs. Keep this separate from Arin’s personal workshop and the construction equipment room.

**Evidence:** [revision/latest.md:369](../../revision/latest.md#L369); [visual-novel/game/friendships_book_one.rpy:66](../../visual-novel/game/friendships_book_one.rpy#L66); [visual-novel/game/friendships_book_one.rpy:80](../../visual-novel/game/friendships_book_one.rpy#L80).

**Scene links:** `joren_home`, `kaleb_walk`, `community_memorial`.

**VN images:** [soren-workshop.png](../../visual-novel/game/images/backgrounds/book-one/soren-workshop.png).

<a id="kaleb_walk"></a>
#### Kaleb’s guided exploration route

`kaleb_walk` · Basis: **story** · Model: **unplaced**

Maze-like, unfamiliar passages and a hidden area; the children choose turnings and record an arch to recognize their way back. The VN uses the construction-path background.

**Use and privacy:** Guided local outing.

**Location and connection status:** Within Lumen, reached on a walk with Kaleb. May share some construction routes, but the text does not equate every outing.

**Still to resolve:** Destination, route and distance; distinguish the route from Kaleb’s off-ship expeditions and maps of places the children cannot yet reach.

**Evidence:** [revision/latest.md:377](../../revision/latest.md#L377); [visual-novel/game/friendships_book_one.rpy:101](../../visual-novel/game/friendships_book_one.rpy#L101).

**Scene links:** `kaleb_walk`.

<a id="construction_paths"></a>
#### Outer construction zones and passages

`construction_paths` · Basis: **story** · Model: **unplaced**

Multiple half-built passages, scaffolding, stored materials, machinery, clanging metal and welding sparks. Later expeditions use a light, scanner and Arin’s multi-tool; paths narrow and turn. Skilled making and automated construction coexist with living structure.

**Use and privacy:** Work/growth areas encountered by exploring children.

**Location and connection status:** New/outer sections reached from established routes; visible depth and adjacent working heights in the VN.

**Still to resolve:** Connections among separate outings, scale and growth process. “Outer” does not establish vacuum exposure or mean the whole settlement is under this dome.

**Evidence:** [visual-novel/game/script.rpy:155](../../visual-novel/game/script.rpy#L155); [revision/latest.md:425](../../revision/latest.md#L425); [revision/latest.md:431](../../revision/latest.md#L431).

**Scene links:** `meeting_joren`, `kaleb_walk`, `outer_exploration`, `dome_ascent`.

**VN images:** [construction-path.png](../../visual-novel/game/images/backgrounds/construction-path.png).

<a id="construction_room"></a>
#### Construction tools and machinery room

`construction_room` · Basis: **story** · Model: **unplaced**

An enclosed room of tools and machines; a handheld device projects the section’s blueprint, and nearby systems shape materials and work autonomously. The art shows benches, machinery and an open doorway onto the construction route.

**Use and privacy:** Working/staging space encountered on exploration.

**Location and connection status:** Within an unfinished section reached from construction passages.

**Still to resolve:** Full machinery/storage footprint and exact location. It is neither Arin’s nor Soren’s workshop and must not replace either.

**Evidence:** [revision/latest.md:433](../../revision/latest.md#L433); [visual-novel/game/friendships_book_one.rpy:182](../../visual-novel/game/friendships_book_one.rpy#L182); [revision/latest.md:437](../../revision/latest.md#L437).

**Scene links:** `outer_exploration`.

**VN images:** [construction-room.png](../../visual-novel/game/images/backgrounds/book-one/construction-room.png).

<a id="dome_platform"></a>
#### Unfinished dome: scaffold climb and overlook

`dome_platform` · Basis: **story** · Model: **unplaced**

A massive unfinished dome in a new section, with scaffolds and platforms to climb, a usable place to remain through the afternoon, and a view over gardens and passages. The VN shows inhabited structure at many heights around a deep internal landscape.

**Use and privacy:** Local construction outing and friends’ refuge.

**Location and connection status:** Reached through construction areas; overlooks part of Lumen including the pattern to which home belongs.

**Still to resolve:** Height, dimensions, actual view to home and route length. No requirement that this structure caps the entire ship or directly adjoins Cali’s garden. The happy climb ends with a descent.

**Evidence:** [revision/latest.md:447](../../revision/latest.md#L447); [visual-novel/game/friendships_book_one.rpy:234](../../visual-novel/game/friendships_book_one.rpy#L234); [visual-novel/game/friendships_book_one.rpy:239](../../visual-novel/game/friendships_book_one.rpy#L239).

**Scene links:** `dome_ascent`, `cassia_grief`, `treehouse_remembrance`.

**VN images:** [dome.png](../../visual-novel/game/images/backgrounds/book-one/dome.png); [theme-dome-friends.png](../../visual-novel/game/images/cg/book-one/theme-dome-friends.png).

<a id="sanctuary"></a>
#### Sanctuary and First Breath welcome

`sanctuary` · Basis: **story** · Model: **unplaced**

Cali is brought home from the Sanctuary following First Breath. The VN opening depicts the family’s intimate welcome, not a complete facility. Birth/preparation/counseling functions belong to the broader wiki account.

**Use and privacy:** Care and family welcome; privacy appropriate to the occasion.

**Location and connection status:** A distinct place within Lumen, separate from the childhood dwelling.

**Still to resolve:** Book I does not map its layout or birth mechanism. The wiki’s preparation/counseling/ceremony/gathering room list is explicitly phrased as likely, so retain its provisional status.

**Evidence:** [revision/latest.md:5](../../revision/latest.md#L5); [visual-novel/game/script.rpy:27](../../visual-novel/game/script.rpy#L27); [wiki/worldbuilding/The-Sanctuary.md:103](../../wiki/worldbuilding/The-Sanctuary.md#L103).

**Scene links:** `first_memory`.

**VN images:** [first-memory-young.png](../../visual-novel/game/images/cg/first-memory-young.png).

<a id="moon_expedition"></a>
#### Nearby moon research expedition

`moon_expedition` · Basis: **remote** · Model: **unplaced**

Joren and family leave for a routine research expedition to a nearby moon; an unexpected malfunction causes the fatal accident despite attempted rescue. The news/grief is staged at home.

**Use and privacy:** Off-Lumen family expedition.

**Location and connection status:** Away from Lumen’s childhood construction sites.

**Still to resolve:** Vehicle, moon terrain, facility, malfunction mechanics and other casualties are unspecified. Do not make the dome climb the accident or design a fatal gravity failure to explain it.

**Evidence:** [revision/latest.md:475](../../revision/latest.md#L475); [visual-novel/game/friendships_book_one.rpy:304](../../visual-novel/game/friendships_book_one.rpy#L304).

**Scene links:** `loss`.

### Wiki and design provisions

<a id="shared_work_facilities"></a>
#### Guild workshops, studios, archives and training

`shared_work_facilities` · Basis: **wiki** · Model: **unplaced**

The existing wiki describes shared equipped work/studio spaces, archives, training and pooled materials. Distinct from family-associated workshops/libraries; the full world needs both scales.

**Use and privacy:** Guild members, learners and collaborators.

**Location and connection status:** Within Lumen’s wider economic/work network; Book I does not map these facilities.

**Still to resolve:** Which facilities exist at the childhood census, their distribution and shared versus personal equipment. Professional roles alone do not prove a separate room for every occupation.

**Evidence:** [wiki/worldbuilding/Socioeconomics.md:37](../../wiki/worldbuilding/Socioeconomics.md#L37); [wiki/worldbuilding/Socioeconomics.md:38](../../wiki/worldbuilding/Socioeconomics.md#L38).

<a id="markets_exchange"></a>
#### Markets, exchange and shared supplies

`markets_exchange` · Basis: **wiki** · Model: **unplaced**

The wiki assigns general markets to the Central Plaza and also describes specialty exchanges and skill fairs. These require event setup, goods movement and storage arrangements, not necessarily dedicated permanent retail buildings.

**Use and privacy:** Households and guilds.

**Location and connection status:** The wiki names the Central Plaza; other venues and childhood scheduling are not established by the VN.

**Still to resolve:** Childhood scope, handling/storage routes and use of the same public space across different events.

**Evidence:** [wiki/worldbuilding/Socioeconomics.md:205](../../wiki/worldbuilding/Socioeconomics.md#L205); [wiki/worldbuilding/Socioeconomics.md:206](../../wiki/worldbuilding/Socioeconomics.md#L206).

<a id="living_systems"></a>
#### Cultivation, circulation and maintenance systems

`living_systems` · Basis: **story-and-wiki** · Model: **unplaced**

Lyron explains water cycling through gardens, people and Lumen; Arin makes irrigation equipment and Soren designs operational systems. The wiki assigns routine cultivation, food processing, maintenance and standard growth to automation while people experiment and guide it.

**Use and privacy:** Distributed ecological/work support.

**Location and connection status:** Connects gardens and inhabited spaces throughout the living body; not necessarily one central mechanical plant.

**Still to resolve:** Production areas, water/nutrient/air routes, light, root volumes, heat and service access. A decorative garden alone does not size the entire food or metabolic system.

**Evidence:** [visual-novel/game/friendships_book_one.rpy:47](../../visual-novel/game/friendships_book_one.rpy#L47); [visual-novel/game/friendships_book_one.rpy:51](../../visual-novel/game/friendships_book_one.rpy#L51); [wiki/worldbuilding/Socioeconomics.md:293](../../wiki/worldbuilding/Socioeconomics.md#L293).

**Scene links:** `cassia_home`, `community_memorial`.

<a id="care_work"></a>
#### Professional care and counseling provision

`care_work` · Basis: **wiki-and-inference** · Model: **unplaced**

Sage is a transition counselor; Thalia mediates; the wiki includes biomedical and wellness practice. These roles need suitable settings and privacy in a developed world. Household comfort scenes do not assign every professional appointment to Sage’s bedroom.

**Use and privacy:** Care recipients, practitioners and invited support.

**Location and connection status:** Location and possible shared facilities are unresolved.

**Still to resolve:** Which care settings are shared, part of the Sanctuary, elsewhere in a neighborhood, or within a practitioner’s home. Do not invent a named childhood clinic or ceremonial core chamber.

**Evidence:** [revision/latest.md:39](../../revision/latest.md#L39); [wiki/worldbuilding/Socioeconomics.md:29](../../wiki/worldbuilding/Socioeconomics.md#L29).

<a id="mobility_services"></a>
#### Accessible movement, deliveries and exterior transfer

`mobility_services` · Basis: **inference** · Model: **unplaced**

A deeply inhabited body and off-ship expeditions require usable movement and transfer arrangements. Book I gives paths, stairs, scaffolds and carried projects; it does not provide a complete accessible transport, supply or docking plan.

**Use and privacy:** Residents, visitors and service work.

**Location and connection status:** To be worked into the distributed body around preserved local scenes.

**Still to resolve:** Accessible alternatives, inter-level connections, supplies/waste, emergency access and off-ship transfer. Elevators, docks or shafts drawn in studies remain proposals, not discovered story locations.

**Evidence:** [revision/latest.md:57](../../revision/latest.md#L57); [revision/latest.md:475](../../revision/latest.md#L475).

### Narrated and represented places

<a id="imagined_places"></a>
#### Stories, dreams, maps and painted worlds

`imagined_places` · Basis: **represented-settings** · Model: **not-physical**

Sage’s Aria/Bram/Cora Astravus and central water system; Nibble’s fairy-tale land; Kael’s dream crystal cave; Dorian’s narrated distant journeys; Cassia’s creature and talking trees; map rivers, pirate ship, space station and planets; places painted on the mural. These are remembered, imagined or represented settings, not extra measured places inside childhood Lumen. Including narrated history here does not classify that history as fictional; distant destinations are simply outside this local layout.

**Use and privacy:** Imagined or represented.

**Location and connection status:** Stories are told in real rooms and refuges whose space is inventoried separately.

**Still to resolve:** Do not derive Lumen’s physical central hub, life-support architecture, oceans or alien fauna from these narrative layers. Other Astravii mentioned as heritage are not rooms within Lumen.

**Evidence:** [revision/latest.md:159](../../revision/latest.md#L159); [revision/latest.md:209](../../revision/latest.md#L209); [revision/latest.md:405](../../revision/latest.md#L405); [visual-novel/game/friendships_book_one.rpy:422](../../visual-novel/game/friendships_book_one.rpy#L422).

**Scene links:** `dorian_stories`, `sage_story`, `family_rhythm`, `meeting_cassia`, `treehouse`, `rain_refuge`, `painting_grief`, `mural_remembrance`.

## Connections to preserve or resolve

Explicit text, audible relationships, visual observations and open attachments are labeled separately. A hearing relationship is not proof of a shared wall; successive scene backgrounds are not proof of an immediate connecting door.

| From / to | Basis | Constraint |
|---|---|---|
| [Shared central room](#central_room); [Internal halls and thresholds](#home_halls) | explicit | Halls branch from the shared central room to other parts of the home. [revision/latest.md:69](../../revision/latest.md#L69). |
| [Cali's private room](#cali_room); [Kael's private room](#kael_room) | explicit | Kael’s room is next to Cali’s. [revision/latest.md:77](../../revision/latest.md#L77). |
| [Cali's private room](#cali_room); [Lyra's private room](#lyra_room) | explicit | Lyra’s room lies on the other side of Cali’s from Kael’s; this does not set compass directions. [revision/latest.md:81](../../revision/latest.md#L81). |
| [Internal halls and thresholds](#home_halls); [Selene's music room](#selene_music) | explicit | Cali hears music in the hall before reaching Selene’s door. [visual-novel/game/family_book_one.rpy:125](../../visual-novel/game/family_book_one.rpy#L125). |
| [Sage's room](#sage_room); [Shared central room](#central_room) | audible | The household fountain is audible beyond Sage’s door; this constrains the sound path without proving immediate adjacency. [visual-novel/game/family_book_one.rpy:271](../../visual-novel/game/family_book_one.rpy#L271). |
| [Cali's childhood home](#home); [Maia's household garden](#maia_garden) | explicit | The garden folds around the home. Current VN home art includes an opening toward planted outdoor space. [visual-novel/game/script.rpy:52](../../visual-novel/game/script.rpy#L52). |
| [Sunflower bed and daily garden learning](#planting_patch); [Oak ladder, landing and upper entrance](#treehouse_access) | sightline | Cali sees the ladder into the oak from the planting patch. [visual-novel/game/script.rpy:96](../../visual-novel/game/script.rpy#L96). |
| [Maia's household garden](#maia_garden); [Oak treehouse: upper room](#treehouse_upper) | explicit | The treehouse is at the garden’s far corner/wooded edge; the upper room looks onto its flowers and glowing paths. [revision/latest.md:385](../../revision/latest.md#L385); [visual-novel/game/script.rpy:191](../../visual-novel/game/script.rpy#L191). |
| [Oak lower hollow and second entrance](#treehouse_hollow); [Oak treehouse: upper room](#treehouse_upper) | vertical | The lower hollow is underneath the raised room and has a separate entrance. [revision/latest.md:395](../../revision/latest.md#L395). |
| [Furnished refuge beneath the oak](#treehouse_lower_sitting); [Oak ladder, landing and upper entrance](#treehouse_access) | visual | The VN wide garden view connects the furnished lower platform to the ladder and upper landing. [visual-novel/docs/location-continuity.json:81](../../visual-novel/docs/location-continuity.json#L81). |
| [Maia's household garden](#maia_garden); [Shared woodland, open ground and nearby households](#local_landscape) | author | Household garden privacy meets more shared woods/open ground; a social threshold need not break planting continuity or the ladder sightline. [visual-novel/game/script.rpy:52](../../visual-novel/game/script.rpy#L52). |
| [Arin's workshop](#arin_workshop); [Miniature waterwheel test site](#waterwheel_site) | carried-project | The wheel is made in Arin’s workshop and carried to a garden pond; distance and thresholds remain unplaced. [visual-novel/game/friendships_book_one.rpy:143](../../visual-novel/game/friendships_book_one.rpy#L143). |
| [Outer construction zones and passages](#construction_paths); [Construction tools and machinery room](#construction_room) | explicit | The children enter a machinery room from the construction passages. [visual-novel/game/friendships_book_one.rpy:182](../../visual-novel/game/friendships_book_one.rpy#L182). |
| [Outer construction zones and passages](#construction_paths); [Unfinished dome: scaffold climb and overlook](#dome_platform) | explicit | The dome outing approaches through construction and climbs scaffolds to an elevated platform. [visual-novel/game/friendships_book_one.rpy:225](../../visual-novel/game/friendships_book_one.rpy#L225); [visual-novel/game/friendships_book_one.rpy:239](../../visual-novel/game/friendships_book_one.rpy#L239). |
| [Central Plaza, approaches and occupied galleries](#central_plaza); [Community storytelling courtyard](#courtyard) | distinct | The recurring community-wide plaza and local storytelling court are distinct production locations. [visual-novel/docs/LOCATION_CONTINUITY.md:47](../../visual-novel/docs/LOCATION_CONTINUITY.md#L47). |
| [Oak treehouse: upper room](#treehouse_upper); [Tree of Echoes approach and clearing](#echoes_grove) | distinct | The oak refuge and ancient transplanted Tree of Echoes are different trees and destinations. [visual-novel/docs/location-continuity.json:61](../../visual-novel/docs/location-continuity.json#L61). |
| [Joren's home](#joren_home); [Soren's systems workshop](#soren_workshop) | attachment-open | The family visit uses Soren’s workshop; narrative association does not map the whole dwelling or establish a specific connecting door. [visual-novel/game/friendships_book_one.rpy:104](../../visual-novel/game/friendships_book_one.rpy#L104). |
| [Arin's workshop](#arin_workshop); [Cali's childhood home](#home) | attachment-open | Workshop is part of the family’s daily spatial program; exact connection and service entrance need design. [visual-novel/game/script.rpy:45](../../visual-novel/game/script.rpy#L45). |
| [Dorian's library and reading area](#dorian_library); [Cali's childhood home](#home) | attachment-open | The family repeatedly uses Dorian’s library; preserve it while resolving its connection, not by replacing it with shared-room shelving. [visual-novel/game/family_book_one.rpy:193](../../visual-novel/game/family_book_one.rpy#L193). |

## VN image register

All background/CG definitions and all closing-theme images are assigned. The observations record what was inspected; camera limits and production choices remain distinct from textual canon. Existing detailed visual-continuity rules remain in the [production register](../../visual-novel/docs/location-continuity.json). The [annotated atlas](lumen-study/Reference-Atlas.md) presents a selection of these images.

| Image / runtime name | Space | Inspected spatial evidence |
|---|---|---|
| [family-home.png](../../visual-novel/game/images/backgrounds/family-home.png) · `bg family_home` | [Shared central room](#central_room); [Internal halls and thresholds](#home_halls) | Round table, sofa left, fountain behind, passage rear-right and garden opening at right; whole dwelling remains off camera. |
| [family-home-painting.png](../../visual-novel/game/images/backgrounds/book-one/family-home-painting.png) · `bg family_home_painting` | [Shared central room](#central_room); [Household drawing and painting provision](#home_painting) | Same central room with painting materials and work in progress on the table. |
| [home-dusk.png](../../visual-novel/game/images/backgrounds/book-one/home-dusk.png) · `bg home_dusk` | [Shared central room](#central_room) | Dusk/grief state of the same room; no new grief room. |
| [garden-close.png](../../visual-novel/game/images/backgrounds/garden-close.png) · `bg garden_close` | [Maia's household garden](#maia_garden); [Sunflower bed and daily garden learning](#planting_patch); [Garden ponds and the shallow rescue basin](#garden_ponds) | Timber-edged beds beside a curved stone path and a pond behind; local brighter planting light within enclosure. |
| [garden.png](../../visual-novel/game/images/backgrounds/garden.png) · `bg garden` | [Maia's household garden](#maia_garden); [Oak treehouse: upper room](#treehouse_upper); [Oak ladder, landing and upper entrance](#treehouse_access); [Oak lower hollow and second entrance](#treehouse_hollow); [Furnished refuge beneath the oak](#treehouse_lower_sitting) | Upper room projects left of the right-hand oak; ladder meets landing; separate lower door and broad furnished platform. Ground path approaches from left. |
| [community-courtyard.png](../../visual-novel/game/images/backgrounds/community-courtyard.png) · `bg community_courtyard` | [Community storytelling courtyard](#courtyard) | Local low-table gathering circles, planted edges, rounded arches and adjoining passages. |
| [construction-path.png](../../visual-novel/game/images/backgrounds/construction-path.png) · `bg construction_path` | [Outer construction zones and passages](#construction_paths); [Community halls, paths and planted walkways](#community_routes) | Curved path through thick branching structure, stored panels/tools, scaffolds and adjacent occupied working heights. |
| [treehouse-shaded.png](../../visual-novel/game/images/backgrounds/treehouse-shaded.png) · `bg treehouse` | [Oak treehouse: upper room](#treehouse_upper) | Left diagonal trunk, arched entrance behind, open right bays/rails, curtains, maps, boxes and cushions; broad useful room. |
| [treehouse-rain.png](../../visual-novel/game/images/backgrounds/treehouse-rain.png) · `bg treehouse_rain` | [Oak treehouse: upper room](#treehouse_upper) | Same structural room with rain outside the open bays; interior remains sheltered. |
| [treehouse-later.png](../../visual-novel/game/images/backgrounds/book-one/treehouse-later.png) · `bg treehouse_later` | [Oak treehouse: upper room](#treehouse_upper) | Same structure; table moved toward the viewing bays, changed seating and accumulated projects in later childhood. |
| [treehouse-memory.png](../../visual-novel/game/images/backgrounds/book-one/treehouse-memory.png) · `bg treehouse_memory` | [Oak treehouse: upper room](#treehouse_upper) | Later furniture arrangement plus messages/drawings and rain outside; ordinary remembrance. |
| [workshop.png](../../visual-novel/game/images/backgrounds/book-one/workshop.png) · `bg workshop` | [Arin's workshop](#arin_workshop) | Broad rear workbench and side benches/drawers, tools and small mechanisms, stool, timber floor, planted window left and doorway right. |
| [workshop-waterwheel.png](../../visual-novel/game/images/backgrounds/book-one/workshop-waterwheel.png) · `bg workshop_waterwheel` | [Arin's workshop](#arin_workshop) | Same workshop; small wooden wheel occupies the workbench as a project state. |
| [music-room.png](../../visual-novel/game/images/backgrounds/book-one/music-room.png) · `bg music_room` | [Selene's music room](#selene_music) | Piano and shared bench center, harp and soft seating right, hallway doorway left and planted window openings. |
| [library.png](../../visual-novel/game/images/backgrounds/book-one/library.png) · `bg library` | [Dorian's library and reading area](#dorian_library) | Books/scrolls around a map table and reading area, additional work surfaces, windows, overhead light and corridor through rear arch. |
| [sage-room.png](../../visual-novel/game/images/backgrounds/book-one/sage-room.png) · `bg sage_room` | [Sage's room](#sage_room); [Private provision for Maia, Arin, Selene, Dorian and Sage](#adult_retreats) | Cushioned gathering around low table, sleeping alcove behind, door left, window right; personal and welcoming uses in one room. |
| [cassia-home.png](../../visual-novel/game/images/backgrounds/book-one/cassia-home.png) · `bg cassia_home` | [Cassia's home](#cassia_home) | Craft surfaces/books, drying drawings, tea table and seating; planted water feature and another room through a rear-left arch. |
| [soren-workshop.png](../../visual-novel/game/images/backgrounds/book-one/soren-workshop.png) · `bg soren_workshop` | [Soren's systems workshop](#soren_workshop) | Drafting bench and plans, tool drawers, work surfaces, floor rover prototype and arched corridor at right; distinct from Arin’s shop. |
| [echoes.png](../../visual-novel/game/images/backgrounds/book-one/echoes.png) · `bg echoes` | [Tree of Echoes approach and clearing](#echoes_grove) | Ancient hollow tree in a planted clearing, dense enclosure and overhead foliage/light; no literal faces or voices. |
| [garden-pond.png](../../visual-novel/game/images/backgrounds/book-one/garden-pond.png) · `bg garden_pond` | [Garden ponds and the shallow rescue basin](#garden_ponds); [Dry pond bank and plant-arranging area](#pond_bank) | Low stone coping, shallow pebbled basin, inlet left, plant groups and timber boundary; accessible dry bank. |
| [garden-work-area.png](../../visual-novel/game/images/backgrounds/book-one/garden-work-area.png) · `bg garden_work_area` | [Dry pond bank and plant-arranging area](#pond_bank); [Garden ponds and the shallow rescue basin](#garden_ponds) | Wider dry working bank with potted plants; basin remains behind the occupied ground. |
| [waterwheel.png](../../visual-novel/game/images/backgrounds/book-one/waterwheel.png) · `bg waterwheel` | [Miniature waterwheel test site](#waterwheel_site); [Garden ponds and the shallow rescue basin](#garden_ponds); [Dry pond bank and plant-arranging area](#pond_bank) | Miniature wheel and supports by inlet of the recurring basin; tools on dry foreground bank. |
| [garden-wonders.png](../../visual-novel/game/images/backgrounds/book-one/garden-wonders.png) · `bg garden_wonders` | [Sunflower bed and daily garden learning](#planting_patch); [Maia's household garden](#maia_garden) | Closing-theme flower/insect detail beside the garden path; no new garden location. |
| [memory-mural-v2.png](../../visual-novel/game/images/backgrounds/book-one/memory-mural-v2.png) · `bg memory_mural` | [Garden mural and remembrance place](#garden_mural) | Hand-painted wall with working supplies, bench and planted water beside it. The adventure landscape on the wall is paint. |
| [festival.png](../../visual-novel/game/images/backgrounds/book-one/festival.png) · `bg festival` | [Central Plaza, approaches and occupied galleries](#central_plaza); [Plaza stage and floral/display space](#plaza_stage) | Large tree/curved stair left, rear passage beneath bridge, occupied multi-level arcades, low dais center-right, floral display and lanterns. |
| [memorial-plaza.png](../../visual-novel/game/images/backgrounds/book-one/memorial-plaza.png) · `bg memorial_plaza` | [Central Plaza, approaches and occupied galleries](#central_plaza); [Plaza stage and floral/display space](#plaza_stage) | Same plaza architecture with flowers/messages and a gathered crowd; festival instruments removed. |
| [remembrance-plaza.png](../../visual-novel/game/images/backgrounds/book-one/remembrance-plaza.png) · `bg remembrance_plaza` | [Central Plaza, approaches and occupied galleries](#central_plaza); [Plaza stage and floral/display space](#plaza_stage) | Same square and dais with annual drawings/messages, crowd and changed light. |
| [construction-room.png](../../visual-novel/game/images/backgrounds/book-one/construction-room.png) · `bg construction_room` | [Construction tools and machinery room](#construction_room) | Benches, tools, machinery and projected section drawing; doorway joins a planted construction passage. |
| [dome.png](../../visual-novel/game/images/backgrounds/book-one/dome.png) · `bg dome` | [Unfinished dome: scaffold climb and overlook](#dome_platform) | Foreground overlook/parapet and scaffolds; views across gardens, branching structure, arches and inhabitants at many heights. This does not measure the whole ship. |
| [first-memory-young.png](../../visual-novel/game/images/cg/first-memory-young.png) · `cg first_memory` | [Sanctuary and First Breath welcome](#sanctuary) | Close welcome with five adults and newborn Cali, cushions, cloth and warm alcoves; facility extent and birth mechanism unseen. |
| [garden-compromise.png](../../visual-novel/game/images/cg/book-one/garden-compromise.png) · `cg garden_compromise` | [Dry pond bank and plant-arranging area](#pond_bank) | Three people arranging plants on dry supported bank; pond reflections and planting choices remain visible. |
| [flute-playing.png](../../visual-novel/game/images/cg/book-one/flute-playing.png) · `cg flute_playing` | [Selene's music room](#selene_music) | Cali and Selene share the piano bench; harp, keyboard and surrounding room remain coherent. |
| [flute-rest.png](../../visual-novel/game/images/cg/book-one/flute-rest.png) · `cg flute_rest` | [Selene's music room](#selene_music) | Same lesson composition and bench while the flute is lowered; not another room. |
| [pond-rescue.png](../../visual-novel/game/images/cg/book-one/pond-rescue.png) · `cg pond_rescue` | [Dry pond bank and plant-arranging area](#pond_bank); [Garden ponds and the shallow rescue basin](#garden_ponds) | Children kneel on a dry low bank and reach wet Lyra in shallow water; animals have supported ground. |
| [pond-comfort.png](../../visual-novel/game/images/cg/book-one/pond-comfort.png) · `cg pond_comfort` | [Dry pond bank and plant-arranging area](#pond_bank); [Garden ponds and the shallow rescue basin](#garden_ponds) | Siblings sit together on broad dry ground beside the recurring basin after the rescue. |
| [cassia-storytelling.png](../../visual-novel/game/images/cg/book-one/cassia-storytelling.png) · `cg cassia_storytelling` | [Community storytelling courtyard](#courtyard) | Children seated with sketchbook and cushions, adult gathering and arches behind; intimate court. |
| [family-embrace.png](../../visual-novel/game/images/cg/book-one/family-embrace.png) · `cg family_embrace` | [Shared central room](#central_room) | Maia and Cali on central-room sofa, table and corridor behind; comfort occupies existing home space. |
| [cassia-comfort.png](../../visual-novel/game/images/cg/book-one/cassia-comfort.png) · `cg cassia_comfort` | [Oak treehouse: upper room](#treehouse_upper) | Seated beside the trunk, with upper door and open bays visible; later table and seats remain behind. |
| [treehouse-friends.png](../../visual-novel/game/images/cg/book-one/treehouse-friends.png) · `cg treehouse_friends` | [Oak treehouse: upper room](#treehouse_upper) | Trio seated around the low map table in the familiar upper room; close framing does not shrink the unseen room. |
| [theme-garden-opening.png](../../visual-novel/game/images/cg/book-one/theme-garden-opening.png) · Closing theme | [Sunflower bed and daily garden learning](#planting_patch) | Close sunflower/garden moment; no additional outdoor location. |
| [theme-path-friends.png](../../visual-novel/game/images/cg/book-one/theme-path-friends.png) · Closing theme | [Community halls, paths and planted walkways](#community_routes) | Distinct timber neighborhood walkway with branch rails, plants and occupied structures beyond; not the specific oak garden approach. |
| [theme-insect-discovery.png](../../visual-novel/game/images/cg/book-one/theme-insect-discovery.png) · Closing theme | [Sunflower bed and daily garden learning](#planting_patch) | Children inspect an insect by garden planting and dry path. |
| [theme-nibble-moment.png](../../visual-novel/game/images/cg/book-one/theme-nibble-moment.png) · Closing theme | [Maia's household garden](#maia_garden) | Cali and Nibble beside an outdoor timber bench; intimate garden resting provision. |
| [theme-treehouse-arrival.png](../../visual-novel/game/images/cg/book-one/theme-treehouse-arrival.png) · Closing theme | [Oak treehouse: upper room](#treehouse_upper) | Close trio inside upper room with trunk, entrance and viewing bays; filename does not establish a new arrival building. |
| [theme-waterwheel-team.png](../../visual-novel/game/images/cg/book-one/theme-waterwheel-team.png) · Closing theme | [Miniature waterwheel test site](#waterwheel_site); [Dry pond bank and plant-arranging area](#pond_bank) | Children work around miniature wheel on dry bank beside pond; illustrative assembly/test moment. |
| [theme-dome-friends.png](../../visual-novel/game/images/cg/book-one/theme-dome-friends.png) · Closing theme | [Unfinished dome: scaffold climb and overlook](#dome_platform) | Trio stands on the overlook with parapet and layered inhabited view behind. |
| [theme-sketch-laughter.png](../../visual-novel/game/images/cg/book-one/theme-sketch-laughter.png) · Closing theme | [Oak treehouse: upper room](#treehouse_upper) | Tight composition of map table and friends inside the upper room; sketch creature is fictional. |
| [theme-evening-reading.png](../../visual-novel/game/images/cg/book-one/theme-evening-reading.png) · Closing theme | [Oak treehouse: upper room](#treehouse_upper) | Cali sketches on her lap by cushions and an open rail; this is not her private bedroom desk. |
| [theme-morning-outlook.png](../../visual-novel/game/images/cg/book-one/theme-morning-outlook.png) · Closing theme | [Maia's household garden](#maia_garden); [Oak treehouse: upper room](#treehouse_upper); [Furnished refuge beneath the oak](#treehouse_lower_sitting); [Oak ladder, landing and upper entrance](#treehouse_access) | Cali on garden route with oak’s upper room, lower refuge and ladder behind; camera separation matters for apparent scale. |
