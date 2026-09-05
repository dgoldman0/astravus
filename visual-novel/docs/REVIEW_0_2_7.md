# Pacing and action staging — 0.2.7 alpha

This pass addresses the planting scene's unusable foreground and the gap between narrated actions and neutral standing poses. The story remains the same 32-scene adaptation of Book I. The source remains `revision/latest.md`; the protected narration bridging scenes 24–25 is unchanged.

## Staging

| Scene | Change |
| --- | --- |
| 3, planting disagreement | A wider view places the pond behind a broad dry working area and shows the flower pots. The discussion moves into an illustration of Cali, Kael and Maia crouching together with the pots. |
| 5, first music lesson | Cali and Selene sit at the piano. Separate playing and resting illustrations follow the single broken attempt, encouragement, and later short phrase. The instrument is lowered before Cali speaks. |
| 8, family routine | The same lesson illustrations accompany later flute practice. Lyra still receives her own speaking portrait because she is outside the illustration. |
| 10, pond scare | Cali and Kael kneel on the bank to help wet, frightened Lyra. A second illustration shows Lyra safely out, held by Cali, with Kael nearby. Barkley and Shadow accompany them. |
| 13, meeting Cassia | The shared sketchbook conversation shows Cali and Cassia seated with the other children in the established courtyard. |
| 14, Cassia's family | A short fade marks the later evening with Lyron, in the same home. Reduced motion disables the fade. |
| 24, disagreement | Cali and Joren return to their ordinary poses when they reach a compromise. Source narration and the transition into the loss remain intact. |
| 26, family grief | Maia's embrace is depicted at the line describing it. |
| 28, Cassia's grief | The hand-holding conversation uses a seated illustration of the friends together in their existing treehouse. Cassia retains her corrected facial shading and warm complexion. |

The character-free backgrounds and separate sprites remain available. The eight new scene illustrations are fixed shared moments, not independently animated actors. Their depicted cast is declared in `CG_CAST`; a speaker outside that cast still receives a portrait. Each illustration clears at the next scene or when the action ends. The garden's additional camera angle is used for planting; the original water-focused view remains in the pond scare. These are distinct used assets, not before/after backups.

## Pacing

The prose pass trims repeated questions and closing summaries, clarifies the move from community gatherings to home visits, and gives later exploration and mural work clearer time transitions. Lyra's inclusion ends with the group asking her to join the next hunt. The memorial uses concrete shared memories and silence. No new revelations, metaphysical events, plot outcomes or Book II material are added.

## Artwork provenance

All nine new assets were generated with the **built-in image_gen tool**, using the approved backgrounds and character artwork as references. Selected output pixels are copied unchanged into the project. Full prompts, reference chains, output identifiers, dimensions and hashes are recorded in [assets.json](assets.json) and [environment-assets.json](environment-assets.json).

Runtime paths:

- `game/images/backgrounds/book-one/garden-work-area.png`
- `game/images/cg/book-one/garden-compromise.png`
- `game/images/cg/book-one/flute-playing.png`
- `game/images/cg/book-one/flute-rest.png`
- `game/images/cg/book-one/pond-rescue.png`
- `game/images/cg/book-one/pond-comfort.png`
- `game/images/cg/book-one/cassia-storytelling.png`
- `game/images/cg/book-one/family-embrace.png`
- `game/images/cg/book-one/cassia-comfort.png`

The generation prompts specify intended constraints; selection and in-game review assess the resulting artwork. This remains an alpha with limited expressions and poses. Verification results are recorded in [VALIDATION.md](VALIDATION.md).
