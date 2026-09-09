# Familiar compositing refinement · 9 September 2026

Implemented two scene-specific refinements in [familiars.rpy](../../../visual-novel/game/familiars.rpy), then compared fresh native Ren’Py renders before and after. The selected result and its originals are preserved in the [comparison receipt](familiars/receipt.json) and linked below. No generated paint, PNG edits, shared chroma-key changes or new contact-shadow artwork were needed.

At the Tree of Echoes, Barkley’s original bright orange-gold coat appeared more strongly sunlit than the cool clearing. A Barkley-only `TintMatrix("#d5e3f5")` now applies at this background: approximately 0.835 / 0.890 / 0.961 RGB multipliers, with alpha unchanged. His golden coat, brown eyes, expression and fur edge remain readable. The result respects the [manuscript](../../../revision/latest.md) passage describing his golden fur shining in afternoon skylight.

In the construction room, the dialogue gradient obscured Nibble and most of Shadow. Nibble now sits on the clear front workbench at `(760, 610)` and Shadow on the visible doorway floor at `(1360, 760)`. Their display heights remain 90 and 185; Barkley remains 310. The new placements visibly meet the tabletop and floor, keep the projected blueprint readable and preserve the rat–cat–dog size ordering. These exact positions are production staging, consistent with the group exploring the tools-and-machines room; they are not added canon.

Visual inspection confirmed that Nibble’s light coat, dark facial patches and violet/right–coral/left eye identity remain intact. Shadow’s green eyes, ear notch and crooked tail remain consistent with her [wiki entry](../../../wiki/bios/Shadow.md); the selected left-ear placement is retained. Lyra’s fine warm hair fringe remains visible against Echoes, but the selected native view did not justify another global keying adjustment.

The focused test navigated the real chapter UI through Echoes, the construction path, the construction room and home in an isolated project. Each scene was captured with dialogue visible and hidden, yielding eight frames per run at 1738 × 977. Both Ren’Py runs passed. Home and construction-path frames are pixel-identical before and after, including the return from the tinted Echoes scene. Echoes differences are confined to Barkley’s on-screen bounds; construction-room differences follow the moved small familiars. All three source PNGs retain their exact bytes.

| Native frame | Changed pixels | Observed outcome |
| --- | ---: | --- |
| construction-path-clean.png | 0 | Unchanged control. |
| construction-path-dialogue.png | 0 | Unchanged control; existing foreground companions still enter the dialogue fade. |
| construction-room-clean.png | 20,852 | Nibble meets the workbench; Shadow meets the doorway floor. |
| construction-room-dialogue.png | 20,733 | Both small familiars are substantially clearer above the text. |
| echoes-clean.png | 36,020 | Gentler golden coat under cool shade; silhouette unchanged. |
| echoes-dialogue.png | 36,015 | Warm identity remains clear within the final dialogue framing. |
| home-clean.png | 0 | Unchanged control after leaving Echoes. |
| home-dialogue.png | 0 | Unchanged control after leaving Echoes. |

This check covers the selected desktop compositions and scene-to-scene reset, not a full-book release test, every accessibility setting or WebGL/mobile rendering. It does not claim that every familiar is fully visible through the dialogue fade in every scene. The main integration pass owns broader runtime checks and rebuilding.

| Preserved comparison | Before | Selected after |
| --- | --- | --- |
| Echoes · dialogue | [PNG](familiars/before/echoes-dialogue.png) | [PNG](familiars/after/echoes-dialogue.png) |
| Echoes · hidden UI | [PNG](familiars/before/echoes-clean.png) | [PNG](familiars/after/echoes-clean.png) |
| Construction room · dialogue | [PNG](familiars/before/construction-room-dialogue.png) | [PNG](familiars/after/construction-room-dialogue.png) |
| Construction room · hidden UI | [PNG](familiars/before/construction-room-clean.png) | [PNG](familiars/after/construction-room-clean.png) |

The archive contains both native logs ([before](familiars/before/native.log), [after](familiars/after/native.log)), testcase definitions ([before](familiars/before/testcase.rpy), [after](familiars/after/testcase.rpy)), both familiar-code snapshots, the [original runner](familiars/run-native-as-executed.py), [global test support](familiars/global-test-support-as-executed.rpy), input records and [pixel comparison](familiars/comparison.json). The [receipt](familiars/receipt.json) hashes every archived file and retains all four unchanged control-frame hashes without duplicating those PNGs. `after` corresponds to the original `candidate` run. The before definition was recovered from the unchanged runner template; only its screenshot-directory value differs from the after definition. Historical scripts retain their machine-local paths. Archival did not rerun tests or change runtime code.

Runtime code SHA-256:

```text
before  da70dd1da9e1fd15fb044ddbebb7109d0b90cddd69e0ed154dfef6a4f652cce2
selected  6985c15f0436b65547bb00ccbe4bc627572a4e462c0ecb1c24bf017c7793056e
```

Unchanged source PNG SHA-256:

```text
game/images/familiars/barkley.png  49084a021567be20c336956201f5ed6bfdb4ac6a9c8a8198b7e2040e7d88ad37
game/images/familiars/nibble.png  a3eb23fe22427f87b6fdf12c7c6c2fdf7dcbc87d50579ba288726f2bd7f1bb95
game/images/familiars/shadow.png  f6864aa410c2968f57ae863a41b2c22b389fa12401a501c57aae705961b90f59
```

Primary comparison screenshot SHA-256:

```text
familiars/before/construction-room-clean.png  eac9b0ccf0c30354b12ec86faedd0d3e8c8d599f0bcb3799efe1a087d6ed46e0
familiars/after/construction-room-clean.png  32327295969fe70cb383887b42aad5ebf327baf5fe497b83ee3577125628a2e0
familiars/before/construction-room-dialogue.png  cb8bda6bde0d4f6f9bb43f04a7ae50a098136827f567c2cfad111f0bf2312742
familiars/after/construction-room-dialogue.png  aac57146d5be6aa679b6a55f07b188673f5d1802b708b038be8ed074c0f2dc88
familiars/before/echoes-clean.png  a6dae2e51a242176fa032aa1c26fb7161aab1485b5ccd17f0111b7adbadde5c3
familiars/after/echoes-clean.png  66a9d577c0f2cabefefb5dd0e7e62d9ed68186c18713a6efb0d4f3ca8081832c
familiars/before/echoes-dialogue.png  100f520e2261ff06aefe91941bb989499988fcf1cfb3618d3172970f0f6a8b63
familiars/after/echoes-dialogue.png  10b8430984f60e56a5935ef589361ec7af32e6554713a330fd292c9fb81fb102
```
