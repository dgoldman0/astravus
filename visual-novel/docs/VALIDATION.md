# Book I preview validation — 0.2.3

Verified locally on September 4, 2026, using Ren'Py **8.5.3.26051504** on Linux. The rough 0.1.3 preview and its original validation remain in commit `3dfcf6c`; this document covers the expanded Book I build with illustrated familiars, individual People entries, corrected flute staging, sampled audio and dialogue portraits.

| Check | Result |
| --- | --- |
| Script lint | Pass: **697 dialogue blocks, 7,894 words, 47 images, 18 screens**; no script warnings or errors. |
| Native complete playthrough | Pass: **96 assertions across all 32 scenes**, with the final Nibble design. Includes familiar discovery and illustrated profiles, save/load on both sides of their introduction, rollback and fresh-start reset, familiar staging and scene cleanup, individual People entries on the first spoken line, Cassia's encounter rollback and save/load, distinct Thalia/Lyron introductions, source-order reveals, three flute cues in story order, age/clothing, dialogue portraits, weather rollback, grief, reading settings, Credits and Continue. |
| Chromium full playthrough | Pass: **all 32 scenes in order**, all **14 individual People entries** opened and checked on their first spoken lines, **three illustrated familiar profiles** checked at their narrated introduction, familiar appearances in **seven scenes**, and all three flute cues in story order. Includes save/load, reveals, age/clothing, portraits, rain, grief, ending, Credits, reload and Continue with the complete human and familiar rosters; no engine/page errors. Nibble's final portrait and exploration appearance were visually reviewed in Chromium. |
| Cache and unavailable WebGL | Pass: stale cached content refreshes online and remains available offline. Unsupported WebGL shows the fallback before any engine/game download. |
| Image provenance | Pass: **47 selected images and 78 generation records** across four manifests. Files, dimensions, modes and SHA-256 hashes match. Selected generations, runtime definitions and stored reference chains resolve; no unlisted images remain in the runtime tree. Nibble's author-supplied reference is documented as a conversation attachment, without an available local source file. |
| Audio | Pass: all **19 delivered assets** decode correctly. Format, stereo content, DC, clipping, oversampled peak estimates, duration and loop boundaries pass. All thirteen compressed loops preserve their masters' frame counts. The new single attempt is 1.6 seconds at 24 kHz; the original hesitant phrase still matches its SHA-256 and plays later in the first lesson. Runtime audio totals **24.16 MiB**. |
| Audio provenance | Pass: **78 pinned source files**, including 73 VSCO instrument samples, the library license, and four environmental downloads, plus ten extracted archive members match their SHA-256 hashes. Every external source is CC0. Sources and uses are recorded in `audio-sources.json` and the bundled audio credits. |
| Native screenshot review | Inspected First Memory, family spaces, young and older children, weather, dome, grief and ending. Reviewed all three familiar portraits, their home, disagreement and painting appearances, and Nibble's final fluffy black-and-white design with violet/coral eyes. Matte backgrounds disappear in the game. Reviewed individual People entries for Maia, Selene and Lyron, with compact names on the left and readable profiles on the right. Reviewed dialogue portraits during flute, storytelling, rescue and rainy conversations. Text fits its panels. |
| Exports | Pass: **0.2.3 PC and Mac ZIPs, browser ZIP and nested game ZIP** pass CRC checks. All **79 relevant source/asset files** match the working tree: 19 audio files, 47 images, 12 runtime scripts and audio credits. Packaged READMEs also match. The PC package contains Windows and Linux launchers. Test scripts, source libraries, saves and development caches are excluded; Ren'Py includes its generated runtime bytecode and build metadata. |
| Source coverage | Compared against Book I of `revision/latest.md`, from First Breath through annual remembrance. Every mapped encounter, development, reveal and consequence is represented; inventories and recurring routines are condensed. No Book II events or alternate outcomes. See `BOOK_ONE_COVERAGE.md`. |
| Repository boundaries | Source, selected images and delivered audio are under `visual-novel/`. SDK downloads, masters, rejected art, builds, ZIPs, saves, compiled scripts, screenshots and test logs remain ignored. |

## Reproduce

From `visual-novel/`:

```sh
python3 scripts/project.py lint
python3 scripts/project.py test --headless
python3 scripts/check_assets.py
python3 scripts/audio_check.py
python3 scripts/project.py web
python3 scripts/project.py build
python3 scripts/project.py serve --port 8000
# Separate terminal, with Playwright and Chromium installed:
python3 scripts/browser_smoke.py --url 'http://127.0.0.1:8000/?preview=0.2.3'
```

Native tests run with separate state under `test-results/state/`. Browser tests use a fresh Chromium context, observe the running engine through its web bridge, and read using real keyboard/mouse input. They require the exact ordered 32-scene sequence, capture each scene, check both sides of the Lumen reveal, require the older Cassia before loss, and prohibit a live Joren portrait after his death. Spoken dialogue is checked for a visible actor or speaker portrait; key action scenes must exercise the portrait fallback. The test bridge sends ASCII Python source to preserve Unicode date and dialogue labels through the SDK's base64 transport. Rain checks allow the previous ambience's scheduled fadeout to finish. Screenshots, build logs and audio measurements are local ignored review artifacts in `test-results/`.

The People guide reserves “constellation” for the adults' partnership and uses “family” or “household” for the wider group. The browser test opens the guide on each speaker's first line, selects that person's button, and checks the displayed profile. Native tests also check that rollback removes an encounter, loading an earlier save restores the earlier roster, and loading the encounter save brings the entry back.

Familiars unlock from their first narrated introduction at home. Tests open all three illustrated profiles, check that the roster persists afterward, and require their scene appearances during First Memory, family routine, Tree of Echoes, waterwheel, construction exploration, treehouse disagreement and painting. Native tests verify familiar rollback, saves before and after discovery, scene cleanup and a fresh reading's empty familiar roster.

## Saves, startup and caching

Book I uses `Astravus-Book-I` as its save namespace and stamps saves with `astravus-book-one-v1`. Continue selects the newest compatible save; the load UI disables incompatible slots. The old preview's files are preserved. Scene autosaves wait for displayed dialogue so saved thumbnails and state reflect the new setting. Revelation and loss flags belong to the current reading and roll back or reset with it; completing the book does not spoil the next fresh reading's People guide.

The new roster reads the existing current dialogue history and completed scene progress, so compatible saves need no new unlock flags. Entries for the current scene follow actual speakers; completed scenes restore earlier encounters if the history is shortened. The title footer shows the running preview version.

The prior browser failures remain covered. Unsupported WebGL receives a useful fallback before any engine/game download. The service worker copies immutable request headers before revalidation, updates online, and retains the refreshed response for offline access. Startup checks for worker updates. The exporter gives game/bootstrap URLs a content-based build identifier; the local server sends `Cache-Control: no-store`. Browser save storage is not cleared. A tab already running the old engine still needs to navigate to the fresh preview address.

## Scope of verification

The automated runs verify function and presentation state, not literary or artistic finality. Dialogue, pacing and emotional balance still benefit from a full reading. Audio was decoded and measured here; it has **not** been subjectively certified by listening. The original score now uses recorded instruments; environmental recordings supply rain, water and wood. There are no voice performances or recorded crowds.

Windows and macOS packages are built and inspected, but have not been launched on their target operating systems. The Mac package is unsigned. Safari, mobile layouts, self-voicing output and physical speaker/headphone playback have not been manually verified. Character artwork has limited poses and expressions. Ten main speakers have dialogue portraits when their standing pose is hidden; Thalia, Lyron, Soren and Kaleb still lack dedicated artwork, and their dialogue keeps listeners visible. The rain is painted rather than animated. These are current preview limitations, not missing Book I plot events.
