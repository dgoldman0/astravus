# Browser audio handoff repair

The garden-to-rain handoff is fixed in the web package rebuilt on **September 9, 2026 at 10:22:47 AM EDT**. The subsequent complete Chromium playthrough passes all 32 scenes and all 32 reverse chapter jumps, including rain, manual save/load, closing-theme controls, Credits, reload/Continue, cache refresh and the unsupported-graphics fallback. The [full log](browser-playthrough.log), [focused audio result](current/browser-audio.json) and [rebuild receipt](rebuild.json) identify the tested package.

The previous [ten-second failure](../../organization/browser-rain.md) was reproduced with an observational trace of the actual browser backend. Its fadeout branch could promote a queued copy of the outgoing loop while that track was still decoding or waiting for synchronized playback. It then returned without stopping the promoted loop. Garden ambience continued while rain waited; synchronized music could also remain waiting. The [stock trace](stock/browser-rain-probe.json) records the outgoing garden track at position zero both before and after the fadeout call.

The build now inserts a small compatibility guard into the exported copy of Ren'Py 8.5.3's `renpy/common/_audio.js`: if an audio track has not started, a fadeout request stops it and clears its queued repeat. Running tracks retain the original fadeout behavior, including fades spanning a loop boundary; video handling remains unchanged. The downloaded SDK, story, audio files, visual assets and native packages are unchanged. The guard is applied before the web cache identifier is calculated, so clients receive the corrected engine with the new build.

[project.py](../../../../../visual-novel/scripts/project.py) checks the entire original engine file's SHA-256 before applying the guard and rewrites `game.zip` through a temporary archive. An unknown SDK source stops the build for review. [check_release.py](../../../../../visual-novel/scripts/check_release.py) now verifies that the final web ZIP actually contains the exact corrected engine file in addition to checking the 144 game/README files and archive integrity. All three existing desktop/web artifacts still match their game source; this follow-up rebuild changes the web package only.

The [focused browser check](../../../../../visual-novel/scripts/browser_audio_check.py) loads the actual packaged engine and confirms its hash before testing:

- **Rapid advancement, reduced motion:** the outgoing garden track is cleared at position zero; both rain and the remembrance score have positive playback positions within 3.21 seconds of observing the rainy scene.
- **Normal scene fades:** garden is already playing at 8.50 seconds when its two-second fadeout is requested. It remains active immediately afterward, demonstrating that the guard preserves the fade. Both replacement tracks are playing within 3.95 seconds of observing the rainy scene.
- **Save/load in both cases:** save at the treehouse, advance to the plaza's different ambience, then load through the real menus. The same dialogue, rain and remembrance score return.

These are playback-state and fade-scheduling checks, not a new subjective listening approval. The two measured delays include the test's polling overhead. [Regression results](regressions.log) pass all 67 tests. The new [engine regression tests](../../../../../visual-novel/tests/test_web_audio.py) execute the actual original and patched fadeout functions in Node: the original reproduces the pending-loop error; the guard clears it while retaining running fades, loop-boundary fades and video behavior. Archive tests cover metadata preservation, SDK drift and interrupted writes.

Exploratory evidence remains here. The [loop-setting probe](tight/browser-rain-probe.json) also avoided the failure, but changing loop behavior globally was not adopted. The [play-wrapper probe](guard/candidate-probe.log) failed inside its temporary diagnostic wrapper before reaching the scene and supplies no candidate result. The first focused runner stopped after reaching rain because its diagnostic import was scoped incorrectly; [that error](probe-import-error.log) is retained separately from the completed [audio log](browser-audio.log). No game criterion was relaxed in the final checks.

The [pre-fix ZIP](../../../archive/local/web-before-audio-fix.zip) is preserved in the ignored development archive with its original checksum recorded in [before.json](before.json). The selected version remains `0.1-alpha`; this repair does not change older release or platform approvals.

To repeat against a locally served build, from `visual-novel/`:

```sh
python3 -m unittest discover -s tests
python3 scripts/project.py web --review-build
python3 scripts/check_release.py --review-build
python3 scripts/browser_audio_check.py
python3 scripts/browser_smoke.py --url 'http://127.0.0.1:8000/?preview=0.1-alpha'
```
