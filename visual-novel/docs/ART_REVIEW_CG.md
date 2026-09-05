# Final CG image-quality review — 0.1-alpha

Reviewer: `art_sprite_review`. Scope: the 17 revised/restored CGs below. The other three CGs have their separate root reviews. This report records inspection of the final installed bytes, not approval inherited from a generation batch.

For each picture, the complete final frame was compared with its deliberately selected earlier Git painting, and native-resolution face details were checked against current character references. The earlier painting is the composition/detail comparison, not blanket authority for eye hue, architecture or anatomy. All seven dimensions were reviewed: focal presence, tonal depth, material texture, facial anatomy/expression, identity/stage, native resolution/sharpness, and regression from the edit. Exact standing-height claims are limited by pose, support, depth and cropping.

The current stage references retain their existing bodies, facial structure and silhouettes. The four selected Calista sprite changes are bounded iris retouches; their outside pixels and silhouettes were verified separately. Their corrected blue pigment, current wiki identities and unchanged stage bodies are the references used here.

No review images or duplicate before/after PNGs are added to the game. Temporary inspection crops and comparison sheets were used in `/tmp/alpha-final-cg-review`; the durable findings and immutable comparison IDs are below.

## Per-image result

Each entry passed after the final installed full frame and native faces were inspected.

### cassia-storytelling

The close seated circle, open sketchbook and engaged listeners retain the earlier composition. Warm cheek midtones, curls, woven clothing and stone detail remain clear at native size. Calista and Cassia have comparable supported torsos; Cassia keeps her natural profile and shaded dark green iris. Calista now has subdued blue pigment; face shape, expression and all other painted detail survive the narrow correction.

Comparison: `git:7a27af1382cd53534b41b70015f7f8066d21336f`. Final SHA-256: `74608e12c38015c5129b3c08db5af53d267d4e35b473857acf2d398d85ac3503`. Canvas: 1672 × 941.
Selected raw generation: `alpha-cassia-storytelling`; source SHA-256 `e9f74f119e91cbb130e342a1c9e3cb90d8dd6c178dce958a6d6c4b33c11e37cd`. Recipe: `alpha-cassia-storytelling-masked-irises` in [iris-retouches.json](iris-retouches.json).

### flute-playing

The intimate lesson, supported bench pose and hand/flute relationship retain the earlier framing. Candle warmth and soft dimensional skin remain; hair strands, clothing folds and room instruments retain native detail. Calista has a natural young face with blue pigment beneath the original lids; Selene remains a petite adult with lowered lids. The iris correction leaves the complete composition and texture unchanged outside the mask.

Comparison: `git:37b7d3f6597004978668cab2116b698246605649`. Final SHA-256: `8f44a837334af47ec5081cd04a4ab65087faca327fb278127ea3062214d109c1`. Canvas: 1672 × 941.
Selected raw generation: `alpha-flute-playing`; source SHA-256 `16eb9b846c72f31402bcd83c2e7885ad05f297b86b456a3d2f50a606371c7c23`. Recipe: `alpha-flute-playing-masked-irises` in [iris-retouches.json](iris-retouches.json).

### flute-rest

The pause in the same lesson retains the lowered flute, Calista's upward glance and Selene's reassuring pose. Warm midtones, lips, cheeks, delicate white hair and cloth retain the earlier detail and sharpness. Calista's blue pigment is subdued with the original pupil and catchlight; Selene's lowered eyes remain untouched. The companion scene's bodies and room have not drifted.

Comparison: `git:595bb47ef8188cc71671358205c4b4995fda5973`. Final SHA-256: `7554e2418496049f96c44d83b65460e9cc79a038f902ff2639ab6648215ae521`. Canvas: 1672 × 941.
Selected raw generation: `alpha-flute-rest`; source SHA-256 `e16e5ba61f12a3548d34f3ecd1540127fcac689115d652bb93b2ba466e07beed`. Recipe: `alpha-flute-rest-masked-irises` in [iris-retouches.json](iris-retouches.json).

### garden-compromise

The shared row of pots and three-way conversation remain the focus. The blue flowers make Calista's handled pot readable without changing the shot's depth or character presence. Warm dimensional faces, individual braids/curls, soil, pottery and leaves retain native detail. Maia reads as an adult and Kael has longer reach/larger torso than Calista despite their kneels; blue, hazel/gold and amber-dark eye readings are coherent.

Comparison: `git:7350e889f6d170bd36596868b2fd21eeecb034b5`. Final SHA-256: `d0416d9d112d712dacf13cd4ec13649d9c16931c585f2554f0d7e389bba126bc`. Canvas: 1672 × 941.

### pond-rescue

The reaching diagonal from the dry bank to Lyra remains clear, with Barkley and the black cat framing the rescue. Native face, fur, water and cloth detail retain the earlier texture and warm depth. Calista's pigment is corrected to blue without changing expression. Kael's tiny dark olive/gold iris is preserved: the blue-grey patch beside it is shaded sclera, not iris. Lyra has green eyes and a much smaller frame.

Comparison: `git:51cd3c86a43145a35a907d30443a62f03299128a`. Final SHA-256: `0de515348590fbc8aff39736ad072e1c1c07d7ccb967fdd847dd5e4a75f009fb`. Canvas: 1672 × 941.
Selected raw generation: `alpha-pond-rescue`; source SHA-256 `4f07d7f2ebc3693447afb08b19652adcb1965b93bfd02f1e409002b24b5f99cb`. Recipe: `alpha-pond-rescue-masked-irises` in [iris-retouches.json](iris-retouches.json).

### pond-comfort

The stronger HEAD painting is restored, with only 97 Calista iris pixels changed. The close protective embrace, delicate Barkley fur, softer foliage/ground strokes and natural narrower Kael eyelids all survive. The rejected scale/face variants hardened fur and facial detail. Kael squats deeply on his boots farther back while Calista kneels upright nearer the camera; his longer arms, larger hands and torso establish the older brother without forcing a higher crown. Calista blue, Kael hazel and Lyra green remain naturally shaded.

Comparison: `git:c0f7f367ac993698f56d099e09d4d6dd8d254f28`. Final SHA-256: `56074675442f5eee3db5506e1a0816d2fc52e385bdbc175518612d9a34fc6f43`. Canvas: 1672 × 941.
Selected raw generation: `review-027-pond-comfort`; source SHA-256 `55ee6da13f6da16add60ed3bb23488a937d334aba86bb55ec0caf9f4c899e88b`. Recipe: `alpha-pond-comfort-masked-irises` in [iris-retouches.json](iris-retouches.json).

### theme-dome-friends

The trio, pointing gesture and broad warm dome vista retain the earlier focal relationship. Corrected supported feet and longer Joren torso/legs give him a modest height lead while Calista/Cassia stay comparable later-childhood peers. Faces retain coherent cheek/nose/mouth shape, and vest/jacket textures, masonry and foliage remain detailed rather than blurred. Blue/forest-green/blue pigment is subdued; occluded iris areas and shaded scleral whites remain unchanged.

Comparison: `git:20b90b19832a4d68968f8cf80c3333a459e013db`. Final SHA-256: `9ee19cb65c68b41d5e03f3c6cf40d6fe617c6d0db3abe7ce6774a7e0da3611c1`. Canvas: 1672 × 941.
Selected raw generation: `alpha-scale-theme-dome-friends`; source SHA-256 `e0cf5f5eb62053d2efd8994c00d1cc87469e834e830b924fbb29583499746350`. Recipe: `alpha-theme-dome-friends-masked-irises` in [iris-retouches.json](iris-retouches.json).

### theme-evening-reading

The intimate seated drawing pose, notebook and lamplight retain the earlier focal presence. Warm face midtones, fine curls, embroidered sleeves, cushion and table grain retain detail and sharpness. Calista's lowered blue eyes and small quiet smile remain naturally modeled; no whole-face repaint was needed. The one-human crop supports stage/pose review, not standing-height measurement.

Comparison: `git:6e130f2d1dd06bbd20cb843c0cd79ea3512000d6`. Final SHA-256: `3600e695c1bddaf867faa04d5f157faf323012e269626fcce8fa5aab247627fc`. Canvas: 1672 × 941.

### theme-garden-opening

The opening retains both children close among the sunflowers and Kael's explanatory pointing gesture. Calista's eyes are less round and exaggerated than the earlier opening, with restrained slate-blue pigment and dimensional freckled cheeks. Kael remains recognizably older with hazel/gold eyes and a larger shoulder/arm frame. Warm light, fabric, hair and flower detail remain clear without introducing a flat dark face or losing the story's welcome.

Comparison: `git:5f9d8cababad8282526b9d0993128bd40386c092`. Final SHA-256: `cc409a5fd4996cf8839252c402efda8ef611da9670e82426e2611b07ba531c51`. Canvas: 1672 × 941.

### theme-insect-discovery

The leaf/insect and shared close curiosity retain their earlier focus. Calista's subdued blue eyes and Lyra's green eyes have preserved dark pupils and naturally shaded lids. The younger sister's rounder face and shorter arms remain distinct; both retain coherent noses, mouths and fingers. Soft warm cheek light, detailed curls, sleeves and leaf textures survive without a wider or emptier recrop.

Comparison: `git:d0c724135db07d1adeb9dfef81812647fe092da9`. Final SHA-256: `e8171081255755b34c4457269f78cc2caf92032b495121029b84d77a596412e8`. Canvas: 1672 × 941.

### theme-morning-outlook

The final shot restores the earlier close hopeful Calista, warm dawn shafts and clear freckled face, instead of the rejected distant dark figure. Fine curls, clothing, notebook and luminous foliage retain tactile detail and native sharpness. The broad upper room and lower refuge sit farther behind her, with the ladder partly occluded by her foreground body; this is not a miniature room scaled against a child on its deck. Blue iris pigment alone changes in the selected raw painting. The crop does not expose her feet, so no metric standing-height claim is made.

Comparison: `git:8013c8dba8d9a830293506480cbd046cd4036d52`. Final SHA-256: `61382b336aeb7c7989e7339855dbf89337e0f9c29ab5a90cbd04bb25b147834f`. Canvas: 1680 × 936.
Selected raw generation: `alpha-theme-morning-quality`; source SHA-256 `c124f0469f89d7889a7645575f08ff7f37c0b91d2fb71da3b50ad1d8382efc01`. Recipe: `alpha-theme-morning-outlook-masked-irises` in [iris-retouches.json](iris-retouches.json).

### theme-nibble-moment

The close held-rat composition retains Calista's tender downward gaze, hand support and warm facial depth. Nibble now faces us with a clear black hood, broad white blaze, fluffy white body, pink ears and violet viewer-left/coral viewer-right irises. Native fur, whiskers, fingers, curls and cloth remain detailed; the stronger markings do not erase the painterly softness. Calista's mostly lowered eyes do not need invented exposed color.

Comparison: `git:dc8b366ee538b9a13081290899959c0019c29e1a`. Final SHA-256: `c20617d52737079f8d91da956b3b0aa7c958cf87577696f32bb691c4576b1fb5`. Canvas: 1672 × 941.

### theme-path-friends

The strongest earlier warm close trio/map composition is retained, replacing the rejected dark distant full-body redraw. Calista's complete figure is locally larger so her torso/arms read as Cassia's peer; Cassia's forward lean and Joren's modest larger frame remain plausible. Faces, hair strands, textile pattern, map linework and nearby rail detail retain their close narrative presence and sharpness. Cassia has a natural smile and forest-green pigment; Calista/Joren have subdued blue with original pupils and lids. This is a planted Lumen walkway, not a newly invented Maia-garden layout.

Comparison: `git:986f6de9d6a8cb3505ece59cca85b2e417424879`. Final SHA-256: `1fbaeeac453d40ad6761894b68b6955a332942fa29b02ae2be93934fbabde2f5`. Canvas: 1672 × 941.
Selected raw generation: `alpha-path-close-stature`; source SHA-256 `08ade5a93c7c5d9128eb4927876b4dd6744205c375f51e318a30972e6df4b029`. Recipe: `alpha-theme-path-friends-masked-irises` in [iris-retouches.json](iris-retouches.json).

### theme-sketch-laughter

The shared comical drawing and three close faces retain the earlier warm lively framing. Cassia's stretched open mouth/pinched chin is replaced by a natural smiling mouth and coherent cheek/jaw structure while preserving amusement. Calista and Joren retain their expressions; all three have subdued blue/green/blue iris pigment. Fine curls, fabric, fingers, drawing lines and table objects retain native clarity and modeled light. The face crop cannot certify standing height.

Comparison: `git:f21752c8330630a43dab772a5fb095930e3d927e`. Final SHA-256: `834fd2c8430fe29da8d504b36170d417e3a7bfff710d014b4a2e6229ae7d73d8`. Canvas: 1672 × 941.
Selected raw generation: `alpha-face-theme-sketch-laughter`; source SHA-256 `c7f7a278808705c3197c43aa8ce8d1657374b177d85b5690e31982caca27faa1`. Recipe: `alpha-theme-sketch-laughter-masked-irises` in [iris-retouches.json](iris-retouches.json).

### theme-treehouse-arrival

The final composition retains the earlier close welcoming trio and rich warm material detail, while replacing the trunk-cupboard room with the broad canonical upper interior. The real left entrance, right open bays and map table fit the established room. Calista's complete figure was scaled coherently; her nearby folded arms/notebook and tilted face remain natural, with Cassia a comparable peer and Joren modestly larger. Native freckle/cheek/lip modeling, curls, cloth and timber retain detail. Calista's existing blue eyes stay untouched; only Cassia forest-green and Joren blue pigment are masked. Feet are outside the crop, preventing a metric height assertion.

Comparison: `git:7ed1d8c4334a56df205fd3157081478564e0b4dc`. Final SHA-256: `7525e3f19fab329fb96b0ed6d1ac6c1aa06db608b8197ad8d7b83fbd3c5554a6`. Canvas: 1672 × 941.
Selected raw generation: `alpha-theme-arrival-quality`; source SHA-256 `89a62789ffce10142e47e21a932865d5158a3ee838fd47e5ef66db784dbcc499`. Recipe: `alpha-theme-treehouse-arrival-masked-irises` in [iris-retouches.json](iris-retouches.json).

### theme-waterwheel-team

HEAD is restored byte for byte because it is the stronger painting. The children's attention stays on the wheel; soft dimensional faces, fine clothing/wood texture and warm bank detail avoid the rejected variant's hard synthetic strokes and redirected gaze. Cassia leans forward with chin on palm, accounting for a lower crown without changing peer maturity; supported hips, bent limbs and shared wheel establish depth. Original narrow lowered lids expose mostly dark pupils, catchlights and shaded sclera, with no conspicuous contradictory pigment. No eyes were opened or recolored to force visibility.

Comparison: `git:741bb14fa76dd4501d4adb18bafd1ad547194e07`. Final SHA-256: `4fe77c4bc926b67f973e582646b11f212a22e29210f924e0faf11c6d85290d60`. Canvas: 1672 × 941.

### treehouse-friends

The intimate tabletop conversation, map and bright open room retain their earlier framing and material detail. Calista's fuller peer-scale seated torso/limbs avoid the former much-smaller near-seat child, accounting for cushion/hip support. Cassia remains her peer and Joren modestly larger; expressions and gestures stay engaging. Warm face midtones, curls, patterned clothing, cushions and timber remain crisp at native size. Calista blue and Cassia forest-green pigment are bounded corrections; Joren's subdued profile blue remains untouched.

Comparison: `git:b33962669b1b652b97a509612dbd8ef64d409c84`. Final SHA-256: `5bf094774526bf79a5ffd6bdd7b9e1cf2b07c74a8dd0c42778b3b43a2892f318`. Canvas: 1672 × 941.
Selected raw generation: `alpha-scale-treehouse-friends`; source SHA-256 `219eb76ae15c5b171e7a204827c53ae9705a7e95d1bbbca03ddcc7674e8d3058`. Recipe: `alpha-treehouse-friends-masked-irises` in [iris-retouches.json](iris-retouches.json).

## Exact iris protection checks

Freshly compared each installed corrected CG against the exact selected source and the saved support mask, then reproduced it from the installed recipe and script. All 11 outputs reproduce byte for byte. Every image retains its source mode and canvas; every outside-mask pixel and each protected pupil/catchlight pixel is equal. The masks leave sclera and eyelids outside their pigment support. A zero difference is a protection proof, not the artistic approval above.

| CG | Changed pigment pixels | Outside-mask changes | Protected changes | Exact reproduction |
| --- | ---: | ---: | ---: | --- |
| cassia-storytelling | 31 | 0 | 0 | Yes |
| flute-playing | 90 | 0 | 0 | Yes |
| flute-rest | 54 | 0 | 0 | Yes |
| pond-comfort | 97 | 0 | 0 | Yes |
| pond-rescue | 63 | 0 | 0 | Yes |
| theme-dome-friends | 81 | 0 | 0 | Yes |
| theme-morning-outlook | 64 | 0 | 0 | Yes |
| theme-path-friends | 207 | 0 | 0 | Yes |
| theme-sketch-laughter | 507 | 0 | 0 | Yes |
| theme-treehouse-arrival | 123 | 0 | 0 | Yes |
| treehouse-friends | 117 | 0 | 0 | Yes |

Waterwheel is exactly equal to its selected HEAD blob and has no iris retouch. Pond comfort is equal to its HEAD painting outside the 97 Calista iris pixels. These restorations preserve the better original fur, facial modeling, gaze and material texture; lower crowns caused by a supported crouch or lean are not defects to repaint.

The CG character register binds current cast/stage/reference signatures as well as each inspected image hash. The release matrix records these independent per-image quality results separately from geometry, provenance, runtime and audio checks.
