# Audio sources and delivery

All music and effects are original procedural synthesis created for Astravus's Book I preview with `scripts/make_audio.py`. There are no downloaded recordings, commercial samples, sampled voices, Suno tracks, or borrowed melodies.

The runtime contains eight music cues and five environmental loops as **24 kHz stereo Ogg Vorbis**, plus five short **24 kHz, 16-bit stereo WAV** effects. First Light's original motif is retained; distinct arrangements support family life, discovery, wonder, celebration, refuge, grief, and remembrance. Separate tentative and practiced flute phrases support the music lessons. There is no voice acting.

The reproducible renderer uses NumPy, SciPy, and SoundFile. Gameplay requires none of those Python packages. Long WAV masters, the encoder, and the original draft First Light are retained only in the ignored `.cache/` directory; selected runtime files and the renderer belong in version control. The compressed runtime set is approximately 11 MiB.

Rendering used SoundFile 0.13.1, libsndfile 1.2.2, and Vorbis `compression_level=0.15` (quality 0.85). Ogg serial numbers and page checksums are normalized for reproducible files without altering the compressed audio packets.

See `docs/AUDIO_DIRECTION.md` in the source repository for the full cue sheet, dependencies, regeneration commands, and measurements. `scripts/audio_check.py` checks decoded Ogg/WAV content, clipping, DC, stereo, duration, loop boundaries, and master comparisons. These are numerical checks; in-game listening remains necessary to assess musical quality and scene balance. No subjective listening review is claimed by this provenance notice.
