# Construction path grounding review

Reviewed 2026-09-05 by the release-matrix agent in Ren’Py 8.5.3, Linux/Xvfb, 1920×1080 logical framing. The focused `environment_grounding_review` suite completed **8 assertions**. Screenshots hide the dialogue interface using the real H-key action, so it cannot conceal floating feet or paws.

The background’s foreground left is a raised work ledge; its right is occupied by panels, a tool crate and coiled rope. Generic left/right stage positions placed the children against those objects. For this background only, `at_left` and `at_right` now use the clear central paving, retaining the shared standing baseline and age-specific scale. Other locations retain their original positions.

| Frame | Actual observation |
| --- | --- |
| `grounding-first-joren.png` · scene 15 | Early Calista and Joren stand on the central stone paving. Calista’s boots clear the ledge face; Joren’s boots clear the tool crate and rope. Bodies and faces remain distinct. |
| `grounding-kaleb-path.png` · scene 17 | The home-outfit Calista uses the same path placement beside young Joren; both boots have plausible support. Kaleb is represented by the dialogue portrait in normal interface mode. |
| `grounding-expedition-path.png` · scene 21 | Older children retain their modest height difference and stand on the paving. The previous generic familiar line put Shadow and Barkley at knee/waist height without support. Location-specific transforms now place them on foreground stones, with normal foreground overlap at the children’s boots. Nibble sits on the actual work-ledge top. No pet covers a face or hand. |
| `grounding-dome-path.png` · scene 23 | Older children stand on the same clear path before the ascent; the rope and tool crate remain visible at right. |
| `grounding-garden-default.png` · scene 2 | The next chapter jump restores ordinary left/right positions, confirming the construction adjustment does not leak into other backgrounds. |

## Remaining recurring placements

The focused review now includes twelve UI-hidden frames. Home sofa/table/door placements have visible support and remain unchanged. At the pond, Shadow sits on the tool box, Nibble uses its edge and Barkley sits on the dry bank; no animal stands on water. At Echoes the animals occupy the farther clearing floor, while the children stand nearer the camera. These surfaces were checked visually, not inferred from their Y coordinates.

The construction-room shelf placements were demonstrably unsupported, so its three companions now sit on clear floor before the workbench. Nibble’s music-room placement moved from below the piano stool to the floor in front of it, matching the narrated movement. The native captures show actual paws on those surfaces. Nibble’s path transform resolves its coordinates at each location change so Ren’Py does not reuse the preceding location’s ATL state.

In the treehouse dispute the earlier generic stage put Calista’s boots over the open treasure chest and Joren’s over the map table. `book_stage` now places actors on the clear interior floor to the left of the round table. All five stage positions use the same 0.76 distance multiplier and floor baseline for dry/rain/remembrance variants; it changes camera distance, not relative body height. The close-standing dispute and mourning pairs were inspected with the interface hidden. Their feet clear both foreground objects and their faces/hands stay readable. Shadow correctly remains on the map table, as the source says; Barkley has a cushion and Nibble is on the floor. The baseline character-framing test continues to use a neutral stage and separately checks the production height contract.

Evidence additionally includes `grounding-construction-room.png`, `grounding-music-familiars.png`, `grounding-echoes-familiars.png`, `grounding-waterwheel-familiars.png`, `grounding-dispute-familiars.png`, `grounding-home-familiars.png`, and `grounding-treehouse-grief.png`.

Current evidence: `test-results/native-grounding.log`, these five files in `test-results/screenshots/`, and exact input/frame hashes in `test-results/construction-grounding-inputs.json`. The native full-book and visual rows still require the final integrated run. This focused review checks the recurring familiar placements; it does not replace the full cross-game scene/UI review.
