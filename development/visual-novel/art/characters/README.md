# Character key development records

The [selected production gallery](../../../../visual-novel/art/character-keys/index.html) contains the current sheets and concise character instructions. This directory preserves how those references were made: exact prompts, earlier candidates, immutable sprite inputs, generated paint, masks, editable XCFs, verification and integration records. These are production history and evidence, not canon articles or additional selectable game assets.

The organization pass moved this material out of the production-reference folder without changing its selection. Earlier full `KEY.md` and gallery README wording remains recoverable at commit `b8e7918` under `visual-novel/art/character-keys/`. The decision explanations below preserve the useful rationale removed from those working notes.

## Registers and related work

| Record | Scope |
| --- | --- |
| [Parent changes](parents-changes.json) | Five parent sheets, original sprite identities, Arin/Sage changes and native composition records |
| [Supporting changes](supporting-changes.json) | Kael, Lyra, Thalia, Lyron, Soren and Kaleb; selected and unselected generations; sprite decisions |
| [Trio and familiar changes](trio-familiars-changes.json) | Two childhood stages each for Calista, Cassia and Joren; Shadow, Barkley and Nibble; corrections and retained sprites |
| [Opening identity test](../opening-identity/README.md) | The accepted Arin/Sage direction, protected opening composition, editable repairs and actual Ren'Py comparisons |
| [Scene refinements](../character-refinements/README.md) | Propagation into the opening and Lyra illustrations, before/after viewer, source inspection and bounded native review |

Source snapshots and integration receipts retain the hashes and check counts from their respective steps. A historical source hash does not assert that a mutable production document still has those bytes. Selected-image records identify the intended current artwork; rejected candidates and raw donors are not substitutes for it. The built-in image tool did not expose its backend model version, so these records do not establish verified GPT-Image-2.5 access.

## Decisions retained from the key review

| Character | Decision and reason |
| --- | --- |
| Maia | Kept both home and gardening sprites: their face, amber-green eyes, dark curls, silver braids and activity-specific clothes already conformed. The key adds angles, restrained acting and lighting references. |
| Arin | Carried the accepted opening's pale freckles, blue eyes, angular face and close auburn crop into the everyday sprite. Native head and arm/hand masks preserve unrelated costume regions, lower body and feet. |
| Selene | Kept the bronze, violet-eyed, genetically white-haired adult and existing listening pose. Petite stature and white hair do not make her elderly. |
| Dorian | Kept the dark complexion, glasses, broad build and modest childhood-era silver. The notebook remains in his anatomical left hand through the key's front, side and rear views. |
| Sage | Replaced the formerly narrow face and upper-body construction with round cheeks, a softer neck, sandy sweep and medium build. Native masks preserve crossed hands, lower trousers and bare feet. |
| Calista | Corrected the early key's front body to face forward and its profile to show one eye. Kept all eight sprite variants; the later key preserves modest childhood maturation rather than adult proportions. |
| Cassia | Corrected the early front-body angle and replaced an overly geometric gold-moon wrist symbol with subtle irregular left-wrist pigmentation. Kept all three sprites and their previously approved umber facial midtones and softened lip boundary. |
| Joren | Kept all three sprites and added two childhood keys. The later sadness study represents living-child disappointment; it does not introduce an appearance after his death. |
| Kael | Kept the lean older-child sprite. The key adds angles and acting; undated mature injuries and bulk remain outside this childhood design. His anatomical-left dimple still requires care in close shots. |
| Lyra | Selected the second key with more natural eye proportions. Full-sprite and enlarged-face generated edits made insufficient geometric change and remained unselected. The selected sprite uses moderate native GIMP zero-whirl pinch in two feathered eye regions, retaining gaze, iris pigment, smile, feather and body; a stronger pinch trial was rejected. Scene faces retain separate fright, recovery and discovery performances. |
| Thalia | Kept face, hair, pose and costume; changed the irises to source-required deep green with native GIMP hue/lightness/saturation through bounded masks. Central pupils and catchlights were excluded. |
| Lyron | The first key over-preserved a contemporary denim-shirt, belt and cargo-trouser combination. The author's correction led to the selected blue-gray overlapping garment, plain trousers and woven shoes. The author clarified that the wardrobe issue mainly concerned Lyron, so other outfits remained selected. The exact cut is a production interpretation, not a Lumen uniform or a new clothing technology. Earlier sheet and face-only donor remain unselected. |
| Soren | Kept the focused face, cropped hair and practical work outfit; the key adds angles and a restrained emotional range. A neutral empty-hand pose does not enact tool use. |
| Kaleb | Kept the angular weathered face, gray-streaked brown hair, golden-brown eyes and travel layers; the key adds warmer and grieving expressions without making one performance universal. |
| Shadow | Restored the omitted anatomical-left ear notch in the upper standing side view. Kept the original sprite, sleek black/green identity and single crooked-tip tail. |
| Barkley | Kept the retriever sprite without a corrective generation. Standing and rear studies continue the honey-gold coat and ordinary canine anatomy without new marks or equipment. |
| Nibble | Corrected two left-facing profiles from violet to coral, fixed the side label and removed an invented dark rump patch. The anatomical-right eye remains violet and anatomical-left coral; rear haunches remain white. The selected sprite retains the author attachment's fluffy rat design because the original attachment had no local path. |

Generated side/back surfaces are practical constructions, not measured 3D geometry or new canon. Some standing views retain a relaxed slight turn. The parent sheets returned at 1536 × 1024 despite a larger requested size; no artificial upscaling was applied. Individual sheets fill their own pages, so page height is not a relative-stature measurement.

The original gallery review opened all twenty sheets in local Chromium with external network requests blocked. Stage comparison, zoom/reset, deep-link reload and the mobile selector passed, with no JavaScript errors or page overflow; desktop and mobile layouts were inspected. That historical viewer check does not by itself validate later link migrations, the game runtime or every artistic detail. Current migrations and rebuilds require their own scoped checks.
