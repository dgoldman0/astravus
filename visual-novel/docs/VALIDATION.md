# Book I preview validation — 0.2.0

Verified locally on September 4, 2026, using Ren'Py **8.5.3.26051504** on Linux. The rough 0.1.3 preview and its original validation remain in commit `3dfcf6c`; this document covers the expanded Book I build.

| Check | Result |
| --- | --- |
| Script lint | Pass: **697 dialogue blocks, 7,894 words, 44 images, 18 screens**; no script warnings or errors. |
| Native complete playthrough | Pass: **60 assertions across all 32 scenes**. Includes title and ending, manual save/load, history, larger text, solid dialogue panel, reduced motion, People, source-order reveals, changed child stages and clothing, both flute cues, dry/rain rollback and audio, grief state, Credits, Continue and fresh-start reset. |
| Chromium full playthrough | Pending final exported-build run. |
| Cache and unavailable WebGL | Pending final exported-build run. |
| Image provenance | Pass: **44 selected images and 68 generation records** across the three manifests. Files, dimensions, modes and SHA-256 hashes match. Selected generations, runtime definitions and complete reference chains resolve; no unlisted images remain in the runtime tree. |
| Audio | Pass: all **18 delivered assets** decode correctly. Format, stereo content, DC, clipping, oversampled peak estimates, duration and loop boundaries pass. All thirteen compressed loops preserve their masters' frame counts; the report records exact hashes and measurements. |
| Native screenshot review | Inspected First Memory, family spaces, young and older children, dry/rain treehouse, Tree of Echoes, finished water wheel, construction-room blueprint, dome summit, grief, mural and ending. Text fits the reading panel. Age and outfit changes are visible. Pose conflicts during rescue, flute playing, embraces and brush-washing are avoided by hiding standing portraits. |
| Exports | Pending final package integrity and source/hash checks. |
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
python3 scripts/browser_smoke.py --url 'http://127.0.0.1:8000/?preview=0.2.0'
```

Native tests run with separate state under `test-results/state/`. Browser tests use a fresh Chromium context, observe the running engine through its web bridge, and read using real keyboard/mouse input. They require the exact ordered 32-scene sequence, capture each scene, check both sides of the Lumen reveal, require the older Cassia before loss, and prohibit a live Joren portrait after his death. Screenshots, build logs and audio measurements are local ignored review artifacts in `test-results/`.

## Saves, startup and caching

Book I uses `Astravus-Book-I` as its save namespace and stamps saves with `astravus-book-one-v1`. Continue selects the newest compatible save; the load UI disables incompatible slots. The old preview's files are preserved. Scene autosaves wait for displayed dialogue so saved thumbnails and state reflect the new setting. Revelation and loss flags belong to the current reading and roll back or reset with it; completing the book does not spoil the next fresh reading's People guide.

The prior browser failures remain covered. Unsupported WebGL receives a useful fallback before any engine/game download. The service worker copies immutable request headers before revalidation, updates online, and retains the refreshed response for offline access. Startup checks for worker updates. The exporter gives game/bootstrap URLs a content-based build identifier; the local server sends `Cache-Control: no-store`. Browser save storage is not cleared. A tab already running the old engine still needs to navigate to the fresh preview address.

## Scope of verification

The automated runs verify function and presentation state, not literary or artistic finality. Dialogue, pacing and emotional balance still benefit from a full reading. Audio was decoded and measured here; it has **not** been subjectively certified by listening. The score is original stylized synthesis, with no voice performances or recorded crowds.

Windows and macOS packages are built and inspected, but have not been launched on their target operating systems. The Mac package is unsigned. Safari, mobile layouts, self-voicing output and physical speaker/headphone playback have not been manually verified. Character artwork has limited poses and expressions; some speakers remain offscreen. The rain is painted rather than animated. These are current preview limitations, not missing Book I plot events.
