# Integrated runtime visual review

On 2026-09-05 the release-matrix reviewer inspected 49 current native narrative/action/transition frames in nine comparison sheets, plus twelve UI-hidden physical-support frames. The exact native coverage is **29 scenes with a scene/dialogue view, plus scene 25 as a transition-only view**. Final candidate browser frames provide readable scene views for 22, 25 and 32, and were inspected across all 32 scenes. The full native automated suite independently traverses all 32 scenes; that functional traversal is separate from screenshot coverage.

The individual selected images were reviewed separately against chosen earlier references. This pass checks how those assets, portraits, stage positions, text and scene changes appear together. The support corrections and actual full frames are detailed in [CONSTRUCTION_GROUNDING_REVIEW.md](CONSTRUCTION_GROUNDING_REVIEW.md).

The nine native sheets were refreshed and inspected after the final Help and quick-bar repair. Current full-size native Kaleb dialogue, Cassia grief, larger/high-contrast dialogue, Settings and Chapters frames were also inspected. The ten quick controls fit clearly; larger dialogue remains within its solid panel, selection states are readable, and chapter columns do not clip. The separate [usability review](../releases/USABILITY_REVIEW.md) records actual pointer/keyboard behavior and 1280×720/960×540 browser layouts. The final browser verification completed successfully on the unchanged candidate: all 32 normal scene entrances, all 32 backward chapter jumps, all 10 glossary reveal stages, saves and chapter controls, theme playback, actual SUNO hyperlink activation, cache refresh and the unsupported-WebGL fallback passed. Chromium reported no unhandled page/engine errors; its software compositor measured 69.7 fps for the tested two-actor group.

| Scene | Captured view(s) in test-results/screenshots | Observed alignment |
| --- | --- | --- |
| 01 | first-memory; family-home | Family close composition, then the actual shared home; no duplicate sprites over the baby memory. |
| 02 | garden | Cali and Maia on the planting path; actual first-use line and ordinary scene framing. |
| 03 | siblings-garden; garden-compromise | Dry work area and crouched planting action, with Kael larger than Cali and tools/pots within reach. |
| 04 | workshop | Adult/child stature and workshop task framing retained. |
| 05 | first-melody; flute-rest; first-flute-phrase | Flute at lips for playing, lowered for dialogue; distinct first breath and later phrase follow source order. |
| 06 | library | Dorian shown as the speaker in the library. |
| 07 | sage-speaking | Sage has a dialogue portrait when the scene uses a room view. |
| 08 | flute-practice; flute-listener; grounding-music-familiars | Later musical progress, Lyra portrait during her line; Nibble on the floor after support correction. |
| 09 | tree-of-echoes; grounding-echoes-familiars | Distinct old hollow tree; pets have clearing support and the children share the nearer plane. |
| 10 | pond; pond-rescue; pond-comfort | Rescue at the water edge and comfort on dry bank. Squatting Kael is farther back; his longer limbs, not crown height, establish his larger body. |
| 11 | soup-speaking | Arin portrait during dialogue, preserving home scene and speaker identity. |
| 12 | festival-arrival; festival | Populated plaza, consistent stairs/bridge/stage; held lantern after arrival. |
| 13 | cassia-storytelling | Cali and Cassia meet in populated courtyard, matching approved face/eye designs. |
| 14 | thalia-speaking; lyron-speaking | Cassia and Cali stay on scene; speaking parents get their own portraits. |
| 15 | grounding-first-joren; browser-meeting_joren | Native UI-hidden and full browser dialogue views confirm feet on the construction paving. Joren remains modestly taller and both faces are clear above the text. |
| 16 | soren-speaking | Soren portrait and early children in workshop, no adult/child stature reversal. |
| 17 | kaleb-speaking; grounding-kaleb-path | Kaleb portrait beside the early pair; feet are on the center path. |
| 18 | treehouse | Early pair occupies the room floor, preserving shared depth and door/window landmarks. |
| 19 | treehouse-rain; rain-speaking | Same sheltered room in rain; Cassia portrait identifies the speaking child. |
| 20 | older-children; cassia-older; waterwheel; grounding-waterwheel-familiars | Later age transition preserves peer relationship; wheel placement is in water and companions remain on dry support. |
| 21 | construction-room; grounding-expedition-path; grounding-construction-room | Tools and projected blueprint fit the scene. Corrected children and pets have actual floor/paving support. |
| 22 | browser-lyra_included | Final full-size browser view shows the established upper treehouse, ladder leading to its upper door and the separate lower hollow. Text fits below the structure. No native dialogue screenshot is claimed. |
| 23 | dome; dome-speaking; grounding-dome-path | Approach actors have paving support, then the vista remains unobscured and Cassia speaks through a portrait. |
| 24 | disagreement; familiars-disagreement; grounding-dispute-familiars | Both children stand on clear room boards, away from treasure chest/table; Shadow remains on the table as narrated. |
| 25 | the-news (native transition only); browser-loss | The native frame shows the dusk-home transition, without dialogue. Final browser text supplies the restored source bridge into the loss, clearly readable over that same home. Maia’s response is in scene 26. |
| 26 | grief-maia-response; family-grief; family-embrace | Maia and Cali in the same dusk home, changing to an embrace for that action without duplicate actors. Their response dialogue remains readable. |
| 27 | painting; familiars-painting | Brush/palette and shared map match the beat; familiar supports match the home. |
| 28 | cassia-grief; cassia-comfort; grounding-treehouse-grief | Peer stature and dimensional faces survive room lighting; handholding close-up supports the dialogue. |
| 29 | memorial | Same physical plaza as festival with believable quiet attendance. |
| 30 | mural | Mural and painting pose match remembrance; illustrated adventure is a drawing, not a newly occurring event. |
| 31 | remembering-in-rain | Same treehouse, with added messages/drawings and rain outside. |
| 32 | browser-annual_remembrance | The final full-size browser view preserves the populated plaza, stair, bridge and memorial stage under warmer light. The closing recollection fits in two lines before the hopeful afterword. No native scene screenshot is claimed. |

The native montage sheets in `test-results/native-visual/` are review aids, not shipped game assets. Normal dialogue leaves faces/gestures and the ten quick controls readable; the large-text and solid-background options are evaluated with the current interface. Glossary/People selection, chapter warnings, save/load empty and confirmation states, and keyboard focus belong to the separate usability report and functional suites. An action CG does not suppress a missing speaker: supporting voices such as Lyra, Sage, Kaleb and Cassia use the current appropriate portrait when they are not depicted in the frame.

Final browser scene sheets in `test-results/browser-visual/` were compared with the native views and approved source images. Scenes 15, 22, 25 and 32 were additionally inspected at their full 1280×720 capture size. No clipping, unexplained tint change, duplicate actor, unsupported placement or relative-stature reversal was found in these integrated views. Narrated room entrances sometimes use an establishing environment; subsequent off-frame dialogue uses the appropriate speaker portrait. The source image/pose approval and UI control tests remain separately recorded, rather than inferred from these reduced comparison sheets.

The final empty Glossary, first Constellation definition, expanded Lumen definition and scrolled song-credit page were also inspected at full browser size. Their headings, selected rows, definitions, Return/sidebar actions and link labels are readable and contained. The initial credit test failure came from an automated instantaneous move/click before Ren’Py updated hyperlink focus; an isolated real move/focus/click opened the correct URL. Only the test helper changed, followed by a complete successful browser rerun. No runtime or archive alteration was needed.

Evidence: `test-results/native-visual/reviewed-frames.json` identifies the 49 native capture bytes, `test-results/browser-visual/reviewed-frames.json` identifies all 32 final browser scene bytes, and the release receipts bind those captures, the twelve grounding frames, the current report and supporting UI views. Reviewed final browser ZIP SHA-256: `7b6df1432271365e4d562b419eb4027a0bf5f8c34f98aa60b8e08052badbd3c9`. This is a scene/frame inspection; real-time film viewing, physical-device audio listening and untested platforms are not claimed.
