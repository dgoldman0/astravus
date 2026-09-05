# Audio sources and delivery

Astravus's underscore melodies and arrangements are original to this adaptation.
The 0.1-alpha score contains **15 core compositions and nine variations**: 24
instrumental cues with approximately 38 minutes of musical material. Authored
melodies, contrasting passages, and arrangements follow the story's scenes and
subscenes. The score is rendered with recorded harp, soft upright piano, cello/viola ensembles, and
flute from **VSCO 2 Community Edition**, published under **CC0 1.0** by Versilian
Studios and its contributors: https://versilian-studios.com/vsco-community/

The environmental sound uses these **CC0** recordings, edited and mixed locally:

| Source | Author / editor | Use |
| --- | --- | --- |
| [Rain (loopable)](https://opengameart.org/content/rain-loopable) | Ylmir | Treehouse rain |
| [Dripping water loop](https://opengameart.org/content/dripping-water-loop) | Independent.nu; submitted by qubodup | Garden water and quiet indoor fountain |
| [Tree Creaking](https://opengameart.org/content/tree-creaking) | Department64; edited by AntumDeluge | Tree of Echoes, wooden contacts, subdued workshop/gathering textures |
| [6 Short water splashes](https://opengameart.org/content/6-short-water-splashes) | ezwa; submitted by qubodup | Pond splash |

CC0 public-domain dedication: https://creativecommons.org/publicdomain/zero/1.0/
These source credits are retained voluntarily. This notice does not relicense
the author's story or the original musical compositions.

Music and ambience are 48 kHz stereo Ogg Vorbis. Short effects are 16-bit stereo
WAV: 48 kHz except the two tentative flute cues at 24 kHz. **flute_attempt.wav**
is one short breath that briefly catches a note, then breaks. The original
**flute_first.wav** remains byte-for-byte intact and plays later in that lesson,
when Cali tries several notes. The later practiced phrase uses sampled flute
while retaining its original notes and timing. The festival's quiet rhythmic pulse and underlying room air remain
original synthesis. The story dialogue is not voiced.

The vocal closing theme, **Curiosity and Discovery**, is by **Daniel Goldman**,
with assistance from **ChatGPT and SUNO**. [Listen on SUNO](https://suno.com/s/IoZ3kzpqJBFXAgJJ).
It was supplied by the author as a 48 kHz stereo WAV. `curiosity_and_discovery.ogg` is an encoding of that song,
with no gain, EQ, compression, cuts or additional fades. It is a separate source
from the CC0 instrument and environmental libraries above. Its source hash and
encoding details are recorded in `docs/closing-theme-audio.json`; the standalone
video and game montage share `game/closing_theme.json` for their timing.
Within the game, the song plays at −6 dB relative to the music mixer to sit
comfortably beside the quieter score. The hesitant multi-note flute plays at
−2.5 dB relative to the sound mixer to match the later practice cue. These are
playback gains; the supplied song and original flute files are unchanged.

The game requires no sample player or additional software. Source recordings
and 24-bit music masters remain in the developer's cache. The score catalog and
scene cue sheet are in `docs/score-catalog.json` and `docs/score-cue-sheet.md`.
Most core cues use developed 32-bar forms, the festival has 48 bars, and the
variations have 24 bars. Music changes when the reader reaches a documented story
beat, using sequential fades; it can loop while the reader lingers.

The repository's `docs/audio-sources.json` pins all downloaded source files by
SHA-256, including the VSCO commit and license. `scripts/compose_score.py`
reproduces the instrumental score offline from editable notation in
`scripts/score_material.py`, `scripts/score_new_material.py`, and
`scripts/score_catalog.py`. `scripts/make_audio.py` delegates score rendering to
it and retains the existing environment/effect renderer; `scripts/sample_audio.py`
supplies the recorded instruments. `scripts/audio_check.py` checks all 36 audio
files: the 24 score cues, five ambience loops, six effects, and the closing song.

Each score cue is metered to its intended loudness group: ordinary music targets
−22.5 to −21.5 LUFS, reflective music −24 LUFS, and grief −26 LUFS, before the
reader's music setting. The audit measures actual encoded loudness and peaks,
loop continuity, and playback gains. Numerical and runtime checks do not replace
listening in context.
