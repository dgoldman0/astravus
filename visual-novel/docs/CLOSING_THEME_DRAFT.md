# Closing theme — revised sequence

The user supplied `Curiosity and Discovery.wav` at the workspace root and the lyrics in conversation. The expanded afterword now offers **Play closing theme**, alongside finishing immediately. The film leads to the end-of-book controls, which also offer replay. This remains an editable development preview; release packaging is on hold.

The credits list **Curiosity and Discovery — by Daniel Goldman, with assistance from ChatGPT and SUNO**, with a [Listen on SUNO](https://suno.com/s/IoZ3kzpqJBFXAgJJ) link supplied by the author.

`build/closing-theme.mp4` is the standalone 1080p/50 fps preview. The game reuses the images with a 3.81 MiB Ogg version of the song, rather than including the entire MP4. Both use the shot order, timing and shallow camera moves in `game/closing_theme.json`. The complete supplied song is retained. Its 48 kHz stereo encode has the same frame count and only a −0.030 dB average-level change; no gain, EQ, compression or cuts were applied. Source and output hashes are in [closing-theme-audio.json](closing-theme-audio.json).

## Measured audio

- Duration: **177.76 seconds (2:57.76)**.
- Format: stereo, 48 kHz, 16-bit PCM; 32.56 MiB.
- Sample peak: approximately −4.0 dBFS; whole-track RMS approximately −17.8 dBFS.
- Signal analysis finds potential changes near 0:10, 0:23, 0:44, 0:55, 1:05, 1:15, 1:30, 1:44, 1:55, 2:07, 2:16, 2:34 and 2:44. Clear energy dips occur near 2:05 and 2:38.
- These are waveform/spectral cues, **not verified vocal or lyric timestamps**. Rhythm analysis produced competing tempo interpretations, so a rigid BPM edit would be premature.

Local analysis artifacts are `test-results/theme-song/analysis.json` and `timing.png`. The supplied WAV remains untouched at its original path.

## Revised visual sequence

The film opens on **Cali and Kael exploring the sunflowers**. **Fourteen of fifteen shots feature characters**, and **every image is used once**. A single flower/insect insert follows their opening glance; the remaining pictures follow family guidance, small discoveries, Nibble, shared stories, projects, laughter, evening sketching and another morning. The memories include Joren as a child, without suggesting he returns after his death.

| Start | Selected picture | Camera |
| --- | --- | --- |
| 0:00.00 | [Cali and Kael in the sunflowers](../game/images/cg/book-one/theme-garden-opening.png) | Gentle push in |
| 0:10.40 | [A closer look at the garden](../game/images/backgrounds/book-one/garden-wonders.png) | Hold |
| 0:22.52 | [Gentle guidance](../game/images/cg/book-one/garden-compromise.png) | Hold |
| 0:33.00 | [Learning with Selene](../game/images/cg/book-one/flute-rest.png) | Gentle pan |
| 0:43.76 | [Following a new path together](../game/images/cg/book-one/theme-path-friends.png) | Gentle push in |
| 0:54.80 | [A tiny shared discovery](../game/images/cg/book-one/theme-insect-discovery.png) | Hold |
| 1:05.36 | [Nibble investigates](../game/images/cg/book-one/theme-nibble-moment.png) | Gentle pan |
| 1:15.44 | [Come inside](../game/images/cg/book-one/theme-treehouse-arrival.png) | Gentle pull back |
| 1:29.88 | [Stories shared](../game/images/cg/book-one/cassia-storytelling.png) | Hold |
| 1:44.32 | [Friends by my side](../game/images/cg/book-one/treehouse-friends.png) | Gentle push in |
| 1:54.64 | [We made it work](../game/images/cg/book-one/theme-waterwheel-team.png) | Gentle pull back |
| 2:07.16 | [The world grows wider](../game/images/cg/book-one/theme-dome-friends.png) | Gentle pan |
| 2:16.24 | [A sketch and a laugh](../game/images/cg/book-one/theme-sketch-laughter.png) | Hold |
| 2:33.76 | [One more page before night](../game/images/cg/book-one/theme-evening-reading.png) | Gentle push in |
| 2:44.08 | [Another day to discover](../game/images/cg/book-one/theme-morning-outlook.png) | Gentle pull back |

The **0.8-second dissolves** are shorter than the first cut's transitions. Camera movement uses gentle starts and stops, fractional positioning and **50 fps**, with several fully held pictures. The standalone renderer uses cubic sampling through FFmpeg's [perspective filter](https://ffmpeg.org/ffmpeg-filters.html#perspective), avoiding the previous rounded moving crop. Native playback also uses fractional placement and derives its offsets from the actual scale, instead of rounded render bounds. Reduced motion keeps every frame still.

A 150-frame synthetic-marker check measured the exported camera's smooth path: maximum position error **0.090 pixels**, no backward steps above the check's 0.02-pixel tolerance, and maximum frame-to-frame acceleration **0.011 pixels**. This checks the movement mechanism; it does not certify artistic pacing. Musical boundaries remain an editable timing pass, not verified word-level lyric alignment.

The in-game film has Pause/Resume, Space to pause, Skip, and Escape to return to the ending. Reduced motion removes camera moves and dissolves. If an audio backend provides no position (for example when muted), a fallback clock keeps the visuals progressing. Skipping while paused does not leave replay paused. Continue after finishing returns to the end card.

Ten new character illustrations are saved under `game/images/cg/book-one/theme-*.png`, with the individual paths linked in the table above. They use the **built-in image_gen tool**, with the established cast, clothes and settings as references. Their complete prompts, input references and selected hashes are the `theme-recut-*` records in [assets.json](assets.json). The earlier garden detail and friends' treehouse image retain their original records in [environment-assets.json](environment-assets.json) and [assets.json](assets.json). The original character-free backgrounds and separate sprites remain available for story scenes.

## Reproduce and adjust

Edit the shot entries in `game/closing_theme.json`, then run:

```sh
python3 -m pip install --target .cache/video-tools imageio-ffmpeg==0.6.0
python3 scripts/render_closing_theme.py
```

Use `--source /path/to/song.wav` when the author's original WAV is elsewhere; `--width 1280` gives a smaller review render. The default source is the workspace-root upload. The renderer removes its temporary shot clips and replaces the current MP4 only after decoding the entire result and checking the expected frame count. The original WAV and existing runtime audio encode remain untouched when their recorded hashes match. The title overlay is programmatic typography; scene artwork is copied from selected generated pixels without retouching.

The native sequence uses Ren'Py's [creator-defined displayable API](https://www.renpy.org/doc/html/cdd.html), with audio-position timing and a pause-aware fallback. A standalone MP4 is for ordinary video players; the game itself does not depend on platform-specific movie decoding.

## Current afterword copy

**There is more to her story.**

Calista will carry these memories with her. Ahead lie new friendships, unfamiliar places, and adventures beyond anything she imagined in the treehouse. There will be laughter, love, and wonder, too.

Seeds of Youth is the first book of a larger story. We hope to bring the rest of Calista's journey to life as visual novels. Follow Astravus on itch.io and share your thoughts—your interest can help bring the next book to life.

This copy and the sequence remain open for the author's edits. Later friendships, art, love and travel are supported by the source; the card avoids revealing specific later events.
