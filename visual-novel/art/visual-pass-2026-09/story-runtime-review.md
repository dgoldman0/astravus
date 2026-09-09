# Native story and People review — 2026-09-08

No blocking visual regression was found in the 62 captures individually inspected for this review. Character identity, early/later childhood staging, grief presentation, and dialogue/menu readability remain coherent at the captured 1738 × 977 window size. Two retained familiar-compositing limitations are recorded below.

The captures come from `chapter_playthrough` in [game/testcases.rpy](../../game/testcases.rpy), beginning at line 96. They were refreshed on September 8 at 22:54:37–22:55:54 EDT (September 9, 02:54:37–02:55:54 UTC). The [run log](chapter-playthrough.log) reports 156/156 assertions passed under Ren’Py 8.5.3.26051504. That functional result is separate from the visual observations here.

## Observations

- **Early childhood and supporting people:** `garden`, `siblings-garden`, and `garden-compromise` keep Cali smaller than Maia and Kael, with Kael still a lean child. Cali’s chestnut hair, freckles and blue eyes remain recognizable between standing art and the garden/music CGs. The flute playing/rest changes are clear, with no duplicate portrait over the seated Cali/Selene composition. `flute-listener` and `festival-arrival` preserve Lyra’s golden curls, upward green-eyed gaze and much smaller stature; no obvious seam from the bounded eye adjustment is visible at this size. `library`, `soup-speaking`, `soren-speaking`, and `kaleb-speaking` show distinct Dorian, Arin, Soren and Kaleb identities. Portraits stay clear of dialogue text.
- **Stage and activity continuity:** `festival-arrival` has empty hands before the held lantern in `festival`. `treehouse` and `rain-speaking` use young Cassia/Joren; `older-children`, `cassia-older`, and `dome-speaking` show longer proportions and later outfits while retaining their faces and characteristic colors. The frustrated expressions in `disagreement` replace the earlier cheerful poses. No misplaced standing child appears in the pond establishing view or the rainy treehouse narration view.
- **Grief and remembrance:** `the-news` is a dark, empty home pause. `grief-maia-response`, `family-embrace`, `grief-embrace`, and `cassia-grief` use restrained, distressed or compassionate expressions, with appropriate subdued light. The embrace CG has no duplicate standing figures or extra speaker portrait. Painting and mural views restore some warmth without a celebratory expression. No living Joren sprite or dialogue portrait appears in the reviewed post-loss views; the mural depicts remembered adventure, and People switches to remembrance text. Memorial and renewed-rain backgrounds preserve the emotional change in familiar locations.
- **People and interface:** all 11 reviewed People captures have readable labels, selected entries and unclipped text. The three familiar illustrations match their scene identities, including Nibble’s contrasting eye colors. The human People entries, including Lyron, are text-only; those views do not verify human portraits. Lumen and Joren text changes are visible at the intended checkpoints. Title, spoiler dialog, save/load, history, settings, large-text, afterword, end, credits, resumed end and chapter-grid captures have no obvious overlap or clipping. `large-text` only demonstrates the short “Here, Cali.” line. Save/load thumbnails include older saved images; they are not evidence of the current selected art.

## Residual limits

- Barkley’s bright warm coat and frontal source lighting stand out against the cool forest in `tree-of-echoes`; weak contact shadow makes the cutout more apparent. The home/painting versions fit their warmer setting better. This is retained familiar art/compositing, not introduced by the character refinements.
- In `construction-room`, the lower dialogue gradient dims most of Shadow and Nibble and Barkley’s lower body. Their placement is on the foreground floor, but the smallest familiar has low contrast. This is a retained placement/readability limitation, not an identity failure. The familiar PNGs and `game/familiars.rpy` are unchanged relative to HEAD at review time.

This review covers the named static checkpoints below, not every dialogue line, intermediate transition, animation, audio cue, save slot or display size. Reduced motion was enabled by the suite. Exact iris color and fine matte edges are harder to judge in small dialogue portraits. No art or runtime files were changed for this review.

The 11 captures assigned to the root reviewer are excluded: `first-memory`, `workshop`, `sage-speaking`, `lyron-speaking`, `thalia-speaking`, `pond-rescue`, `pond-comfort`, `family-grief`, `cassia-comfort`, `waterwheel`, `dome`. The separately assigned `theme-art-00` through `theme-art-14` are also outside this report.

## Inspected capture hashes

Paths below are relative to `test-results/screenshots/`. These are SHA-256 hashes of the actual PNGs inspected, in suite order.

| Capture | SHA-256 |
| --- | --- |
| [title.png](../../test-results/screenshots/title.png) | `10008b5941fe2f5a6c6b33bcc0e25de9433f8e20edcf65a770870372ebe36a78` |
| [chapter-spoiler-warning.png](../../test-results/screenshots/chapter-spoiler-warning.png) | `9132e5b846a9e65f12c49bdb4328e097d1ca0dd104291fef92493780622595d4` |
| [people-before-reveal.png](../../test-results/screenshots/people-before-reveal.png) | `7f479e6ea391df18e742004ac1cbfad43ba11be8b0bf624e7b4ac7d0630f1f9d` |
| [family-home.png](../../test-results/screenshots/family-home.png) | `9194b78be8e19d18bee6f5caad5cb65278a426a852c746efaa80644c21eb3ba1` |
| [familiars-home.png](../../test-results/screenshots/familiars-home.png) | `3184c453f4df498432bf552788420393ddc597926253b4b2a9141150be8ecd20` |
| [people-shadow.png](../../test-results/screenshots/people-shadow.png) | `2413ff51e8c4ecd8662cd70c8af4bae86731dc302123aaa9981aa8a00dcc3251` |
| [people-barkley.png](../../test-results/screenshots/people-barkley.png) | `9dc83d28688aaf142ef3860328505f9f739bb3964b7fe8d364a225a138721c2d` |
| [people-nibble.png](../../test-results/screenshots/people-nibble.png) | `359e4ddc45d6e9e704f1ae85978719931ec6e6da47cd3da87626484a94e75857` |
| [garden.png](../../test-results/screenshots/garden.png) | `24426a810d8dd9280b2f8cfc84c038a41357f2e3a80abac4d2aca63d3e859c0e` |
| [people-maia.png](../../test-results/screenshots/people-maia.png) | `0aed23221a284a07efb1d35baf4176745847e200cf0bbb338cd38442d80b4fee` |
| [load-before-automatic.png](../../test-results/screenshots/load-before-automatic.png) | `cb0188cbb616498e55341481d8db565d9692cc7e6425c7ae46770a3e0ee838e8` |
| [save-from-automatic.png](../../test-results/screenshots/save-from-automatic.png) | `38f30243100b7a1b99c728882d268462bd815a832da3695651a78e38c7a31c86` |
| [history.png](../../test-results/screenshots/history.png) | `0206acd02465837217f0767a73905be569983cbe67576bf17affa35cc60c4640` |
| [settings.png](../../test-results/screenshots/settings.png) | `040dff0d9b4cfc3c6cddf2ba2f37396592e325cab73f4c1b0b3e6355a7e20b5a` |
| [large-text.png](../../test-results/screenshots/large-text.png) | `f8c3b10f77b547c8b427de25827587fcec138c4fe57dd5cbf191db310d95b4d6` |
| [siblings-garden.png](../../test-results/screenshots/siblings-garden.png) | `299a2229e03a8ceab4e5c48a534baaca67b2580bdfd204c81c2eabced07091b2` |
| [garden-compromise.png](../../test-results/screenshots/garden-compromise.png) | `d4782b6fc09eb53643da9efa8818ee92445b0e88bbaf2a32f9c4bd2e46c5a6b1` |
| [first-melody.png](../../test-results/screenshots/first-melody.png) | `5db9b93e63de3b82b0a1acea57757708d19dd799b4b99058e5135fc397adc5c2` |
| [flute-rest.png](../../test-results/screenshots/flute-rest.png) | `a741855b7a082e551870fb551542e1e96d3ee86e3d59cf45a37967379b77d489` |
| [people-selene.png](../../test-results/screenshots/people-selene.png) | `2a1ea7565f8d0fa1444a0dc4c842d6383cb5cdb805296acb811edebe4e50e4e8` |
| [first-flute-phrase.png](../../test-results/screenshots/first-flute-phrase.png) | `09118f8c60fd5a25bbe33bb58f291e557e9c7bb5699cda163647df5c5825649a` |
| [library.png](../../test-results/screenshots/library.png) | `53fe17570aa99f267bd87c45e040a603a7a0dcf15cf493a57350cabf2811addd` |
| [sage-story.png](../../test-results/screenshots/sage-story.png) | `3d9aacc23fd16fb2a8cb71c71eab4db692d8393ef4ce4e672fb7a1ceb50a1614` |
| [flute-practice.png](../../test-results/screenshots/flute-practice.png) | `e723ac649d4474e88442580bac75e8048909e3034be658d0e9ad7db9281459e4` |
| [flute-listener.png](../../test-results/screenshots/flute-listener.png) | `91742a66eb0e433a2b1008336b8a9509329c9047cd464638e329af10506f9c94` |
| [people-after-reveal.png](../../test-results/screenshots/people-after-reveal.png) | `bcc8369e70b4d86b7b0f431ae765889c5570e1bffe6554b517a11e8be5dbc716` |
| [tree-of-echoes.png](../../test-results/screenshots/tree-of-echoes.png) | `d21ba9d192f0c14e58bbafdc8d7af3cf49db30ae2dbc7b5c5e199bb33301357b` |
| [pond.png](../../test-results/screenshots/pond.png) | `49dbe058829784357ad6c5d8891223bda442a8118f9f00907d270807adb68cc9` |
| [soup-speaking.png](../../test-results/screenshots/soup-speaking.png) | `f9dec07fcc00ddfd10f3efcb19949566cfd538188dfc07df17ce701f1aed6f23` |
| [festival-arrival.png](../../test-results/screenshots/festival-arrival.png) | `0e7a47470d7f28f9f4cc0d1f9279e282dc5febf6ea7a7c53e1c3939cd86f7a57` |
| [festival.png](../../test-results/screenshots/festival.png) | `2f33138736f31c0f19345ee72976c913dbff7a6256e1b2004ff0b8f0a17797dc` |
| [people-first-cassia-line.png](../../test-results/screenshots/people-first-cassia-line.png) | `adae6905e2e4addd27ad787df294d1ca6cad0b0bb2ba468788d53eddbaf19d8d` |
| [cassia-storytelling.png](../../test-results/screenshots/cassia-storytelling.png) | `5f4703ede7cba6562cdd46efadb90d0beecfb379320ecf5e414b9ef8ef747418` |
| [people-lyron.png](../../test-results/screenshots/people-lyron.png) | `6a62c0e941a82bdd6f2d355a1aabab5b0019f3fc0e6e2a8fcd50114ed0a70934` |
| [people-friends.png](../../test-results/screenshots/people-friends.png) | `4ee2642c97836f91b78e4b967140997019a26290b033fd776d80117d7361865e` |
| [soren-speaking.png](../../test-results/screenshots/soren-speaking.png) | `9ed88c70b5407adb49acf17572027a595545c3a56f9b035d40b2b95617d7c396` |
| [kaleb-speaking.png](../../test-results/screenshots/kaleb-speaking.png) | `d236b4e8d15d05032445d4e57adb793255bac6e354994bbfe31480522cb988b6` |
| [treehouse.png](../../test-results/screenshots/treehouse.png) | `179ef21dd14154852c6a49e3e318655955ee340312f7ec8cfa8b8c2f50de2835` |
| [treehouse-rain.png](../../test-results/screenshots/treehouse-rain.png) | `ca4ee2aec67598ce4349e1114724561af70e5be3617011528c3c81089828b137` |
| [rain-speaking.png](../../test-results/screenshots/rain-speaking.png) | `c6e35577b99be069bcef4d6a02ab4e3532150459ccac353f9b97d4025cfbb9f2` |
| [older-children.png](../../test-results/screenshots/older-children.png) | `bc22bd2850f78cf8a63cced3b4876329bd6be7043b1c0bdd0d7fc204742b0009` |
| [cassia-older.png](../../test-results/screenshots/cassia-older.png) | `a6c4ae6eb390c57c25d470eb6937332d26f391ecd7496e21e1ae5c9677bb23fd` |
| [construction-room.png](../../test-results/screenshots/construction-room.png) | `cb8bda6bde0d4f6f9bb43f04a7ae50a098136827f567c2cfad111f0bf2312742` |
| [dome-speaking.png](../../test-results/screenshots/dome-speaking.png) | `ab5b4834369d3af437b91cd188a5e9e19392f86e26fe5427a23e1c5491b51a2d` |
| [disagreement.png](../../test-results/screenshots/disagreement.png) | `07e498c9e04c2b89d3137a1ab853aa5c8fee575bd77676fa1ad1aee487906321` |
| [familiars-disagreement.png](../../test-results/screenshots/familiars-disagreement.png) | `c48dc4c194c666b837bd8ee631ceb2244ae81df4bdcd78ea28b72ad022efbba2` |
| [the-news.png](../../test-results/screenshots/the-news.png) | `15efb5fc4a550bb863da6317184eb7abcff87c70697f162cae35f31a4b368ab3` |
| [people-remembrance.png](../../test-results/screenshots/people-remembrance.png) | `acafc7d535c02abcf954f7f0e88642eb989d73fa8d318b6c4724b453c75b6fbb` |
| [family-embrace.png](../../test-results/screenshots/family-embrace.png) | `8c44cebb775e40fdbea91738f384f9d270541e0890ae105be0e2d3afd818ff30` |
| [painting.png](../../test-results/screenshots/painting.png) | `97dd393aada25ba8cbd74d51e6c8ff30015c6edd0d86d7948f71ab150f13da03` |
| [familiars-painting.png](../../test-results/screenshots/familiars-painting.png) | `a9c57887f03963c53826fd60a29a2c83816f1c618efac656d8ad2e051d62f5f0` |
| [cassia-grief.png](../../test-results/screenshots/cassia-grief.png) | `f4b1133f971f2b4f3f261833d52377f1c7025cf548d6b62ce227286a05090d1b` |
| [memorial.png](../../test-results/screenshots/memorial.png) | `1bcf510ff8018adbacb8a98cfdb01e48a4bd2321fafd7389f0bf0cdb206621fe` |
| [mural.png](../../test-results/screenshots/mural.png) | `6b8bb246b746cea9524a2828be110b86f5aaf0918310284da55fd5a4505695e7` |
| [remembering-in-rain.png](../../test-results/screenshots/remembering-in-rain.png) | `377e235224e101355d66cceb22fcf2d4f55f71719bdca92c1e1eaf0b81c76090` |
| [afterword.png](../../test-results/screenshots/afterword.png) | `4a22bd437a61aa68d69053174c6550495faff6362357743a4d7373907bb2a979` |
| [end.png](../../test-results/screenshots/end.png) | `774e6ae09b5794a9b41d788e77258a37f462ad8d631f4377d065dbdbf8c20af6` |
| [credits.png](../../test-results/screenshots/credits.png) | `a53b2687b5986fa1922c4b770caf101945e2c3ff9d7fe182bfae3ca5800d7341` |
| [resumed.png](../../test-results/screenshots/resumed.png) | `774e6ae09b5794a9b41d788e77258a37f462ad8d631f4377d065dbdbf8c20af6` |
| [dev-chapters.png](../../test-results/screenshots/dev-chapters.png) | `9603156af3f956ab98019a4584721c645b75910320b6396a803aedefadcda9e0` |
| [grief-maia-response.png](../../test-results/screenshots/grief-maia-response.png) | `4e02418db2107cd2c844e8c7b9bcdc6bb5433aca678db40b45b1c5bfc7732cb7` |
| [grief-embrace.png](../../test-results/screenshots/grief-embrace.png) | `2dd507be85e96bb95a98e74a4d896033d59f64ef1fae52126a04647468c76c82` |
