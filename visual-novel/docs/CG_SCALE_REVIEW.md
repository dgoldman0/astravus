# Baked character scale and identity review — 0.1-alpha

All 20 selected CGs now have current cast/stage, face and reference reviews in [the character register](cg-character-review.json). The 17 revised or restored pictures also have independent composition, light, detail, anatomy and sharpness comparisons in [ART_REVIEW_CG.md](ART_REVIEW_CG.md); the other three have their separately recorded quality receipts. These are approvals of the inspected artwork, not a claim that remaining runtime, film or release checks have passed.

Sprite transforms cannot repair people already painted into a CG. Conversely, a changed head position does not establish a height error: supported pose, limb lengths, depth and crop matter. The final review rejected several technically plausible replacements because they damaged the stronger original composition, face or texture.

## Relative stature contract

These are **production drawing targets**, not new canonical measurements or exact ages. They preserve the same relative relationships within each childhood stage. Later childhood requires longer limbs and less infantile proportions; scaling the earliest drawing taller does not establish that growth.

The shared values live in [character_layout.json](../game/character_layout.json): early Cali/Cassia/Joren **675/680/710**, Kael **785**, Lyra **495**; later Cali/Cassia/Joren **750/755/790**. These are target visible sprite heights used to keep the same relationships in CG briefs, not measurements in the fictional world.

| Character | Reference stature within the same stage | Drawing instruction |
| --- | --- | --- |
| Cali | 1.00 | Baseline for the peer group. Keep her skull/face proportions, torso, hands and limbs consistent across poses. |
| Cassia | Approximately 1.00 (about 0.98–1.02) | A peer of comparable height, with her own slender build. Do not make her an older/taller adolescent beside a small Cali, or shrink her to Lyra's scale. |
| Joren | Approximately 1.05 (about 1.03–1.08) | Modestly taller than the girls. The difference belongs chiefly in torso/limb length, not a much larger head. |
| Kael | Approximately 1.16 in early family scenes | Clearly the older, taller sibling, with longer limbs and a larger frame than Cali or the peer trio. Keep that relationship when he crouches or kneels. |
| Lyra | Approximately 0.73 in the early sibling scenes | Distinctly smaller, with shorter arms, torso and legs. Her normal younger-child head proportions must not turn into a large body beside Cali. |
| Parents | Clearly adult relative to the children in that scene | Preserve adult torsos, hands and limb lengths. Selene remains a petite adult; white hair does not make her elderly. Do not force all adults into one identical height. |

For a directly comparable group, use one readable ground/seat plane and similar depth. Compare **skull-to-sole stature**, not hair volume or the top edge of a PNG. At the same depth, peer skull/face sizes should remain close; Joren should not acquire a giant head merely to make him taller.

For seated or leaning figures, inspect the supporting hip/seat position and the shoulder-to-hip, upper-arm/forearm and thigh/shin segments. A bent torso changes the crown's position, but it does not shorten every limb or change the character's age. Perspective is only a valid explanation when the floor, overlap and common props actually establish the required depth; it is not a blanket explanation for a changed size relationship.

## Final selected compositions

| Asset | Supported conclusion and final treatment |
| --- | --- |
| [Friends on the path](../game/images/cg/book-one/theme-path-friends.png) | The warm close trio and shared map are restored from the strongest earlier composition. A local complete-Calista scale correction makes her torso/arms comparable to Cassia's; Cassia leans forward and Joren is modestly larger. Feet remain cropped, so this is not a metric standing-height measurement. The rejected distant dark redraw is superseded. |
| [Treehouse arrival](../game/images/cg/book-one/theme-treehouse-arrival.png) | The welcoming close trio now occupies the canonical broad upper interior, with a real entrance and open bays. Calista's complete figure was scaled coherently; her nearer position and head tilt explain crown differences. Comparable peer torsos and Joren's modest size lead remain. Feet are cropped. The wide, dark room variant is rejected. |
| [Dome friends](../game/images/cg/book-one/theme-dome-friends.png) | The later-childhood girls have comparable stature on a readable floor plane. Joren's longer torso and legs give him a modest height lead without a larger head. The warm vista and pointing gesture remain. |
| [Friends at the table](../game/images/cg/book-one/treehouse-friends.png) | Calista has a comparable peer torso and limb scale at the nearer cushion. Supported hips and knees explain the seated head positions; Joren remains modestly larger. The close conversation, map and room detail survive. |
| [Pond recovery](../game/images/cg/book-one/pond-comfort.png) | The stronger HEAD painting is restored with only Calista iris pigment corrected. Kael squats deeply on his boots farther back; Calista kneels upright nearer the camera. His longer arms, larger hands and torso already establish the older sibling, and Lyra is distinctly smaller. A higher crown was not needed; the attempted redraw degraded Barkley's fur and Kael's face. |
| [Morning outlook](../game/images/cg/book-one/theme-morning-outlook.png) | Close hopeful Calista is in the foreground, with the full-sized upper room and lower refuge farther behind. The ladder is partly occluded by her body. She is not a same-plane scale ruler standing against the upper door or on its deck. This preserves character presence and the warm dawn composition instead of a tiny distant child. |
| [Waterwheel team](../game/images/cg/book-one/theme-waterwheel-team.png) | HEAD is restored byte for byte. Cassia leans forward with her chin supported on her palm; their other supported kneels differ. Comparable later-childhood torsos/limbs, the common wheel and visible bank explain the positions. The original downward attention, soft faces and tactile cloth/wood are stronger than the rejected regeneration. |

## Face, iris and stage review

Each final full frame was inspected with native face crops against the current stage sprites and the deliberately selected earlier painting. Checks include cheeks, jaw, nose, mouth, expression, eye openings, actual iris pigment, pupil, upper-lid shadow and catchlights. Lighting may warm or conceal pigment; closed or lowered lids do not need to be opened to demonstrate a color.

Calista and Joren have subdued blue pigment where exposed; Cassia has forest-green pigment. Kael retains gold/hazel and Lyra green. Nibble's frontal violet viewer-left and coral viewer-right eyes, broad white blaze and fluffy black/white coat are clear in the held-rat shot. Native inspection distinguishes Kael's blue-grey shaded sclera in the rescue from his tiny dark olive/gold iris, so his eye remains unchanged. The restored waterwheel painting's lowered lids mostly expose dark pupils, catchlights and shaded sclera; forcing more iris visibility would change the gaze.

The selected sketch/laughter face repair gives Cassia a natural amused smile with coherent cheek and jaw structure. The final path and arrival use the stronger close compositions rather than passing through the rejected distant facial reconstructions. Their identities and anatomy were inspected independently of stature.

Eleven CGs have author-authorized deterministic iris edits. [iris-retouches.json](iris-retouches.json) records source generation, exact source and output hashes, script hashes, masks and operations. Fresh source-to-installed checks and exact recipe reproductions confirm zero changes outside the support masks and zero changes to protected pupils/catchlights. Every other source face, body and scene pixel is preserved by those edits. This is separate from the quality judgment of the selected raw painting.

## Review maintenance

CG-01–18 retain their original findings as history, with current resolutions distinguishing successful corrections from superseded diagnoses or discarded variants. In particular, pond and waterwheel crown-only interpretations must not drive another regeneration. Any changed selected image, stage reference or shared stature contract invalidates its recorded signature and requires a fresh relevant review.

New artwork must pass both continuity and quality: keep purposeful character framing, expressive natural faces, dimensional midtones and painterly material detail while respecting physical layout, relative stage and identity. A matching color or nominal height cannot compensate for a worse painting.
