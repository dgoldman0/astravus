# Production background, familiar and staged-sprite audit

Reviewed independently on 2026-09-05 by `glossary_story`. This complements [the 20-CG audit](graphics-cg-audit.md); no old PASS status was adopted. The scope here is **23 non-treehouse backgrounds, all 3 familiar source sprites, and 8 staged character edits**. The 3 interior treehouse backgrounds and other character sprites have separate owners. This is not a claim that one reviewer has approved all 75 assets.

## Method and limits

All 23 complete background frames were inspected in unwarped 768-pixel-wide comparison sheets; native crops were additionally inspected for the festival harpist/crowd, annual-remembrance crowd, community courtyard residents and mural figures. Day/dusk family interiors and the three plaza events were compared directly. All 3 familiar source sprites were viewed at their 1254-pixel source size. The 8 staged human sprites were compared against their originals at native facial-crop scale; the 3 final warmer Cassia variants were inspected again after their final iris update. Source/output/script hashes were then verified against the current recipes. Full-body identity, proportion and costume context came from the earlier sprite/reference review in the CG audit.

These findings concern visible source art and bounded edit quality. They do **not** certify Ren’Py chroma-key edges, on-screen sprite placement, dialogue obscuration, transitions, mobile layout, or People portrait crops; those require actual runtime evidence. Small background and painted figures do not support precise iris-color or height measurements.

Authority: [Book I source](../../revision/latest.md), current [family scenes](../game/family_book_one.rpy), [friendship scenes](../game/friendships_book_one.rpy), [script](../game/script.rpy), [location continuity](location-continuity.json), the author’s familiar reference and source character descriptions linked in the CG audit. The festival text explicitly names Selene’s **harp**. The outer construction text explicitly describes a device projecting a **blueprint**. Tree-of-Echoes dialogue identifies moving wood/branches as the almost-voice. Those visible details do not need new explanatory prose.

## Background findings

“Keep” means no independently justified source-art repair was found in the inspected dimensions; it is not a blanket runtime or architecture approval.

| Image | Disposition | Actual observation |
|---|---|---|
| [cassia-home](../game/images/backgrounds/book-one/cassia-home.png) | Keep | Warm inhabited craft/plant room; reachable low seating, tea and books. No embedded named face or contradictory action. Room supports Cassia’s family visit. |
| [construction-room](../game/images/backgrounds/book-one/construction-room.png) | Keep | Unfinished workshop with mechanisms and a pale blueprint display. The display has a concrete technological subject, matching outer-exploration dialogue; it is not a spirit or unexplained metaphysical light. |
| [dome](../game/images/backgrounds/book-one/dome.png) | Keep | Scaffolding and unfinished elevated platform frame the settlement. Floor depth and structure agree with the theme dome trio composition; distant architecture does not establish a foreground child’s height. |
| [echoes](../game/images/backgrounds/book-one/echoes.png) | Keep | Old hollow trunk, roots, branches and clearing support touching/listening to the wood. Blue plant light is environmental; no visible ghost, face in the light, or literal speaking spirit is added. |
| [festival](../game/images/backgrounds/book-one/festival.png) | Keep | Populated multi-level curved plaza, left stairs, archways and central raised round stage. Native stage crop shows silver-haired harpist consistent with Selene; flowers/lanterns and crowd action match the script. Small background faces are appropriately less resolved than portraits. |
| [garden-pond](../game/images/backgrounds/book-one/garden-pond.png) | Keep | Shallow visible stone-bottom water, bank and dry path agree with the pond-rescue/comfort setting. No character is embedded on the ledge in this background. |
| [garden-wonders](../game/images/backgrounds/book-one/garden-wonders.png) | Keep | Theme-only close view of plants and insects. Natural-scale insect detail and warm garden palette support the discovery lyric; no named character identity needs to be shown in this insert. |
| [garden-work-area](../game/images/backgrounds/book-one/garden-work-area.png) | Keep | Pots and a broad usable dry work surface sit beside the pond; their curve and reachable tools support the plant disagreement/compromise action. |
| [home-dusk](../game/images/backgrounds/book-one/home-dusk.png) | Keep | Direct comparison with family-home retains round table, chairs, left couch, alcoves, doorways and circular ceiling opening. Lighting and small table dressing differ with time; the room has not been rebuilt. |
| [library](../game/images/backgrounds/book-one/library.png) | Keep | Books, maps, globe and shared low table fit Dorian’s story setting. Clear foreground staging and consistent warm wood/plant materials; no incompatible embedded action. |
| [memorial-plaza](../game/images/backgrounds/book-one/memorial-plaza.png) | Keep | Same curved gallery, left stair, open arch and round stepped stage as festival, with remembrance flowers/messages and a substantial quieter crowd. No visual resurrection or supernatural Joren apparition. |
| [memory-mural-v2](../game/images/backgrounds/book-one/memory-mural-v2.png) | Keep | Native mural crop shows an intentional painting of the trio, raised treehouse, waterwheel and imagined exploration. Simplified profiles and illustrated adventure props are within the painting, not new literal events. Joren remains the blond boy, both girls brown-haired; tiny painted eyes cannot honestly certify iris hue. |
| [music-room](../game/images/backgrounds/book-one/music-room.png) | Keep | Harp, keyboard and available seating belong to a lived-in music room. The flute CGs remain separate matched action inserts; this background does not depict an advanced first performance. |
| [remembrance-plaza](../game/images/backgrounds/book-one/remembrance-plaza.png) | Keep | Annual gathering preserves the festival/memorial plaza’s main galleries, left stairs, central arch and stepped circular stage. Native crowd crop has coherent supported standing/seated bodies and family contact; changed flower/message dressing is appropriate. |
| [sage-room](../game/images/backgrounds/book-one/sage-room.png) | Keep | Soft low cushions, candles, bed alcove and communal small table suit Sage’s intimate storytelling setting. No disembodied symbols or spectacular event has been inserted. |
| [soren-workshop](../game/images/backgrounds/book-one/soren-workshop.png) | Keep | Plans, bench tools, a small wheeled mechanism and technological drafting display support Joren’s visit to Soren. This is a different owner’s workshop, so its furniture need not duplicate Arin’s. |
| [waterwheel](../game/images/backgrounds/book-one/waterwheel.png) | Keep | Completed wheel is physically in the shallow pond with its water feed and supporting timber. This is the actual story’s installation image; it must not be confused with the dry-plank theme construction test. |
| [workshop](../game/images/backgrounds/book-one/workshop.png) | Keep | Arin’s workbench, tools and open floor support building and instruction; consistent room use across workshop-first/family-rhythm/waterwheel. No finished pond outcome embedded prematurely. |
| [community-courtyard](../game/images/backgrounds/community-courtyard.png) | Keep | A populated but intimate courtyard with shared low table, cushions, planted arches and dry connecting paths. Native figure crop has readable seated support, without treating incidental background residents as named cast. |
| [construction-path](../game/images/backgrounds/construction-path.png) | Keep | Unfinished corridor/scaffold supports outer construction travel and meeting Joren. Visible supports and stacked materials explain the working location without depicting dangerous impossible character placement. |
| [family-home](../game/images/backgrounds/family-home.png) | Keep | Warm family room with large round working/dining table, chairs, sofa and connected doors. Reused consistently; no named person embedded who should disappear when the scene changes. |
| [garden-close](../game/images/backgrounds/garden-close.png) | Keep | Gardening tools, planting beds, broad curving ground path and small stool provide plausible physical support and scale for early garden activity. Pond sits beyond, not directly beneath foreground sprites. |
| [garden](../game/images/backgrounds/garden.png) | Keep within this audit; architecture owner also reviews | Full exterior visibly has a substantial upper timber room, ladder, immense oak and separate lower refuge. This review supports material/detail and no contradictory embedded person; final exact exterior-to-interior geometry and changed windows remain the separate environment owner’s scope. |

## Familiar findings

| Source sprite | Disposition | Identity, anatomy and comparison |
|---|---|---|
| [Nibble](../game/images/familiars/nibble.png) | Keep | Fluffy black-and-white coat, broad white face blaze, pink ears/paws/tail, violet viewer-left and coral viewer-right eye match the author’s reference. Four small paws and curling tail form a readable supported pose. The deliberately cute rat design is author-directed; applying the human face correction indiscriminately would lose that identity. Theme Nibble retains these markings/colors. |
| [Shadow](../game/images/familiars/shadow.png) | Keep source sprite; repair 2 CG details separately | Black cat with green eyes, bent tail tip and a small notch on the viewer-right ear in this frontal reference. Seated limbs are coherent. Pond-rescue and pond-comfort omit the notch; those require a tiny silhouette repair on the corresponding anatomical ear, preserving their differently turned poses and every human face. |
| [Barkley](../game/images/familiars/barkley.png) | Keep | Golden retriever coat, floppy ears, warm brown eyes and large fluffy tail match the CG dog. Seated front legs and rear haunch/paws are coherent. Source green matte is intentional and is not proof of runtime edge quality. |

## Eight staged sprite edits

The four early Calista variants now have slightly smaller, calmer eye apertures. The existing deep-blue gaze, nose, smile, freckles and skin modeling remain recognizable. There are no visible lid kinks, doubled lash lines or local seams in the native paired crops. Lyra’s restrained reduction similarly retains a distinctly younger, wide-eyed face. These are bounded improvements; they do not make every generated CG face match automatically.

Cassia-young’s geometry change is modest and retains the familiar smile and facial identity. The first iris pass was too cool/teal at the lower iris. The final warmer target `[.32, .57, .24]`, inspected independently after that change, reads as leaf/forest green in all three stages. Pupils, discrete highlights, darker upper pigment and some warmer flecks remain legible. Older and mourning variants retain their original face construction and expression. The final source art has stylized painted eyes; the review does not pretend it has become photographic or require further enlargement/brightening.

No blocker to promoting these **specific 8 staged edits** was found in this comparison. Full runtime compositing remains outside this finding. All source/output/script hashes matched the then-current `build/graphics-polish/characters/recipes.json` before promotion. The script checked was `scripts/polish_character_geometry.py`, SHA256 `1256b810fb9f1c99afcb31ca9ee2631c72de1eb9e665753979871a095d110110`.

| Staged sprite | Original source SHA256 | Reviewed output SHA256 |
|---|---|---|
| calista-young | `75649a7bc527427ab83e01d4b65749e9207562dadc9e36e0d9d4ce6cc1c541aa` | `7e37d6dd316296f9f89f3ce495cf999b0a3ace235c91be6661d129640e64d8ee` |
| calista-home | `c89f5aa739a14a19b687842c9dc00c54cc2cae3fba101d6869c19a5134494d36` | `407e2ac4a120d2346fd1599c1a9002914e9cd70385f9ef605ac430200b68ab1f` |
| calista-festival | `3a796e998447303d3006871047579793e47db85bebceef1ec0dca323601e29c7` | `cc63e75baf92ad6fa2b1cfff17611f7cd1a7213d65671f6d149f6429fe13ec7f` |
| calista-festive | `ae6808ba84ca5d16f87353f5ecac1aca111fd1531d9933b1a794f4e3f15e350c` | `edff3baed0a6fb3387f7c40c49c3b18c01f830b1ba786c7137572918774bc04a` |
| lyra-young | `7671dd825364831392dad574e2eccad9f73bf538360f75f3fd26b8da6af7cd92` | `af01a6bbb63789a8f060a5ed3b4c4c910246c21a215ece452c2514c7cc8a051d` |
| cassia-young | `362378277efed564dcc97d3902fd3262bd3cd7ce5c0a7e1c979f3b240ce81283` | `353258e8c289f3eb3f95a0329fb1ae44b48fdab90d8604dcc64547cb5581f363` |
| cassia-older | `70b224c4bdc84af7bd09a0e36c44f79294469d1d08a7535a08284b6716f2186c` | `f65d350cb1d99f692c0de61ee2f160f21795aefafd7d263e88e29f27939865d6` |
| cassia-mourning | `9495dfb45c7f45f62bc746b3f655477279e2ab13d39cd31aa2cd45fd16f2caa2` | `8fe0c0a2c74c0199a05cba55115c494f6188c36064d3144bcec2dd3586bcc9b1` |

## Background/familiar source snapshot

These hashes identify the pixels inspected, rather than importing an old acceptance. A later change requires a review of its changed scope.

| File | SHA256 |
|---|---|
| `game/images/backgrounds/book-one/cassia-home.png` | `8e536261e4b647371e346cfc34bd818dad026026eb209d5d4c458f0b2e6c0e0b` |
| `game/images/backgrounds/book-one/construction-room.png` | `c5e93b257206702921c19f923b5ee9bcc14676f5ee08765ab37a88d4e0ae18b3` |
| `game/images/backgrounds/book-one/dome.png` | `dc168e36c3f1a5a9851dbad7d0ba2e30e6dfd71116d77f4447dbc5d4f6ddcaa8` |
| `game/images/backgrounds/book-one/echoes.png` | `cb84874fe2ab57c98c382ca9da15e7f10ac9d9160be780122a0abd69b119c814` |
| `game/images/backgrounds/book-one/festival.png` | `0d1ddc42de15e46e839290310074c2db15d0ab5a25f000f2fb4882f236ffb141` |
| `game/images/backgrounds/book-one/garden-pond.png` | `5fe43f183e54eaa586d4fc085258c770326cc4171234333906840c7fa1f4e958` |
| `game/images/backgrounds/book-one/garden-wonders.png` | `7da2fab31aef36de1a6bde4bbd347193bffe79bd395d3fd6d26ff75c8b0b4aef` |
| `game/images/backgrounds/book-one/garden-work-area.png` | `b5e24f27f7d14e154c4e9cbc924827e1d85d2c7310ae623bd055211af1578aac` |
| `game/images/backgrounds/book-one/home-dusk.png` | `22af8146417df1fac47983901df8ddd7a3adc12737b4bbcdb33372d9ca85d45b` |
| `game/images/backgrounds/book-one/library.png` | `9d2380db731f2576fadba93d4aa7be7460873a701efd973559981b41c5b9cddf` |
| `game/images/backgrounds/book-one/memorial-plaza.png` | `242f9f11339c27d0f479a5280b58ed37e9df754030c490feca59c121c455167c` |
| `game/images/backgrounds/book-one/memory-mural-v2.png` | `38cb3dd1cfad04400f6fec8d971a4171a4eff513c26f9c1e507aefd9fceaba47` |
| `game/images/backgrounds/book-one/music-room.png` | `f3f9eae745ab6e93e0dfe100a9207977901e874624315f5c139eff500706c464` |
| `game/images/backgrounds/book-one/remembrance-plaza.png` | `ad1667be4328b4763e5d9282528e40b042c4eb489de7633663169e551bb54495` |
| `game/images/backgrounds/book-one/sage-room.png` | `b51b309492a5d8026571ff3938d5aae102515653250df054c1dd3d461751d581` |
| `game/images/backgrounds/book-one/soren-workshop.png` | `d451bcedd70e8c80546a8147a33877dce0454a92004b017002aa45050460ae0b` |
| `game/images/backgrounds/book-one/waterwheel.png` | `072158f6d372d60bd6b19e15f6a8cfba26431f74b5e079ac6a21cc0714f76085` |
| `game/images/backgrounds/book-one/workshop.png` | `603d67750be055357d53693ea315aa201473db6a746ab02f8a5f968c9b9b2934` |
| `game/images/backgrounds/community-courtyard.png` | `a02f53750be493a139f06a3811e3911736f9846aa6eb06de6e53342974f9f048` |
| `game/images/backgrounds/construction-path.png` | `9d36f01f1f51194bc99e0d79ce8811397c0b90a23f2df71de18d7a39e90dd0b8` |
| `game/images/backgrounds/family-home.png` | `dbf252a7502305a15c685bcbc6bfc7973f5bf2db277401dbdd6e6fda87d15a6a` |
| `game/images/backgrounds/garden-close.png` | `4d6729bc69f1ca19f13bfc50015d2efc9ecdcb63ab269e889cf79ddd73f05c0a` |
| `game/images/backgrounds/garden.png` | `e32d470defeda7faccd5e6fa1c08125faf9e60f818506e6cb15aae364725d243` |
| `game/images/familiars/nibble.png` | `a3eb23fe22427f87b6fdf12c7c6c2fdf7dcbc87d50579ba288726f2bd7f1bb95` |
| `game/images/familiars/shadow.png` | `f6864aa410c2968f57ae863a41b2c22b389fa12401a501c57aae705961b90f59` |
| `game/images/familiars/barkley.png` | `49084a021567be20c336956201f5ed6bfdb4ac6a9c8a8198b7e2040e7d88ad37` |

## Bounded runtime fringe comparison

After the source-art review, the release-matrix owner supplied native 1920×1080 bright/dark four-character fixtures for a small shader change that widens color-spill cleanup without widening alpha removal. Both complete fixtures and paired Lyra, Selene and Cassia crops were independently inspected. The new treatment is a **small improvement** around Lyra’s curls. The curl silhouette, green eyes and Selene’s white strands remain present; no new transparency hole was observed in these comparisons.

Lyra’s strong painted golden outline remains, and some outer Selene curls retain a pale yellow/green fringe in both old and new crops. This is not evidence that all compositing fringes are eliminated. It supports keeping the bounded shader delta without claiming every story scene or every cast sprite has been visually approved by this comparison. These fixtures also do not themselves certify the physical placement used by the actual story.

| Reviewed current fixture | SHA256 |
|---|---|
| `test-results/character-layout/dark-scene.png` | `076d3bc4f35a592c8f8db89e525042cd3e3e2ddc332bdb8021a29eabae345646` |
| `test-results/character-layout/bright-scene.png` | `8d7c5241898926f0d07201093e34b29a34b32458d488ce06dd86680aae86ab5a` |

Shader-containing file checked: `game/visuals.rpy`, SHA256 `8edf5bbff16dbe5637de29bca7010f24a538cb4fe85d8420a2150a3b7f2b7549`.
