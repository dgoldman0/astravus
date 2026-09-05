# Reader usability review — 0.1-alpha

Result: accepted for the inspected Linux desktop and Chromium layouts after the Help-column and quick-bar fixes. Reviewer: `art_sprite_review`; root independently checked the final small-window Help and dialogue views. Functional assertions and observed presentation are recorded separately below.

## Exact final run

[Focused probe](../scripts/browser_usability.py): **5 grouped checks passed, 0 browser/engine errors, 41 fresh browser captures**: 16 at **1280 × 720**, 25 at **960 × 540**. Run: `2026-09-05T16:20:09.237495+00:00` to `2026-09-05T16:21:47.902861+00:00`. Chromium used Linux software WebGL and a fresh temporary profile; actions were actual pointer clicks and keyboard events. Engine observations supplied visible focus rectangles, text and state, without invoking menu actions or injecting story progress. The test used the real chapter picker to reach the later knowledge pages and ending.

The exact [run log](../test-results/usability/browser-usability.json) has SHA-256 `5e7b6fe5fcb86532772f69197ff323e34ee03f03d7704cb4632c0e621ef2882f`. Final browser archive SHA-256: `7b6df1432271365e4d562b419eb4027a0bf5f8c34f98aa60b8e08052badbd3c9`. Exported `game.zip`: `5b3edbc4f5a9279ac4de6eb3adca58a388a11fc34e43143b5552f2abc3debbe5`. Those artifact hashes stayed unchanged throughout the run. Reviewed `screens.rpy`: `1b2aa2999eec2aee1a296cd8aec98528b7ed0b9418959dd8d8e61f9f46317635`.

Current native Linux [History](../test-results/screenshots/history.png) and [Settings](../test-results/screenshots/settings.png) captures were also visually inspected at 1738 × 977. The matrix's current native playthrough, glossary and theme checks pass separately. This focused probe does not replace the full story, browser cache, credits-link or package checks.

## What the assertions establish

| Group | Observed events and state checks |
| --- | --- |
| Keyboard focus and activation | ArrowDown moved focus from Begin Book I to Load; Enter opened Load. The probe used no Tab-as-focus assumption: Ren'Py uses Tab for skipping. |
| Fresh empty Load | Six empty numbered slots were disabled. Escape returned to the title. |
| Reading menus and warnings | People, Glossary, History, Settings, Help, Chapters and the pause menu opened at both browser sizes. Return, Keep reading, Escape and the warning's Go back kept the same scene, dialogue and knowledge state. Larger text, solid dialogue background and reduced motion toggled successfully. |
| Save/Load and negative confirmations | Automatic, Quick and numbered pages selected correctly; Save switched from the read-only Automatic page to page 1. Six empty page-3 save targets were enabled. A real saved slot appeared; overwrite No and delete No preserved its exact timestamp/metadata, and Escape canceled loading without changing the current read. |
| Opt-out and theme | Chapter spoiler warnings visibly switched Off; a real jump to chapter 32 proceeded without the warning. Populated People/familiar and Glossary selections remained usable. Reduced-motion theme playback, Pause, Space to resume, Escape to leave, replay and Skip closing theme worked, and the theme channel stopped on leaving. |

## What the visual review establishes

| Area | Actual presentation findings |
| --- | --- |
| Title and keyboard focus | The primary Begin action is prominent, and Load/Settings/Credits/Chapters/How to read are plainly labeled. The focused Load control has a visible shaded rectangle and warm text; it is distinguishable from the primary button. The keyboard sequence reached its intended destination. |
| Help | The earlier shortcut/explanation concatenation was a real defect, despite passing functional assertions. A fixed 420px shortcut container with a 30px gap now gives every explanation the same start position. H and V are visibly separate from Hide and Toggle; longer mouse/keyboard labels also fit. The [1280 view](../test-results/usability/1280x720-help.png) and [960 view](../test-results/usability/960x540-help.png) have clear, unclipped rows and footer guidance. |
| Dialogue and quick bar | The solid background gives the larger italic dialogue good separation from the painting. Increasing quick-bar type from 21 to 26 virtual pixels makes labels about 13 screen pixels at 960px width, compared with roughly 10.5 before. All ten labels have distinct spacing and remain inside the window at [1280](../test-results/usability/1280x720-large-solid-dialogue.png) and [960](../test-results/usability/960x540-large-solid-dialogue.png). The larger labels neither crowd the dialogue nor overlap one another. |
| Menus and destinations | The consistent left sidebar, warm selected text and persistent Return make repeated menu navigation understandable. Escape opens a pause menu whose Keep reading action clearly returns to the current line. Save and Load are separated by reading-reference links in the sidebar, but both retain explicit names and distinct page headings. Chapters is easy to reach from the title or reading bar; from an open sidebar menu, Return reaches that bar. |
| Save/Load and modal feedback | Large thumbnail targets and Empty slot labels clearly distinguish unused slots from the dated saved thumbnail. Current numbered pages are highlighted. Automatic is subdued in Save, with explanatory text below the slots. Overwrite and delete confirmations state the affected action and offer separate Yes/No targets; dismissing them visibly returns to the underlying menu. The spoiler modal has readable consequence text, Go back/Jump anyway actions and an explicit reference to the On/Off setting. No required control is clipped at 960 × 540. |
| People, familiars and Glossary | Early People offers Cali and Lumen, with introductory family context in Cali's biography; it does not expose future-friend profiles or plot outcomes. Early Glossary explicitly says No terms yet. The later lists have a clear selected row, spacious definition pane and recognizable familiar tabs. Shadow, Barkley and Nibble portraits and descriptions fit at 960 without overlap; the Nibble markings remain legible. Populated Glossary definitions fit the right pane with clear selection. The native longer History view has readable paragraph spacing, a visible scrollbar and its current line at the bottom. |
| Settings | Reading, Sound, Display and Skipping groups are distinct. The two sound sliders have clear labels, enabled reading options use warm selected text, and the chapter-warning control explicitly says On or Off. Both inspected browser sizes retain the footer and all controls. The native capture confirms the same hierarchy at the larger desktop window. |
| Afterword and theme | The afterword title, paragraphs and three next actions are separated and readable at 960. Theme buttons use a dark backing over the illustration; Pause changes to Resume, making paused state visible. Skip has an explicit label, and the ending offers both replay and Return to title. The playback controls fit at both captured sizes and do not cover the central characters' faces. |

## Remaining limits

960 × 540 is the smallest browser window inspected. The quick bar is improved, but secondary notes, some menu text and theme controls are still compact there; 1280 × 720 provides more comfortable reading. Larger dialogue text changes dialogue rather than enlarging the entire interface. Most setting toggles signal selection through warm text, while the spoiler setting additionally spells out On/Off.

This review covers mouse/keyboard use in Chromium on Linux and the named native Linux captures. It does not establish touch-phone, gamepad, other-browser or Windows-machine behavior. Those are scope limits, not waivers of the required controls checked here. No additional blocking visual defect was found in the inspected final views.

The release receipt binds this report, the final run log, all 41 browser captures and the two inspected native captures. Runtime, evidence or relevant acceptance changes require fresh review.
