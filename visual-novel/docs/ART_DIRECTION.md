# A home inside a living world

The author's repository images are the visual authority. They are concepts, not exact blueprints, but they establish a specific feeling that the first garden candidate missed.

## Reference review

| Reference, relative to the repository root | What this adaptation takes from it |
| --- | --- |
| `revision/Treehouse.png` | Primary garden reference. A huge close oak, patchwork timber house, branch railings, ladder, a lower door in the trunk, circular seating, cushions and accumulated treasures. Amber lights glow locally within a dark, enclosing, bioluminescent canopy. The place feels handled, repaired, and shared. |
| `revision/Treehouse.jpg` | Earlier monochrome construction reference. Reinforces the two levels, trunk entrance, intimate scale, irregular wood, and sheltered seating. |
| `revision/Calista.png` | Primary Calista reference. Chestnut curls, freckles, blue eyes, olive skin, cream and green practical clothing, warmth, and painterly realism. Use the child design in this chapter. |
| `revision/Calista.jpg` | Earlier monochrome character study; supports facial identity and the distinction between childhood and later life. |
| `revision/Echoes.jpg` | Enclosure, mystery, luminous foliage, and the scale of a child beneath an old tree. This depicts a separate place: the Tree of Echoes must not become the oak in Maia's garden. |
| `visuals/lumen-life.png` | Dark teal and blue vegetation, warm occupied spaces, subtle luminous structure. A reference for close local views; the panorama itself is excluded from this chapter because its star-facing enclosure reveals too much too soon. |

The first generated garden retained an attractive painterly finish but overemphasized bright white structural ribs and an open atrium. Its distant treehouse did not carry the scene. The darker revision brings the tree close, adds the low entrance and shared belongings, and lowers the overall brightness. Light comes mainly from small amber lamps, blue-green foliage, and a narrow shaft reaching the planting beds. The larger spacecraft architecture recedes behind the canopy.

The author subsequently clarified that the generated interior should be preserved and that the garden's shading and palette should be kept, rather than its particular upper treehouse design. The interior is therefore the authority for the building: a broad shallow timber room with large viewing bays, branch railings, rust curtains, a low roof, and an arched entrance near the trunk. The exterior must accommodate that room. The opaque little cottage facade in the darker garden candidate is superseded.

## Current selected assets

The built-in image generation tool made seven environment images (including the rainy treehouse variant), four character portraits, and a First Memory family illustration. Exact prompts, reference relationships, and output identifiers are in `assets.json`. Earlier and superseded candidates stay in the ignored `.art-staging/` directory and are excluded from distributions.

First Memory uses `game/images/cg/first-memory-young.png`, an edit of the previous family illustration that retains its arrangement, room, clothing, and newborn. It depicts Cali safely swaddled in Maia's arms with Arin on the left, Selene behind the left side, Dorian behind the right side, and Sage on the right. Faces and the baby sit above the reading panel. The Sanctuary is represented by warm plaster alcoves, timber, fabric, and quiet lamplight. The image illustrates the parents' account without specifying a birth mechanism or implying that Cali directly remembers it.

The previous illustration overused later-life age cues and missed Dorian's rich dark skin and Selene's deep bronze skin. The revised parents have less lined faces, Maia has fewer silver strands, and Dorian has a predominantly dark beard. Arin remains pale and freckled, Sage warm tan and freckled. Selene's white hair remains: [her biography](../../wiki/bios/Selene.md) explicitly says it began graying at 30 for genetic reasons. Hair color is not a universal age indicator.

The parents' biographies list 125+ years **by the later narrative**, not at Cali's First Breath. Their exact ages at her birth are not supplied. [Astraviin development](../../wiki/worldbuilding/The-Astraviin.md) also describes long lifespans and continuing vitality, so ordinary human aging arithmetic would be misleading. The younger appearance is an interpretation requested for this earlier scene, not a newly established numerical age. Do not automatically backdate later scars, injuries, gray hair, or posture to First Breath. Future character sheets should distinguish stable identity traits from scene-specific age and clothing.

`family-home.png` marks the move into later childhood before the narration describes Lyra and the three-child household. Its central round table, cushioned seating, books, artwork, small fountain, branching passages, and filtered ceiling light follow the draft's home description. It returns for the shared-map transition. Pets remain part of the remembered narration rather than being added to every background.

The later opening and planting lesson use `garden-close.png`: another spot in Maia's garden, away from the oak's dense canopy, with brighter filtered light on the soil and path. The transition occurs as the narration turns from the family to Maia's garden. It is a different camera view, with the treehouse behind the camera. The wider `garden.png` introduces the ladder after planting and returns for the friends' familiar visit. This change of place gives the reflective opening room without requiring the entire garden to share the lookout's darkness.

`community-courtyard.png` places Cassia's meeting among local families and garden paths. `construction-path.png` places Joren's challenge beside an unfinished arch, stacked panels and scaffolding, with a low ledge and a blue fringe to the light that Cali notices. Neither exposes the outer nature of Lumen. These are new location interpretations, not exact blueprints from the prose.

The lookout uses `treehouse-shaded.png`, a lighting edit of the retained interior. Its camera, room geometry, furnishings, and warm lamp pools stay in place; the bright view through the open bays becomes shaded teal foliage. The interior remains the architectural authority for the exterior. The original interior is retained as an ignored art candidate, with its prompt and output identifier preserved in the provenance record.

`treehouse-rain.png` edits that shaded view to show rain beyond the open bays, drops along the eaves and railings, and cooler wet foliage. The table, maps, cushions, trunk, openings, and camera remain in place. The script changes the background together with the ambience before discussing rainy afternoons. It does not claim the table moved, nor put glass into the originally open windows. The rain is painted rather than animated; rollback restores both the earlier view and its garden ambience.

Character identity comes from the reference sheets and character biographies. Calista is a child with chestnut hair, freckles, and green overalls. Maia has warm brown skin, gray-streaked braids, gardening clothes, and a seed in her hand. Cassia has rich umber skin, green eyes, chestnut waves, and a natural wrist birthmark. Joren has fair ruddy skin, blond hair, blue eyes, and practical mended clothes.

These are first-playable design selections, not a declaration that the author has approved final character models. There is one standing pose per character. Future angles should use the retained interior and reconciled exterior together. Seen from the garden, the room projects left from the trunk and its arched entrance sits by the trunk at the right end; viewed outward from inside, that relationship reverses. The ladder must reach the entrance landing, and the floor and roof must span the same room in both views.

## Compositing and source preservation

The generator flattened a transparency checkerboard into the RGB files for Calista, Cassia, and Joren, including after a requested transparency correction. The game therefore removes bright neutral matte pixels with a shared Ren'Py shader in `game/visuals.rpy`. The PNG source files are preserved as generated. Maia has an alpha channel but retains some painted rim light. These are working composites; future sprite revisions should provide clean alpha and a broader expression set.

The title and reading interface use dark teal, restrained gold, generous text spacing, and native vector gradients. UI darkening is a separate layer so the selected paintings remain replaceable without destructive edits. No menu or story text is baked into art.
