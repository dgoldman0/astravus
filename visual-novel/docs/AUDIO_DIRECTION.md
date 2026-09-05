# Book I audio direction

Version **0.1-alpha** expands the instrumental score to **15 core compositions and nine variations**: 24 cues with approximately 38 minutes of musical material. The scope covers all 32 chapters and their documented subscenes. Established themes receive longer forms, contrasting passages, and new arrangements; additional themes distinguish observing, making, storytelling, friendship, exploration, painting, and shared grief. The music is rendered with CC0 recorded instruments.

Rain, water, and wood use selected CC0 recordings; soft room air and the quiet festival pulse remain original synthesis. The flute lesson begins with one broken breath, then uses the original hesitant phrase when the narration reaches several notes. The optional vocal closing theme is the author's **Curiosity and Discovery**, created by Daniel Goldman with assistance from ChatGPT and SUNO. Story dialogue is not voiced. NumPy, SciPy, SoundFile, and FFmpeg are build/checking dependencies. Music and ambience ship as Ogg Vorbis; six short effects remain PCM WAV. Ren'Py plays these files directly.

The original **First Light** motif remains recognizable: C–D–E–G–C–A–G–C. Its arrangement uses answering phrases, overlapping harmony, a low register, and a small stereo room. The score shares this musical vocabulary across the book, but each cue changes its density, register, rhythm, and harmonic emphasis. This is intended to give scenes continuity without putting the same unchanging loop underneath every emotion.

## Score structure and cue sheet

[score-cue-sheet.md](score-cue-sheet.md) records every cue's musical purpose and
the exact entrances, changes, and exits across all 32 chapters.
[score-catalog.json](score-catalog.json) records titles, duration, tempo, meter,
sections, instrumentation, variation relationships, and loudness targets. Those
values come from the editable notation in `scripts/score_material.py`,
`scripts/score_new_material.py`, and `scripts/score_catalog.py`.

Most core compositions have 32 bars: an eight-bar statement, an instrumental
answer, a contrasting middle, and a varied return. The festival has a 48-bar
dance form with an interlude. Variations have three eight-bar sections and change
the lead, texture, tempo, articulation, or ordering of melodic material. The
palette includes 3/4, 4/4, and 6/8, notated rests, offbeat phrases, harmonic
inversions, and answering instrumental lines. Different scenes therefore have
different kinds of musical motion, not only different levels of sustained sound.

| Musical role | Core compositions | Related variations |
| --- | --- | --- |
| Beginning and curiosity | `first_light`, `discovery_theme`, `wonder_theme` | `discovery_careful` |
| Home and shelter | `home_theme`, `rain_refuge` | `home_tender`, `home_evening` |
| Observing, making, and exploring | `garden_growth`, `workshop_play`, `outward_paths` | `workshop_success` |
| Stories and friendship | `storytelling`, `friendship_theme` | `storytelling_lullaby`, `friendship_play`, `friendship_warm` |
| Festival | `festival_theme` | `festival_lanterns` |
| Grief, activity, and remembrance | `grief_theme`, `painting_theme`, `shared_grief`, `remembrance_theme` | `remembrance_rain` |

All instrumental cues loop. Notes and reverb tails wrap into the start of the
file; there is no baked-in fade to silence. The script changes music at
reader-reached beats and uses sequential fade-outs and fade-ins on the music
channel. It does not guess reading speed or promise simultaneous crossfades.
A loop's entire form must remain emotionally appropriate to its current
subscene. Musical development does not authorize announcing the next story beat.

## Sound and scene consistency

| File | Length | Use |
| --- | ---: | --- |
| `garden_air.ogg` | 32 s loop | Recorded water with a soft synthesized air bed. No recognizable Earth bird calls. |
| `room_air.ogg` | 32 s loop | Very quiet interior air and the home's wall fountain. No mechanical ship hum. |
| `workshop_air.ogg` | 32 s loop | Quiet room air with irregular recorded wooden contacts. No heavy machinery. |
| `plaza_air.ogg` | 32 s loop | Quiet air with occasional subdued recorded wooden movement. It contains no speech or simulated spoken language. |
| `rain.ogg` | 32 s loop | A continuous field recording of rainfall, edited into a seamless loop. Start with the rain background and stop when the weather/setting changes. |
| `wood.wav` | 0.75 s | A small wooden contact, such as a ladder or treehouse movement. Avoid playing it on every click. |
| `tree_creak.wav` | 6.58 s | A low wooden flex for the Tree of Echoes. Not a voice, monster cue, or danger warning. |
| `water_splash.wav` | 0.42 s | A shallow splash for the pond incident. No implication of a deep-water drowning. |
| `flute_attempt.wav` | 1.6 s | One short breath briefly catches a C, thins into air, and breaks. Plays before “There was a note in there.” Stops as Cali lowers the flute and responds. |
| `flute_first.wav` | 8 s | The original hesitant C–D–E and returning C, unchanged. Plays later in the first lesson at “We went a few notes at a time.” |
| `flute_practice.wav` | 12 s | A connected C–D–E–G–C–A–G–C phrase, showing musical progress through audible phrasing rather than narration alone. |

The flute sounds are story events. The background score fades out before them;
an immediate stop before each actual performance finishes any pending fade if
the reader advances rapidly. The existing effect stops follow Calista lowering
the flute or ending the phrase. There is no mandatory full-performance wait.
Sound settings still govern these cues. The Tree of Echoes and pond splash have
the same protection from a remaining score fade.

Music, ambience, and effects stay on their existing Ren'Py channels so the reader can adjust them. At the current default music volume of 0.32 and sound volume of 0.4, the environmental layers are deliberately quiet, with rain more present than room tone. Keep silence available, especially at the death notification and the first stunned responses. Narrative cue starts use `if_changed`: adjacent scenes sharing a cue continue it without a restart or fade dip. A new cue still uses its stated fade.

The delivery inventory is 36 audio files: 24 instrumental cues, five ambience
loops, six effects, and the supplied closing song. FFmpeg's EBU R128 meter
measures actual program loudness, and the audit applies the gains specified by
the game. Ordinary score targets range from −22.5 to −21.5 LUFS; reflective cues
target −24 LUFS, and the two grief cues target −26 LUFS. The renderer meters each
cue, applies its declared target, controls peaks with linked stereo gain, and
meters the encoded result. These are composition-specific dynamic groups, not a
single normalization target. Actual delivered measurements belong in
`test-results/audio-report.json`.

The original hesitant flute phrase plays at `volume 0.75` (−2.5 dB). Its unchanged
file measures approximately −19.3 LUFS at that gain before the reader's sound
setting, close to the later practice phrase at −19.0. The short broken first
breath remains quieter at −21.5 LUFS. Their notes, timing, timbre, and WAV files
are unchanged by the score expansion.

The closing song is mastered at −14.7 LUFS. Its dedicated music channel applies a −6 dB track gain from `closing_theme.json`, placing it at −20.7 LUFS, close to the preceding home theme's −21.5 LUFS target. The source WAV, runtime Ogg, and standalone MP4 retain the supplied mastering; the gain is specific to playback within the game's quieter mix. Music settings still apply. [Listen on SUNO](https://suno.com/s/IoZ3kzpqJBFXAgJJ).

## Sources and rendering

Every downloaded instrument and environmental recording is explicitly CC0. [audio-sources.json](audio-sources.json)
records the author, source page, download URL, SHA-256, byte size, and pinned VSCO
commit (`440300901dfe9275fd84e0b7763af1f8443ae62e`). The shipped
[audio credits](../game/audio/README.md) identify the recordings and their uses. The author-supplied closing song is a separate source, documented in [closing-theme-audio.json](closing-theme-audio.json).

The instrument set uses 73 source samples from [VSCO 2 Community Edition](https://versilian-studios.com/vsco-community/):
harp, the soft layer of Upright Nr1, sustained cello/viola ensembles, and flute.
The local sampler selects a nearby recorded note, resamples with an antialiasing
filter, preserves stereo information, shapes releases, and crossfades sustained
bowing. Short bowed gestures preserve the recorded attack and release within
their notated length; longer notes use the sampler's sustained bowing. VSCO uses different octave naming conventions for harp/piano and
strings/woodwinds; the mapping is explicit in the sampler and was checked against
recorded pitches.

The final mixes use 48 kHz processing and 24-bit WAV masters. Instrument positions
remain fixed. Small deterministic timing and velocity differences phrase the
notated parts while bass downbeats stay anchored. Brief, linked stereo gain
reduction controls recorded attacks; the per-cue render record reports the
maximum reduction. A dense, damped stereo room response adds depth. Its impulse
is synthesized locally; no external reverb recording is required.
The old blanket 6.5 kHz rolloff is removed from the upgraded assets. These
changes preserve the recordings' detail; resampling does not create detail that
was absent from a source. Rain's original published source is already Vorbis.

For rain and water beds, overlapping the recording's ends produces a continuous
loop without a fade to silence. Wood contacts and the shallow pond splash use
recorded effects. Mono wooden sounds are positioned and given a small room tail;
they are not described as native stereo recordings. Rain stays a separate channel
from the music so the game's existing weather transitions and rollback apply.

**The tentative flute cues use 24 kHz synthesis:** `flute_attempt.wav` is a brief,
breathy failed note. The original `flute_first.wav` is unchanged; its SHA-256 in
the source manifest protects that deliberate beginner performance. The script
places it after the initial single-note exchange, when Cali attempts several
notes. The later practice phrase uses a sampled instrument with the original
note sequence and timing. Both early cues remain deliberately unpolished.

## Reproduce

Run from `visual-novel/` with NumPy and SciPy available. SoundFile is installed
locally; `7z` or `7zz` is needed once to unpack the water-splash source archive:

```sh
python3 -m pip install --target .cache/audio-tools soundfile==0.13.1
python3 scripts/make_audio.py --fetch-sources
python3 scripts/compose_score.py
python3 scripts/audio_check.py
```

The fetch step downloads only the manifest's pinned CC0 files, checks their
SHA-256 hashes, and extracts known audio members. Originals live in
`.cache/audio-sources/`; masters live in `.cache/audio-masters/`. Neither goes
into the game package. The score renderer uses cached, verified samples offline;
it does not write environmental effects, the flute lesson, or the closing song.
It uses the cached FFmpeg from the theme-video tools by default; supply
`--ffmpeg /path/to/ffmpeg` to select another binary. To render selected cues or
refresh the notation catalog without audio rendering:

```sh
python3 scripts/compose_score.py garden_growth friendship_warm
python3 scripts/compose_score.py --catalog-only
python3 scripts/make_audio.py --encode-existing first_light
```

`make_audio.py` delegates score rendering to `compose_score.py` and retains the
existing ambience/effect renderer. For example, `python3 scripts/make_audio.py
first_light rain` rebuilds one score cue and one ambience loop. A full invocation
also regenerates the legacy effects; use the score-only command above for this
polish. Editable MIDI review files go to `.cache/score-midi/`, and per-cue render
measurements go to `.cache/score-render/`. Neither is a runtime dependency.

The encoder remains SoundFile 0.13.1 / libsndfile 1.2.2, with Vorbis
`compression_level=0.15`. Writes use 8,192-frame blocks because a single large
48 kHz write crashed this libsndfile build. Encoding uses a temporary file and
replaces the runtime file only after a successful close. Ogg serial numbers and
page checksums are made deterministic without altering compressed audio packets.

## Validation and listening

`audio_check.py` decodes all 36 delivered assets and checks sample rate,
codec/PCM subtype, stereo content, duration, DC, sample and reconstructed peaks,
loop seams, and frame/level agreement with cached masters. It also checks the
first flute against its preserved hash. The closing song is checked against its provenance and full source duration. FFmpeg EBU R128 measurements, script gains, estimates at the default mixer settings, and related-cue balance checks are included in `test-results/audio-report.json`. The cached FFmpeg installed for the theme renderer is supported; `--ffmpeg /path/to/ffmpeg` selects another installation.

The renderer and checks do not provide a human listening verdict. Source checks
verify chapter entry, actual cue use, and protected narrative timing; native
playback checks exercise those states in Ren'Py. These supplement the decoded
audio measurements. They cannot establish that a melody feels right beside the
prose.

This score pass has a fixed scope: the 24 cues and triggers in the catalog and
cue sheet. After rendering and targeted verification, use the existing Chapters
screen for a short review route:

1. **04:** the workshop spill, silence, and shared cleanup.
2. **12:** public celebration changing into personal lantern wishes.
3. **18–20:** imaginative maps, rain shelter, constructing the wheel, and its
   actual first turn.
4. **24–29:** disagreement and restored warmth, the silent news, distinct family
   grief, painting, shared grief, and the quiet memorial speech.
5. **31–32:** rain and another drawing, annual remembrance, then the hopeful
   afterword and optional vocal song.

Read normally and linger on a few early and late lines to hear the loop remain
appropriate. Git preserves earlier audio versions; do not retain separate
historical copies or comparison exports. Raw sample libraries, masters, and MIDI
files are excluded from exported games. Public versioning remains **0.1-alpha**.
