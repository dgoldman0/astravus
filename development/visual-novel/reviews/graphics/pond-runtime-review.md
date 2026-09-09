# Pond changes in native presentation

The current 12-capture native run passed all **20 assertions**. All twelve complete frames were inspected; the repaired rescue far bank was also inspected at native pixel size. The four pond edits preserve the visible character and prop contacts. Dry ground now connects the rescue's far planter to its coping, removing the extra wet-channel reading. This closes the scoped native pond review; it is not a new whole-game art or sound approval.

The focused suite uses chapter navigation and dialogue advancement. It hides the story UI for support checks, then enters the actual `ClosingTheme` displayable and pauses its shared planting cue at 28.36 seconds. This is runtime evidence, not direct source-image previewing or an MP4 substitute. The final testcase finished in **27.901 seconds** on 2026-09-05 with version **0.1-alpha**. Its log is `test-results/pond-state-review.log`; screenshots and the complete input/screenshot hash receipt are under `test-results/pond-states/`. The receipt timestamp is `2026-09-05T21:56:52+00:00`, SHA256 `c2536de6264f0d0f90403358051a72b622f3a27d228ada527efa205f7d3e44d8`.

| Installed runtime asset | SHA256 |
|---|---|
| `game/images/backgrounds/book-one/garden-work-area.png` | `cab0cbcfc99633faf099baa3122434c13ea5eee0711acd5aff98ac0f4f973f62` |
| `game/images/cg/book-one/garden-compromise.png` | `dec70c2e6a360ab0cdb6cfca4d174b347dbe27f3090f3745cbf9b25787218ff6` |
| `game/images/cg/book-one/pond-comfort.png` | `422994051d70b7782beee5e8babd1190b6fc87c64a9d1ba40c2b7a1bab157bcf` |
| `game/images/cg/book-one/pond-rescue.png` | `cca21ae9421261f603bf1bf3a2b7281273a118a399002f7086285c518e0f62fd` |

## Observed frames

Every complete screenshot was inspected in sequence. Native-size crops additionally show the planting pot bases, comfort knees/boots/paws, rescue far coping and waterwheel familiar placement. UI-hidden support views are distinct from their dialogue-visible companions. The first run caught the rescue's second wet-channel reading; after its repair, the final run produced two changed rescue frames and ten byte-identical frames. Both changed frames and the current sequence were inspected before accepting the scoped result.

| Capture | Actual observation |
|---|---|
| `03-planting-background-dialogue` | New plants and pots sit on a broad dry working bank next to low pond coping. The fence, planted boundary and water remain visible; the old tall retaining-wall pool no longer dominates the shot. The introductory line remains readable. |
| `03-planting-actors-support` | Calista and Kael stand on the dry paved working area, clear of the water and rim. Their visible boots are not buried or left over open water by the new background. |
| `03-planting-compromise-dialogue` | The populated CG follows the working-bank view: Calista, Maia and Kael gather around pots on dry ground, with low coping behind them. The dialogue layout does not introduce duplicate sprites. This remains a broad planting/cooperation illustration; the particular narration about pointing to a reflection is not literally depicted by its pose. |
| `03-planting-compromise-support` | Pot bases, knees, bent legs and hands keep their existing contacts with the dry paving and pots. Lowering the background wall has not moved the figures or cut across those contacts. |
| `10-pond-establishing-dialogue` | The established pond is a low basin with visible shallow-water stones, an inlet at left, fence and plants beyond, and lily pads at right. The scene introduces a small pond. |
| `10-pond-rescue-dialogue` | Calista and Kael reach toward Lyra in the water; Barkley and Shadow remain on the bank. Lyra's dialogue has no redundant portrait over the CG. Dry paving replaces the unwanted reflective strip beyond the far coping. |
| `10-pond-rescue-support` | The rescuers' knees and boots remain on dry ground, and their hands reach Lyra. Lyra's bent body can account for the water reaching her torso without establishing a precise water depth. The far planter now connects to the coping through a visible dry paved strip: the main basin is the only water area. The local repair has not changed the human or familiar silhouettes. |
| `10-pond-comfort-dialogue` | The embrace sits on a broad dry bank; the repaired low pond edge behind the family now agrees in scale with the establishing view. Dialogue remains readable, and the illustration already contains the speaking characters. |
| `10-pond-comfort-support` | Calista's seated knees, Lyra's curled legs, Kael's crouch and the animals' paws all meet the visible paved bank. No repaired water or coping crosses their bodies or feet. |
| `20-waterwheel-background-dialogue` | The completed wooden wheel sits at the left inlet in the established basin. The script says it has been carried to the pond and its supports settled. The retained fence, inlet, near coping and right lily pads make its relation to the establishing image observable. |
| `20-waterwheel-familiar-support` | Shadow and Nibble occupy the wooden toolbox area on the left bank; Barkley sits on the right coping/bank. The rat is small but visible. Their support areas are dry and separate from the water. |
| `theme-garden-compromise-native` | The actual shared theme displays the new low-bank planting CG at its fully settled cue, with all three figures and the pots visible. Resume/Skip are the real theme controls. The receipt's underlying story background tag does not identify the visible image: its `screen` is `closing_theme`, and its `theme.image` records the selected planting CG. |

## Scope and reproduction

Run from `visual-novel/`:

```sh
python3 scripts/project.py test --headless --suite pond_state_review
```

The capture helper snapshots game scripts, all installed PNG assets and the shared theme cue, rejects changes during the run, and records every screenshot hash. It uses the isolated test state directory. Passing assertions establish coverage and stable inputs; they do not independently establish art quality. No score, auditory playback, movie motion or unseen floor-plan facts are approved by this check. Source-frame pond geometry is also reviewed in [POND_GEOMETRY_REVIEW.md](POND_GEOMETRY_REVIEW.md).
