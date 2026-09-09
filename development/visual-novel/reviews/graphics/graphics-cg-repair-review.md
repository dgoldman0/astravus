# Review of staged CG repairs

Independent visual review by `glossary_story`, 2026-09-05. This is a follow-up to [the original 20-CG audit](graphics-cg-audit.md), limited to the six staged face repairs and the two separately staged Shadow details. It does not replace that audit with a blanket PASS.

## Six face candidates

Each original/candidate full composition was viewed side by side without aspect distortion, followed by native-size paired crops of every changed named face. The larger generated face-material previews were considered only input material; acceptance observations below concern their actual registered size in the CG. Source and staged output hashes were checked after inspection. These are source-art observations, not Ren’Py runtime or final environment-window approval.

| Candidate | Finding | Concrete observation |
|---|---|---|
| [theme-treehouse-arrival](../../archive/local/graphics-workspace/cg/theme-treehouse-arrival.png) | Improved; no visible local seam | Cassia has a fuller, less pinched lower face and calmer eye apertures, with warm umber skin, the existing welcoming smile and green irises retained. Calista’s eye reduction is modest, retaining the book-holding pose and blue gaze. Native boundary inspection finds no doubled nose/mouth, abrupt hairline replacement or clear feather seam. The new Cassia material remains painterly; it is not photographic. Bodies, Joren, hands and room are preserved. |
| [treehouse-friends](../../archive/local/graphics-workspace/cg/treehouse-friends.png) | Improved; no visible local seam | Cassia’s short pointed lower face and round apertures are less exaggerated. Her mouth/head slant changes slightly within the same listening/talking pose; the result still reads as Cassia facing Joren. Warm cheek/forehead shading integrates with the scene at native crop scale, without an obvious patch outline. Calista remains recognizable after the small eye edit. Seated support, map, hands and Joren remain intact; a seated crown alignment is not a stature ruler. |
| [cassia-storytelling](../../archive/local/graphics-workspace/cg/cassia-storytelling.png) | Restrained improvement | Calista’s apertures are slightly calmer while her gaze toward Cassia, blue irises, freckles, hair and drawing action remain. No lid kink or local smear is visible in the native pair. Her lower-face construction remains the original stylized construction; this edit does not claim a wholesale face redesign. |
| [theme-dome-friends](../../archive/local/graphics-workspace/cg/theme-dome-friends.png) | Revised material improves later-age construction | The revised Cassia material has fuller cheek/jaw/nose construction and quieter, smaller green eyes. At native size she reads more convincingly as the later child alongside the unchanged body and peers. Warm umber identity and expression remain. No clear mask edge, doubled feature, hair or body regression was found. The small original Calista/Joren eye edits remain restrained. |
| [theme-morning-outlook](../../archive/local/graphics-workspace/cg/theme-morning-outlook.png) | Revised material improves later-age construction | The revised Calista face has calmer eyes and more grounded cheek/lower-face modeling while retaining deep-blue irises, freckles, olive warmth and the hopeful sideward gaze. No obvious mask seam or hair/body regression appears in the native pair. The large foreground figure against a farther doorway remains appropriate. |
| [theme-garden-opening](../../archive/local/graphics-workspace/cg/theme-garden-opening.png) | Clear improvement; no visible local seam | The new Calista material has less circular exposed eyes and lower-lash prominence, with stronger nose/cheek construction. Freckle density changes and the cheek texture is softer than the original isolated crop, but it remains resolved at native size and does not look like a flat blur in the whole scene. Irises read muted steel/deep blue under warm light, not green. The smaller girl/older Kael relationship, sunflower action, hands, hair silhouette and illumination remain. No visible hard patch boundary or doubled feature was found. |

An initial aperture-only treatment left the later-age facial concern unresolved. The two later shots were subsequently revised with portrait-guided face material and inspected again as complete compositions and native paired faces. The current table/hashes record those stronger revisions, which address the specific construction concern without inventing exact canonical ages or rescaling entire bodies.

| Candidate | Original SHA256 | Reviewed staged SHA256 |
|---|---|---|
| theme-treehouse-arrival | `7525e3f19fab329fb96b0ed6d1ac6c1aa06db608b8197ad8d7b83fbd3c5554a6` | `80eed0b8a917fc6fe75cb4e21e270f31a7e25c8f093b102f38009a370860fbbe` |
| treehouse-friends | `5bf094774526bf79a5ffd6bdd7b9e1cf2b07c74a8dd0c42778b3b43a2892f318` | `b8d68644118b9b2eae9af8f8dc56b3490065d7aa540621e230b8aa630f3d96fa` |
| cassia-storytelling | `74608e12c38015c5129b3c08db5af53d267d4e35b473857acf2d398d85ac3503` | `430f4d3d4bb88b6034b7272f9b530fe01af8209fd716c7182edc4e145e226563` |
| theme-dome-friends | `9ee19cb65c68b41d5e03f3c6cf40d6fe617c6d0db3abe7ce6774a7e0da3611c1` | `2ef5e062beb591c59fb5d50673164a9d579650b7567ba4289313d1c886d8e62d` |
| theme-morning-outlook | `61382b336aeb7c7989e7339855dbf89337e0f9c29ab5a90cbd04bb25b147834f` | `b7905063e91564ddf35edee6d7ade57477e64beee16d70db90efc26cb38017bd` |
| theme-garden-opening | `cc409a5fd4996cf8839252c402efda8ef611da9670e82426e2611b07ba531c51` | `01dac4af7615514eaa3f08c4caab3e03571972b02d71e3db2625cd2c4c52d350` |

## Shadow ear-notch candidates

The reference [Shadow sprite](../../../../visual-novel/game/images/familiars/shadow.png) has a small notch in the anatomical left ear, which is viewer-right in its frontal pose and in the two CG three-quarter poses. The two CGs lacked that mark. [The explicit geometry specification](../../../../visual-novel/docs/graphics-shadow-notch-spec.json) records the side, polygon, source hash, reference hash and donor offset. [The reproducible script](../../../../visual-novel/scripts/polish_shadow_notches.py) samples neighboring **source background** through an antialiased notch mask; it does not regenerate a cat, alter a human or filter a complete frame.

Both full candidate compositions, native ear/head crops, and enlarged nearest-neighbor comparisons were inspected. The notch remains small at full scene size, with the nearby background filling the triangular silhouette opening. No unrelated facial, paw, tail, clothing, hand, pond or lighting change is present. Enlarged images are useful to inspect the mask; their pixelation is not a new source-art defect.

| Candidate | Scope | Reviewed staged SHA256 |
|---|---|---|
| [pond-rescue](../../archive/local/graphics-workspace/shadow/pond-rescue.png) | 45 pixels changed; zero outside declared mask; RGB canvas unchanged | `e7d6e33da6ff87a1757344d7191d5589b603e9491dcd1587676fefc69e7b070e` |
| [pond-comfort](../../archive/local/graphics-workspace/shadow/pond-comfort.png) | 35 pixels changed; zero outside declared mask; RGB canvas unchanged | `4eab6fba3b5a0d6976f8e2684c7021cf4dc5c3e56e6b7d4622cb0e2df0da98e0` |

A second run into `/tmp/shadow-notch-reproduction` reproduced both PNGs byte-for-byte. An independent array comparison verified the recorded changed-pixel counts and zero changed pixels where the saved mask is zero. The staged `recipes.json` records source/output/mask/script/reference hashes and exact changed bounding boxes. The original runtime CGs were not modified by this subtask.

Reproduction from the explicit immutable Git source blobs recorded in the specification:

```sh
python3 scripts/polish_shadow_notches.py --output /tmp/shadow-notch-reproduction
```

After authorized promotion, the runner was updated to read the original Git blobs and verify their same SHA256 values. This avoids applying old coordinates to the newly installed output and preserves reproducibility without a separate runtime backup. A fresh run into `/tmp/shadow-notch-git-reproduction` reproduced both installed PNGs byte-for-byte. The frozen runner SHA256 is `aa79afb9827994af3fc2eedae7abb2fd7299c8d641f9cb305d3c1b1cd1a6fe71`, and the staged recipes were refreshed to that exact runner. The candidate is ready for an independent production-owner review. Image promotion, runtime checks, manifests and release actions belong to their owners.

## Waterwheel scope clarification

The dry-plank `theme-waterwheel-team` image is used only in the closing montage. Keep it explicitly classified in the production storyboard as an outdoor **construction test**, before pond installation. The story scene continues to use the separate `waterwheel` background with the completed wheel in the pond. This interpretation must not be presented as a newly sourced event or inserted as explanatory narrative dialogue. The earlier audit’s conditional action finding is resolved only under that restricted usage; it is not approval to reuse the test shot as the completed pond action.

## Authorized Shadow installation

After the production owner independently reviewed and accepted the two candidates, the exact reviewed PNGs were installed in `game/images/cg/book-one/pond-rescue.png` and `pond-comfort.png`. Source and candidate hashes were verified before replacement; installed hashes match the candidate table above. No other runtime art was changed by this installation. Manifest/immutable-input registration belongs to the release-matrix owner. The earlier “runtime CGs were not modified” sentence describes the staging/review phase, before this subsequent authorization.

## Revised branch-only environment candidates: independent review

The three `build/graphics/environments/exterior-rig/*-near-candidate.png` files were reviewed as complete compositions and native paired window crops against the original runtime CGs. An initial daylight overlay was held because its flat dark leaf patches and pale cyan rim fragments contrasted with the existing backlit foliage. The environment owner revised the daylight matte/color/focus treatment, and the two new complete frames and native window pairs were independently inspected again.

- `treehouse-friends`: the conspicuous cyan rims and opaque leaf-stencil patches are gone. Warmer, softer near twigs sit within the original backlit depth without drawing attention from faces or changing the room’s materials.
- `theme-treehouse-arrival`: the olive stencil patch beside Joren/curtain is gone. Subtler near foliage integrates with the original light; the warm face/room focus is preserved.
- `cassia-comfort`: the unchanged cool, darker twigs integrate plausibly with the night scene. Some twigs are crisper, which can read as near foliage. No face/room regression was observed in this branch-only candidate.

The revised **art treatment** is supported for production-owner use. Exact spatial continuity/projection still belongs to the environment owner’s geometry review. These flattened comparison candidates contain the original face baseline, so production must merge the accepted **branch difference/layer only** onto the accepted face repairs and inspect that combined output. Replacing a repaired CG wholesale with an environment comparison candidate would undo its face work.

| Revised branch-only candidate | Reviewed flattened RGB SHA256 |
|---|---|
| treehouse-friends | `718248b88febdd95c237cc478e5386a749bd8bed6cde1ed6e72fb515e5ec520d` |
| theme-treehouse-arrival | `03c8ca774e85f84e8c2419b876849c06e312e480fa19d5e8791e612947942fce` |
| cassia-comfort | `4148066089369387844affb7be75c8e9c2a05d5d434af8a070a668419ff8d08e` |

The comfort layer hash `bce4385…` mentioned by the environment owner is its RGBA overlay, not the flattened candidate above. The actual night candidate pixels remained unchanged between reviews.
