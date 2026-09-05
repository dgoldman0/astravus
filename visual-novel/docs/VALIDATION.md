# Book I alpha validation — 0.2.6

Verified locally on September 4, 2026, using Ren'Py **8.5.3.26051504** on Linux. The rough 0.1.3 preview and its original validation remain in commit `3dfcf6c`; this document covers the expanded Book I build with illustrated familiars, individual People entries, corrected flute staging, sampled audio and dialogue portraits.

Version 0.2.6 adds chapter spoiler warnings, a persistent setting, an itch link in the credits, and a separate hopeful afterword. The title now says **about 40–50 minutes**, based on the calculation in `ALPHA_0_2_6.md`, and identifies the build as an alpha. Story and images retain the 0.2.5 source and visual review. Audio is unchanged from 0.2.3; its measurements and provenance checks below are retained.

| Check | Result |
| --- | --- |
| Script lint | Pass: **667 dialogue blocks, 7,934 words, 54 images, 21 screens**; no script warnings or errors. |
| Native complete playthrough | Pass: **143 assertions across all 32 scenes**. Adds coverage of all 667 dialogue identifiers, warnings from title and reading menus, cancellation, confirmed jumps leaving earlier gaps unread, setting changes surviving loading, credits URL, author-handle removal, the afterword and Continue after finishing. Retains supporting portraits, festival poses, familiar/People discovery and rollback, save/load, scene cleanup, source-order reveals, flute cue order, ages, weather, chapter continuation and fresh-start reset. |
| Chromium full playthrough | Pass: **all 32 scenes in order**, all **14 individual People entries** opened and checked on their first spoken lines, **three illustrated familiar profiles** checked at their narrated introduction, familiar appearances in **seven scenes**, and all three flute cues in story order. Every spoken line requires its actual speaker to be depicted by a standing actor, portrait or applicable CG. Includes save/load, reveals, age/clothing, portraits, rain, grief, afterword, Credits, reload and Continue; no engine/page errors. |
| Chromium chapter selection | Pass: **all 32 jump destinations** match entrances recorded during ordinary reading, including dialogue, backgrounds, actors, People/familiar rosters, ages, loss and revelation flags. The picker also opens after completing, reloading, continuing and returning to title; the test waits for the title fade to finish before clicking. Reverse-order jumps remove later knowledge. |
| Chromium alpha controls | Pass: spoiler warning opens on an unread title-menu jump, Escape and Go back cancel without changing the reading position, confirmation permits the jump, skipped earlier chapters remain unread, and the completed-book flag cannot bypass gaps. Disabling warnings permits a direct jump. The setting survives a browser reload. Both credits and afterword buttons target the requested itch URL. |
| Cache and unavailable WebGL | Pass: stale cached content refreshes online and remains available offline. Unsupported WebGL shows the fallback before any engine/game download. |
| Image provenance | Pass: **54 selected images and 96 generation records** across four manifests. Files, dimensions, modes and SHA-256 hashes match. Selected generations, runtime definitions and stored reference chains resolve; no unlisted images remain in the runtime tree. Nibble's author-supplied reference is documented as a conversation attachment, without an available local source file. |
| Audio | Retained passing measurements: all **19 delivered assets** decode correctly. Format, stereo content, DC, clipping, oversampled peak estimates, duration and loop boundaries pass. All thirteen compressed loops preserve their masters' frame counts. The single attempt is 1.6 seconds at 24 kHz; the original hesitant phrase plays later in the first lesson. Runtime audio totals **24.16 MiB**. This pass verifies their packaged bytes and cue order; it does not claim a new listening assessment. |
| Audio provenance | Retained passing audit: **78 pinned source files**, including 73 VSCO instrument samples, the library license, and four environmental downloads, plus ten extracted archive members match their SHA-256 hashes. Every external source is CC0. Sources and uses are recorded in `audio-sources.json` and the bundled audio credits. |
| Visual review | Inspected the alpha title, spoiler dialog, Settings, credits link and afterword at native and browser sizes. Retain the complete 0.2.5 artwork review: shared plaza architecture/crowds, three Cassia variants, four supporting parents, pond/waterwheel, familiar placement and festival poses. See `REVIEW_0_2_5.md` for those scene-by-scene findings. |
| Exports | Pass: **0.2.6 PC and Mac ZIPs, browser ZIP and nested game ZIP** pass CRC checks. All **87 relevant source/asset files** match the working tree: 19 audio files, 54 images, 13 runtime scripts and audio credits. The chapter picker, warning and afterword are included. Packaged READMEs also match. The PC package contains Windows and Linux launchers. Test scripts, source libraries, saves and development caches are excluded; Ren'Py includes its generated runtime bytecode and build metadata. |
| Source coverage | Compared all 32 scenes against Book I of `revision/latest.md`, from First Breath through annual remembrance, and checked supporting biographies and expanded dialogue. Eight paragraphs from the familiars' intervention through the first grief are reverified verbatim and in source order, with reading-beat and italics formatting adapted for the VN. This includes the closing reflection on friendship and the opening turn toward unforeseen tragedy across scenes 24–25. No Book II events or alternate outcomes. See `BOOK_ONE_COVERAGE.md` and `REVIEW_0_2_5.md`. |
| Repository boundaries | Source, selected images and delivered audio are under `visual-novel/`. SDK downloads, masters, rejected art, builds, ZIPs, saves, compiled scripts, screenshots and test logs remain ignored. |
| Build retention | Pass: the desktop helper checks both new ZIPs before removing older Astravus exports. The 0.2.6 build replaces the superseded 0.2.5 pair; subsequent builds overwrite the same 0.2.6 filenames. Only the current PC and Mac ZIPs remain in `dist/`. Earlier temporary-directory checks cover corrupt/missing-package protection and preservation of unrelated or newer ZIPs. No before/after artwork copies are added to the repository. |

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
python3 scripts/browser_smoke.py --url 'http://127.0.0.1:8000/?preview=0.2.6'
```

Native tests run with separate state under `test-results/state/`. Browser tests use a fresh Chromium context, observe the running engine through its web bridge, and read using real keyboard/mouse input. They require the exact ordered 32-scene sequence, capture each scene, check both sides of the Lumen reveal, require the older Cassia before loss, and prohibit a live Joren portrait after his death. Spoken dialogue requires the actual speaker's depiction; a visible listener alone does not pass. Key action scenes must exercise the portrait fallback. The test bridge sends ASCII Python source to preserve Unicode date and dialogue labels through the SDK's base64 transport. Rain checks allow the previous ambience's scheduled fadeout to finish. Screenshots, build logs and audio measurements are local ignored review artifacts in `test-results/`.

The People guide reserves “constellation” for the adults' partnership and uses “family” or “household” for the wider group. The browser test opens the guide on each speaker's first line, selects that person's button, and checks the displayed profile. Native tests also check that rollback removes an encounter, loading an earlier save restores the earlier roster, and loading the encounter save brings the entry back.

Familiars unlock from their first narrated introduction at home. Tests open all three illustrated profiles, check that the roster persists afterward, and require their scene appearances during First Memory, family routine, Tree of Echoes, waterwheel, construction exploration, treehouse disagreement and painting. Native tests verify familiar rollback, saves before and after discovery, scene cleanup and a fresh reading's empty familiar roster.

## Saves, startup and caching

Book I uses `Astravus-Book-I` as its save namespace and stamps saves with `astravus-book-one-v1`. Continue selects the newest compatible save; the load UI disables incompatible slots. The old preview's files are preserved. Scene autosaves wait for displayed dialogue so saved thumbnails and state reflect the new setting. Revelation and loss flags belong to the current reading and roll back or reset with it; completing the book does not spoil the next fresh reading's People guide.

The new roster reads the existing current dialogue history and completed scene progress, so compatible saves need no new unlock flags. Entries for the current scene follow actual speakers; completed scenes restore earlier encounters if the history is shortened. The title footer shows the running preview version.

Chapter selection reconstructs earlier scene state for the selected destination. It clears the old history and call stack, sets a rollback boundary, restores ages and revelation flags, and supplies inherited music. Family episodes retain their normal continuation after a jump and after save/load. Manual saves remain available; subsequent autosaves follow the new reading position. `DEV_CHAPTER_SELECT` remains enabled in both native and exported builds. The browser test records entrances during normal reading, then visits all 32 destinations in reverse order and compares their dialogue, backgrounds, actors, People/familiar rosters and story state with those entrances.

Spoiler warnings use the engine's separate persistent record of viewed dialogue. Neither a fabricated earlier scene list nor reaching the ending marks skipped chapters as read. The default is On, with an immediately saved Settings toggle. Tests also cover going back to the same reading position from the modal warning, gaps after a confirmed jump, and existing viewed dialogue remaining available across reloads. The chapter selector's reading record is not used to reveal People entries in a new or earlier reading.

The prior browser failures remain covered. Unsupported WebGL receives a useful fallback before any engine/game download. The service worker copies immutable request headers before revalidation, updates online, and retains the refreshed response for offline access. Startup checks for worker updates. The exporter gives game/bootstrap URLs a content-based build identifier; the local server sends `Cache-Control: no-store`. Browser save storage is not cleared. A tab already running the old engine still needs to navigate to the fresh preview address.

## Scope of verification

The automated runs verify function and presentation state, not literary or artistic finality. This pass also includes a source comparison and visual review; the preview remains open to the author's judgment of pacing and emotional balance. Audio was previously decoded and measured; it has **not** been subjectively certified by listening. The original score uses recorded instruments; environmental recordings supply rain, water and wood. There are no voice performances or recorded crowds.

Windows and macOS packages are built and inspected, but have not been launched on their target operating systems. The Mac package is unsigned. Safari, mobile layouts, self-voicing output and physical speaker/headphone playback have not been manually verified. Character artwork has limited poses and expressions; all fourteen speakers now have dialogue portraits when their standing pose is hidden. The rain is painted rather than animated. These are current preview limitations, not missing Book I plot events.
