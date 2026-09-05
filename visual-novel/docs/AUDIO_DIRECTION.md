# Book I audio direction

Version 0.2.2 keeps the original instrumental compositions and renders them with CC0 recorded instruments. Rain, water, and wood use selected CC0 recordings; soft room air and the quiet festival pulse remain original synthesis. The flute lesson begins with one broken breath, then uses the original hesitant phrase when the narration reaches several notes. There are no borrowed melodies, Suno tracks, or voice performances. NumPy, SciPy, and SoundFile are build dependencies, not runtime dependencies. Music and ambience ship as Ogg Vorbis; six short effects remain PCM WAV. Ren'Py plays these files directly.

The original **First Light** motif remains recognizable: C–D–E–G–C–A–G–C. Its arrangement uses answering phrases, overlapping harmony, a low register, and a small stereo room. The score shares this musical vocabulary across the book, but each cue changes its density, register, rhythm, and harmonic emphasis. This is intended to give scenes continuity without putting the same unchanging loop underneath every emotion.

## Cue sheet

| File in `game/audio/` | Length | Dramatic use and arrangement |
| --- | ---: | --- |
| `first_light.ogg` | 64 s | Welcome, First Breath, and the opening act of remembering. Gentle plucked motif, slowly changing bowed harmonies, and room for the prose. |
| `home_theme.ogg` | 66 s | The family home, meals, and ordinary affection. Soft upright-piano melody, soft broken chords, and modest answering variations. |
| `discovery_theme.ogg` | 49 s | Workshop discoveries, friends' projects, and collaborative play. More movement in the plucked figures, with a lighter sustained layer. |
| `wonder_theme.ogg` | 77 s | Sage's story and the Tree of Echoes. Spacious suspended harmony and occasional quiet flute answers; no sudden orchestral reveal. |
| `festival_theme.ogg` | 46 s | Festival of Lights. A livelier plucked arrangement, answering flute, and restrained wooden pulse. The pulse supplies movement without turning the gathering into a march. |
| `rain_refuge.ogg` | 70 s | The shelter of the treehouse and quieter conversations. Sparse upright-piano phrases with soft minor-coloured harmonies; rain remains a separate environmental layer. |
| `grief_theme.ogg` | 80 s | The aftermath of Joren's death. Long gaps in the melody, low soft support, and no swell or emphatic cadence. Let the news arrive in silence before using it. |
| `remembrance_theme.ogg` | 71 s | Shared remembering and the closing movement of Book I. Returns to First Light's contour with changed harmony and a quieter register. Affection and loss coexist; the arrangement avoids a victory finish. |

All music cues loop. The lengths above are rounded; the renderer places eight two-bar phrases on each cue's tempo grid. Phrases change across the loop rather than repeating one bar for a minute. Notes and reverb tails wrap into the start of the file. The loop therefore has no baked-in fade to silence; Ren'Py should fade music at entrances, exits, and scene changes.

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

The flute sounds are story events. Fade out the background music before them; let each phrase continue across text where possible, then return to the score. Avoid a mandatory long wait that punishes a quick reader. Sound settings still govern these cues.

Music, ambience, and effects stay on their existing Ren'Py channels so the reader can adjust them. At the current default music volume of 0.32, the environmental layers are deliberately quiet, with rain more present than room tone. Keep silence available, especially at the death notification and the first stunned responses. A change of scene does not always need a change of music; change it when the emotional or physical setting warrants it.

## Sources and rendering

Every external audio source is explicitly CC0. [audio-sources.json](audio-sources.json)
records the author, source page, download URL, SHA-256, byte size, and pinned VSCO
commit (`440300901dfe9275fd84e0b7763af1f8443ae62e`). The shipped
[audio credits](../game/audio/README.md) identify the recordings and their uses.

The instrument set uses 73 source samples from [VSCO 2 Community Edition](https://versilian-studios.com/vsco-community/):
harp, the soft layer of Upright Nr1, sustained cello/viola ensembles, and flute.
The local sampler selects a nearby recorded note, resamples with an antialiasing
filter, preserves stereo information, shapes releases, and crossfades sustained
bowing. The existing compositions, phrase lengths, harmony, and scene assignments
are retained. VSCO uses different octave naming conventions for harp/piano and
strings/woodwinds; the mapping is explicit in the sampler and was checked against
recorded pitches.

The final mixes use 48 kHz processing and 24-bit WAV masters. Brief, linked stereo
gain reduction controls recorded attacks, capped at 6 dB before the final peak
ceiling, to preserve dynamics without making an entire cue too quiet. A dense, damped
stereo room response replaces the sparse reflection taps in the music. Its
impulse is synthesized locally; no external reverb recording is required.
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
python3 scripts/make_audio.py
python3 scripts/audio_check.py
```

The fetch step downloads only the manifest's pinned CC0 files, checks their
SHA-256 hashes, and extracts known audio members. Originals live in
`.cache/audio-sources/`; masters live in `.cache/audio-masters/`. Neither goes
into the game package. To render selected assets:

```sh
python3 scripts/make_audio.py first_light rain
python3 scripts/make_audio.py --encode-existing first_light
```

The encoder remains SoundFile 0.13.1 / libsndfile 1.2.2, with Vorbis
`compression_level=0.15`. Writes use 8,192-frame blocks because a single large
48 kHz write crashed this libsndfile build. Encoding uses a temporary file and
replaces the runtime file only after a successful close. Ogg serial numbers and
page checksums are made deterministic without altering compressed audio packets.

## Validation and listening

`audio_check.py` decodes all nineteen delivered assets and checks sample rate,
codec/PCM subtype, stereo content, duration, DC, sample and reconstructed peaks,
loop seams, and frame/level agreement with cached masters. It also checks the
first flute against its preserved hash. Reports are in `test-results/`.

The renderer and checks do not provide a human listening verdict. Audition the
music, rain, water, and scene balance in the rebuilt game. Git preserves earlier
audio versions; do not retain separate historical copies or comparison exports.
Runtime audio totals about 24 MiB; raw sample libraries are excluded from
exported games.
