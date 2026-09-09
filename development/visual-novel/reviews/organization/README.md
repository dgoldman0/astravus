# Organization and rebuild checks

The September 9, 2026 pass separates selected game materials from exploratory art and review history. The [development index](../../README.md) explains the new locations; [current validation](../../../../visual-novel/docs/VALIDATION.md) identifies the rebuilt packages and completed game checks.

The [preservation inventory](../../organization.json) maps 543 old paths to their retained destinations. [Preservation results](preservation.json) confirm all destinations exist, all 274 moved ordinary binary files retain their bytes, and all 20 selected key sheets remain unchanged. Six symlinks already had missing targets before the move; their exact originals were recovered from the recorded stash and their links repaired. The [recovery record](../../archive/recovered-proof.json) identifies all 31 recovered source files. Raw prompt text and historical source hashes remain historical evidence; mutable current review records are identified explicitly.

The game gallery now has only 40 files: 20 selected sheets, 17 character notes, its README, catalog and viewer. Exact earlier note wording remains recoverable in commit `b8e7918`. Ignored candidates stay ignored in the local development archive. All 30 active production recipes have recoverable inputs: 27 immutable Git-blob references and 46 retained file references; none of those required file inputs is ignored. An absent local experiment archive no longer prevents the graphics ledger from synchronizing.

## Relocation verification

- [Native GIMP reproduction](native-reproduction.json): the relocated opening, parent and supporting-character workflows reproduce five retained PNGs pixel for pixel in an isolated directory.
- [Actual browser viewer review](browser-viewers.md): 20 keys, nine comparison pairs, opening modes, deep links, split controls, keyboard navigation and mobile layout. All 102 local inputs load; no browser errors or broken paths.
- [Production script audit](script-audit.md): generated gallery links resolve outside the game directory, capture setup creates its missing parent directory, and review evidence remains confined to the game or its dedicated development workspace.
- [Asset guard](asset-check.log), [graphics status](graphics-status.log) and [regressions](regressions.log): current production provenance, explicit artistic findings and review invalidation checks.

## Rebuilt game verification

[Native full-book results](native-playthrough.log) record 156 passing assertions. [Rendered character measurements](native-framing-measurements.log) pass all 26 silhouettes. The [desktop build log](desktop-build.log), [web build log](web-build.log) and [export check](export-check.log) identify the rebuilt 0.1-alpha review artifacts and their exact 144-file payload comparisons. The [film review](../film.md) covers the separate rebuilt movie.

The [rebuild receipt](rebuild.json) binds the packages to their current runtime files and records the browser result as incomplete. The final [browser playthrough log](browser-playthrough.log) stops at scene 31: rain is queued while the preceding garden ambience continues beyond the 10-second check. A separate probe reproduces this handoff; the [rain diagnosis](browser-rain.md) distinguishes observed behavior from an unconfirmed SDK explanation. The final timeout [state](browser-final-timeout.json) and [frame](browser-final-timeout.png) are retained. No game audio or rain assertion was changed to make the check pass.

Earlier attempts exposed obsolete background expectations and synthetic pointer timing problems. Their raw logs remain diagnostic evidence, not passing full-game results. The repaired helper waits for the currently focused button’s exact label and membership in the current screen before sending a real click, with a small pointer movement when a menu reappears beneath an unmoved cursor. The [initial focus check](browser-click-focus.md) passed 40 clicks through eight opening-dialogue cycles; the [final closing-theme check](browser-closing-pointer.md) separately passes replay, pause, Escape, skip, credits and return to title. The full runner retains its scene, character, glossary, action, audio, save/load and chapter-jump assertions. Its remaining checks are not claimed as passed in the final combined run.

Ren'Py and encoder logs retain their original whitespace because their exact bytes are recorded as evidence. The standalone movie, packages and transient test screenshots remain generated outputs. Earlier release/audio approvals and target-platform launch claims are not renewed by this checkpoint.
