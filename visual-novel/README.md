# Astravus — A Place to Begin

A playable, linear opening chapter built in Ren'Py 8.5.3. About 11 minutes: Calista plants a seed with Maia, meets Cassia and Joren, and finds a place with them in the treehouse. This adapts selected opening scenes from the Calista Arc; the player controls reading pace.

## Play

From this directory, on the development machine:

```sh
python3 scripts/project.py run
```

For a fresh checkout, first run `python3 scripts/project.py install` with Python 3.12 or later. This downloads the pinned SDK and web support from renpy.org, verifies SHA-256 checksums, and puts them in `.cache/`. You can also open this directory as a project in the Ren'Py launcher. Set `ASTRAVUS_RENPY_SDK` to use an existing SDK with the helper.

Click, Space, or Enter to reveal and advance dialogue. The bottom bar provides history, save/load, automatic reading, skip, a spoiler-free people guide, and settings. Mouse wheel up or Page Up rolls back. Escape opens the pause menu. Settings include larger dialogue, an opaque dialogue panel, reduced scene transitions, sound controls, and self-voicing where supported by the platform.

Development saves made by the helper live in `.cache/state/`; test saves are separate. Packaged desktop builds use Ren'Py's normal per-user save location. Browser saves belong to the browser's local storage.

To review version 0.1.3's revised dialogue, earlier-life parents, distinct locations, and rainy treehouse, open `http://127.0.0.1:8000/?preview=0.1.3` and choose **Begin the chapter**. The new preview address also bypasses an index page held by the older service worker. An already running game does not pick up rebuilt files automatically; Continue resumes an existing save.

## Build and verify

```sh
python3 scripts/project.py lint
python3 scripts/project.py test --headless   # Linux with Xvfb; omit --headless on a desktop
python3 scripts/project.py build             # Windows/Linux and macOS packages in dist/
python3 scripts/project.py web               # Browser application and ZIP in build/
python3 scripts/project.py serve             # http://127.0.0.1:8000
```

Desktop archives include the runtime; players do not need the SDK. Extract the PC archive and run `astravus-chapter-one.sh` on Linux or `astravus-chapter-one.exe` on Windows. The Mac archive contains an app bundle. Browser builds must be served over HTTP; opening `index.html` as a local file does not work. Exports are local artifacts, not published releases.

The browser version requires WebGL. Embedded editor previews may disable it; use a full browser or the desktop build in that case. The web build checks graphics support before loading the engine and displays an address/link to open externally when support is unavailable. Build through `scripts/project.py web` to include the startup and cache fixes: game downloads have a build identifier, the worker revalidates cached files online, and the local preview sends `Cache-Control: no-store`. Existing browser saves are kept.

The native playthrough exercises the whole chapter, manual save/load, history, settings, people entries, completion, and Continue. `python3 scripts/browser_smoke.py` tests a locally served browser build with Playwright/Chromium. Screenshots are written to `test-results/screenshots/`. See [validation notes](docs/VALIDATION.md) for the checks actually performed and platform limits.

## Project boundaries

| Path | Purpose | Git |
| --- | --- | --- |
| `game/*.rpy`, `game/ui/` | Story, interface, presentation, development test | Track |
| `game/images/`, `game/fonts/`, `game/audio/` | Selected runtime assets and font licenses | Track |
| `scripts/`, `docs/` | Reproducible workflow, provenance, adaptation notes | Track |
| `progressive_download.txt` | Ren'Py web asset-loading rules | Track |
| `web/` | Browser startup and cache fixes applied to each export | Track |
| `.cache/`, `.art-staging/` | Downloaded SDKs, archives, local state, unused art candidates | Ignore |
| `dist/`, `build/`, `test-results/` | Exported games, ZIPs, screenshots, test state | Ignore |
| `*.rpyc`, `*.rpyb`, `game/cache/`, `game/saves/`, logs | Generated Ren'Py files | Ignore |

The chapter is an adaptation in its own folder. The prose draft and wiki remain the source canon. [Adaptation notes](docs/ADAPTATION.md) identify source passages, additions, omissions, and the endpoint. [Writing notes](docs/WRITING_NOTES.md) document the researched dialogue approach. [Art direction](docs/ART_DIRECTION.md) records references and chronology, and [asset provenance](docs/assets.json) preserves generation prompts and selected files.

This is a first playable chapter with one pose per speaking character, seven environment backgrounds including the rain variant, and a dedicated First Memory family illustration. Designs are working selections for this build, pending author review. Audio is an original, procedurally synthesized ambient score and effects; regenerate it with `python3 scripts/make_audio.py` (NumPy required). No voice acting is included.

Ren'Py is distributed under its included third-party licenses. Lato and DejaVu notices are in `game/fonts/`. This work does not add a new license to the author's story or source artwork.
