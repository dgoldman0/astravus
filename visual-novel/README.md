# Astravus — Seeds of Youth

Version **0.2.4** is a kinetic adaptation of **Book I: Seeds of Youth**, built in Ren'Py 8.5.3. Its 32 scenes follow Calista from her borrowed memory of First Breath through family life, childhood friendships, and the book's lasting aftermath. It ends before Book II's late-teen period. The story has one fixed outcome; the reader controls the pace. Allow about an hour, depending on reading speed and pauses.

This is the full-book production preview under development. It expands the earlier rough opening into the book's complete narrative arc; it is not a claim that every illustration, performance, or line has received final approval. The first rough playable draft, version 0.1.3, is preserved at commit `3dfcf6c` and documented in [Draft One](docs/DRAFT_ONE.md).

## Play

From this directory:

```sh
python3 scripts/project.py run
```

For a fresh checkout, first run `python3 scripts/project.py install` with Python 3.12 or later. The helper downloads the pinned SDK and web support from renpy.org, verifies SHA-256 checksums, and stores them in `.cache/`. Alternatively, open this directory in the Ren'Py launcher or set `ASTRAVUS_RENPY_SDK` to an existing SDK.

Choose **Begin Book I** for a fresh review of version 0.2.4. Click, Space, or Enter reveals and advances dialogue. The bottom bar provides history, save/load, automatic reading, skip, People, and settings. Mouse wheel up or Page Up rolls back; Escape opens the reading menu; H hides the interface. Settings offer larger dialogue, stronger contrast, reduced transitions, separate music/effects volume, and self-voicing where supported.

This development build also includes **Chapters** on the title screen and reading bar. All 32 scenes are available immediately; start at **24 · Which way we go** to read the restored source transition into **25 · The news**, or choose **26 · What comfort can do** for the family response. A jump begins at that scene and continues through the book, with the appropriate earlier encounters, ages, revelations and audio. It replaces the current reading position and clears its history; existing manual save slots remain available. Set `DEV_CHAPTER_SELECT = False` in `game/dev_chapters.rpy` before a release that should hide this control.

People entries follow the current reading's discoveries. Its Familiars section introduces Shadow the cat, Barkley the golden retriever, and Nibble the rat when they first appear in the home narration, with individual illustrated profiles. They also accompany the children visibly in seven scenes. Reading controls do not change events or unlock alternate outcomes. Scene checkpoints and manual saves retain progress. **Continue** and load slots accept this book's save format; older rough-draft saves are preserved but excluded from loading into the rewritten book. Development saves live in `.cache/state/`, with separate test state; packaged desktop games use Ren'Py's per-user save location, and browser saves stay in that browser.

After rebuilding and serving the browser version, open `http://127.0.0.1:8000/?preview=0.2.4`. A game already running in a tab does not replace itself when files are rebuilt. The fresh address also bypasses an old cached index page without clearing saved progress.

## Build and review

```sh
python3 scripts/project.py lint
python3 scripts/project.py test --headless   # Linux with Xvfb; omit --headless on a desktop
python3 scripts/project.py build             # Desktop packages in dist/
python3 scripts/project.py web               # Browser application and ZIP in build/
python3 scripts/project.py serve             # http://127.0.0.1:8000
python3 scripts/browser_smoke.py --url 'http://127.0.0.1:8000/?preview=0.2.4'
python3 scripts/check_assets.py
python3 scripts/audio_check.py
```

Desktop archives include the runtime. Extract the PC archive and launch `astravus-book-one.sh` on Linux or `astravus-book-one.exe` on Windows; the Mac archive contains an app bundle. Browser builds require HTTP and WebGL. Embedded editor previews may lack WebGL; the startup screen supplies an external-browser link when support is unavailable. Local exports are review artifacts, not published releases.

After both desktop ZIPs build successfully and pass integrity checks, the build helper removes older Astravus desktop exports from `dist/`. Browser builds replace `build/web/` and `build/web.zip`. Git retains source history; local release ZIPs do not accumulate with each version.

Build through `scripts/project.py web` to retain the startup and cache fixes. Game downloads have a build identifier, the service worker revalidates cached content online, and the local preview server sends `Cache-Control: no-store`. Saved progress is stored separately.

The automated review scripts exercise story progression and reading controls; browser checks also cover cache refresh and unsupported graphics. They produce review output under `test-results/`. Commands and test definitions are not proof of a passed build: see [VALIDATION.md](docs/VALIDATION.md) for the checks actually completed and platform limitations.

## Story, art, and sound

[Adaptation notes](docs/ADAPTATION.md) explain the source boundary, condensation, dialogue changes, and reveal order. The detailed [Book I coverage map](docs/BOOK_ONE_COVERAGE.md) includes the restored family episodes, friends' families, later projects and conflicts, loss, and remembrance. The source draft remains authoritative; the adaptation does not silently rewrite it or the wiki.

[Art direction](docs/ART_DIRECTION.md) and [character continuity](docs/CHARACTER_CONTINUITY.md) distinguish newborn, early-childhood, and later-childhood designs. Wardrobe and expressions change with activity and emotion. The sheltered treehouse retains its architecture and dark garden palette; brighter planting areas, rain, the festival, and remembrance have their own views. Generated images are selected working assets, with prompts, references, and hashes in [the original manifest](docs/assets.json), [character manifest](docs/character-assets.json), and [environment manifest](docs/environment-assets.json).

Audio uses the original score rendered with CC0 instrument samples, plus CC0 rain, water, and wooden recordings. The first flute lesson starts with one broken breath, then uses the original hesitant phrase when Cali attempts several notes. The later practice phrase uses sampled flute. Upgraded assets render at 48 kHz. The [audio direction](docs/AUDIO_DIRECTION.md) documents the sources, reproducible renderer, dependencies, and checks. Speaker portraits beside the dialogue identify main characters when action staging hides their standing sprites; they follow the current age, outfit, and grief state. People gives each human character an individual entry from their first spoken line, using a compact name list and the current reading's saved progress. Familiars use their narrated introduction. Their selected artwork and full prompts are recorded in [familiar-assets.json](docs/familiar-assets.json).

## Version control and generated files

| Path | Purpose | Git |
| --- | --- | --- |
| `game/*.rpy`, `game/ui/` | Story, interface, presentation, and development tests | Track |
| `game/images/`, `game/fonts/`, `game/audio/` | Selected runtime assets and notices | Track |
| `scripts/`, `docs/`, `web/`, `progressive_download.txt` | Reproducible workflow, provenance, and browser fixes | Track |
| `.cache/`, `.art-staging/`, `.venv/` | SDK, audio masters/encoder, local state, and unused candidates | Ignore |
| `dist/`, `build/`, `test-results/` | Packages, ZIPs, measurements, screenshots, and test state | Ignore |
| `*.rpyc`, `*.rpyb`, `game/cache/`, `game/saves/`, logs | Generated Ren'Py files | Ignore |

Keep production work in this subfolder and preserve focused, explained commits. Ren'Py ships with its license notices; Lato and DejaVu notices are in `game/fonts/`. This adaptation adds no new license to the author's story or original visual references.
