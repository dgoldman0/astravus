# First playable validation

Version 0.1.3 verified locally on September 4, 2026, using Ren'Py 8.5.3.26051504 on Linux, after the source, dialogue, parent-age, and scene-continuity pass.

| Check | Result |
| --- | --- |
| Ren'Py lint | Pass: 153 dialogue blocks, 1,655 words, 12 images, 18 screens; no script errors or warnings. |
| Native complete playthrough under Xvfb | Pass: 26 assertions covering title, First Memory without standing sprites, later home and garden, distinct gathering and construction locations, home return, rain image/audio, rollback to the dry room and garden audio, all scenes, manual save/load, history, larger text, solid dialogue background, reduced motion, people guide, completion, Continue, credits, and help. |
| Chromium WebGL complete playthrough | Pass: the running engine reports 0.1.3 and advances through all five scenes with real click/keyboard input. First Memory, home, gathering, construction, and rainy treehouse backgrounds are checked against the scene; the rain view coincides with rain audio and no standing sprites. Both friends' unlocks, Credits, title, page reload with existing saves, and Continue back to the ending pass. No JavaScript page errors or Ren'Py tracebacks. |
| Browser cache revalidation | Reproduced the old worker returning a deliberately stale cached response without reaching the server. The fixed worker fetches the current catalog, replaces the stale copy, and serves the refreshed copy when the browser goes offline. Regression included in `browser_smoke.py`. |
| Startup without WebGL | Original startup failure reproduced with `--disable-webgl`: video-mode initialization fails, followed by `NoneType.update` at the end-screen line despite no input. Fixed export displays a browser/desktop fallback before requesting the engine or game data; regression passes. |
| Screenshot review | Revised First Memory, home, construction, and rainy treehouse inspected with the reading overlay. All five adult faces and the baby remain clear; the construction light and outdoor rain are visible. Screenshot timing now waits for the home narration after the dissolve. Earlier review covered the planting area, shaded treehouse, title, large text, history, settings, people, and end screen. |
| Windows/Linux and macOS exports | Version 0.1.3 archives generated successfully. All 12 selected images match their provenance hashes; script, version and visual definitions match source. Font licenses are present; superseded First Memory, the Lumen panorama, unused art, SDK cache, development test cases, and web support sources are excluded. ZIP integrity checked. |
| Browser export and preview | `build/web.zip` and its nested game archive pass integrity checks. Runtime source and all selected image hashes match the project. Progressive images are delivered beside `game.zip`, whose placeholders refer to them. Build-specific game/bootstrap URLs and their offline catalog entries are present. Local preview serves 0.1.3 with the existing cache fix and `Cache-Control: no-store`. |
| Git boundaries | All new source and selected assets are under `visual-novel/`. Archives, SDK files, exports, test screenshots/state, compiled scripts, and logs are ignored. |
| Asset provenance | Selected image dimensions, color modes, SHA-256 hashes, prompts, reference relationships, and generated output IDs recorded in `assets.json`. |
| Story consistency | All 153 dialogue IDs are unique. Manual comparison restored Cali's eager response to Joren, Cassia's invitation, the familiar treehouse visit, the promise before the rainy passage, and Joren's wonder about talking trees. The premature panorama and explicit Lumen reveal wording are absent. The opening separates First Breath from the later household; the ending no longer implies that a particular seed's sunflower survived the whole childhood interval. Coverage, additions, omissions and age uncertainties are documented in `ADAPTATION.md` and `ART_DIRECTION.md`. |

Native test command:

```sh
python3 scripts/project.py test --headless
```

Browser test, after building and serving locally:

```sh
python3 scripts/project.py web
python3 scripts/project.py serve
# In another terminal; requires Playwright and its Chromium installation:
python3 scripts/browser_smoke.py
```

The native tests use separate state under `test-results/state/`. The browser test uses a fresh browser context. Browser inspection uses the engine's existing web bridge to observe state; the reading interactions are keyboard and mouse events. Test screenshots live in the ignored `test-results/screenshots/` directory.

The original browser test only covered a graphics-capable context and stopped on reaching the ending. It did not cover the embedded editor's unavailable WebGL context. The expanded test now detects both JavaScript errors and Ren'Py errors printed to the console, covers reload with retained browser saves, and separately verifies the no-WebGL startup path. The startup check is source-controlled in `web/startup.js`; `scripts/project.py web` installs it in the generated page, offline file catalog, and ZIP without changing the downloaded SDK.

The stale-cache issue was separate from the WebGL issue. Ren'Py's supplied worker modified immutable `FetchEvent` request headers; the resulting exception entered its offline fallback and returned an old cached response. `web/service-worker.js` copies the headers into a new request before conditional revalidation and waits for client claiming on activation. Startup checks for worker updates on every load. The exporter also versions the game and bootstrap URLs by build content, and the preview server sends `no-store`. A fresh preview query bypasses an index page already held by the old worker. Browser save storage is not cleared; the playthrough still resumes its completed save after reload.

Windows and macOS runtimes have not been launched on their target operating systems. The macOS package is unsigned. Mobile, Safari, self-voicing output, and audible playback have not been manually verified; the automated runs used headless displays. Art remains a first playable set with one pose per character and some visible sprite edge light, as documented in `ART_DIRECTION.md`.
