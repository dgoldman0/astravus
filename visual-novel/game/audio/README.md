# Audio sources and delivery

Astravus's melodies and arrangements are original to this adaptation. The music
is rendered with recorded harp, soft upright piano, cello/viola ensembles, and
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
original synthesis. No voice acting or generated speech is included.

The game requires no sample player or additional software. Source recordings
and 24-bit music masters remain in the developer's cache.
The repository's `docs/audio-sources.json` pins all downloaded source files by
SHA-256, including the VSCO commit and license. `scripts/make_audio.py` and
`scripts/sample_audio.py` reproduce the mix; `scripts/audio_check.py` checks the
decoded delivery files. Numerical checks do not replace listening in context.
