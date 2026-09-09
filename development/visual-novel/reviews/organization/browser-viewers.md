# Moved viewer review — September 9, 2026

The three local viewers pass in Chromium 148.0.7778.96, served over HTTP from the repository root. No broken local paths, JavaScript or console errors, failed requests, or external requests occurred in the completed check. All 102 recorded inputs existed, returned HTTP 200 to HEAD requests, and retained their SHA-256 hashes throughout the run.

| Viewer | Checked behavior | Visual finding |
| --- | --- | --- |
| [Curated character keys](../../../../visual-novel/art/character-keys/index.html) | All 17 characters and 20 sheets; embedded catalog equals `catalog.json`; Calista's two childhood stages together; 200% zoom/reset; Lyron's selected sheet; route reload; mobile character selection. | Both stages fit cleanly beside each other on desktop. On mobile, the selector, sheet, notes and source links remain readable without horizontal page overflow. Full-size links remain available for small sheet lettering. |
| [Nine-pair refinement study](../../art/character-refinements/review.html) | All nine original/selected pairs; all face/garment presets; 18 pixel comparisons showing split endpoints equal the corresponding single-image modes; reset; route reload; B/A/S keys; portrait, landscape and garment views at 390px width. | Split boundaries align with the source compositions. The face inset exposes the intended edit, and Lyron's garment comparison remains usable on mobile. Green sprite mattes are correctly explained as source-image backgrounds. |
| [Opening identity trial](../../art/opening-identity/review.html) | Original, Refined, Raw generation and Compare; slider endpoints and keyboard arrow; four face insets; both archived native captures; mobile mode changes. | Arin and Sage's paired insets are legible, and the native captures stack cleanly on mobile. The trial's dark presentation preserves enough contrast for controls and explanatory text. |

The comparison entry points are named `review.html`, not `index.html`. No path repair was needed. At the coordinator's request, both trial viewers now visibly identify their historical context and link the current curated keys. The opening's Original-mode description now says “Original artwork at the time of this trial.” The original comparison labels, images and trial rationale remain intact; the curated catalog was not changed.

All seven final browser captures were visually inspected: [key desktop](browser-keys-desktop.png), [key mobile](browser-keys-mobile.png), [comparison desktop](browser-comparisons-desktop.png), [face inset](browser-comparisons-detail.png), [comparison mobile](browser-comparisons-mobile.png), [opening desktop](browser-opening-desktop.png), and [opening mobile](browser-opening-mobile.png). The context notes fit without overlapping the controls.

Exact inputs, final HTML hashes, image dimensions, screenshot hashes, routes, browser version and checks are in [browser-viewers.json](browser-viewers.json). The executable [check script](browser-viewers-check.py) and [completed log](browser-viewers.log) are preserved alongside it. Run from the repository root:

```sh
python3 development/visual-novel/reviews/organization/browser-viewers-check.py
```

This review covers viewer loading, interactions and representative desktop/mobile layouts. The mobile check uses a 390 × 844 CSS viewport with desktop Chromium; it does not establish real-device touch behavior or Safari/Firefox compatibility. Linked documents were checked for availability, not re-audited for their prose. This does not replace the separate native Ren'Py tests or the completed character, scene and background visual reviews. Initial harness iterations cancelled image loads by reloading too early; the final script waits for loaded images and settled capture states.
