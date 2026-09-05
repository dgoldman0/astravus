# Closing theme preview — first timing pass

The user supplied `Curiosity and Discovery.wav` at the workspace root and the lyrics in conversation. The expanded afterword now offers **Play closing theme**, alongside finishing immediately. The film leads to the end-of-book controls, which also offer replay. This remains an editable development preview; release packaging is on hold.

The credits list **Curiosity and Discovery — by Daniel Goldman, with assistance from ChatGPT and SUNO**, with a [Listen on SUNO](https://suno.com/s/IoZ3kzpqJBFXAgJJ) link supplied by the author.

`build/closing-theme.mp4` is the standalone 1080p/25 fps preview. The game reuses the images with a 3.81 MiB Ogg version of the song, rather than including the entire MP4. Both use the shot order, timing and shallow camera moves in `game/closing_theme.json`. The complete supplied song is retained. Its 48 kHz stereo encode has the same frame count and only a −0.030 dB average-level change; no gain, EQ, compression or cuts were applied. Source and output hashes are in [closing-theme-audio.json](closing-theme-audio.json).

## Measured audio

- Duration: **177.76 seconds (2:57.76)**.
- Format: stereo, 48 kHz, 16-bit PCM; 32.56 MiB.
- Sample peak: approximately −4.0 dBFS; whole-track RMS approximately −17.8 dBFS.
- Signal analysis finds potential changes near 0:10, 0:23, 0:44, 0:55, 1:05, 1:15, 1:30, 1:44, 1:55, 2:07, 2:16, 2:34 and 2:44. Clear energy dips occur near 2:05 and 2:38.
- These are waveform/spectral cues, **not verified vocal or lyric timestamps**. Rhythm analysis produced competing tempo interpretations, so a rigid BPM edit would be premature.

Local analysis artifacts are `test-results/theme-song/analysis.json` and `timing.png`. The supplied WAV remains untouched at its original path.

## Visual arc

| Lyric passage | Images and intent |
| --- | --- |
| Youth and the garden's call | Begin with the quiet garden, then its smaller details. Let the first image emerge gently. |
| Gentle hands; venturing forth | Planting together with Maia, followed by the path leading away from home. |
| Insects and small wonders | A dedicated flower still with a bee and ladybug, followed by water details. |
| Treehouse and friends | The treehouse, shared sketchbook/storytelling, and warm memories of the children together. Joren belongs naturally in these memories. |
| Adventures and taking flight | The children's project, branches overhead, a widening view of Lumen. Treat flight as imagination, without inventing a literal flight event. |
| Night, dawn and continued curiosity | Move from a sheltered evening view toward an open, brighter garden/path. Hold the final image longer and finish on the title. |

The preview uses **15 shots** with **1.2-second cross-dissolves**, alternating wide settings, people and small details. Some shots hold still; others have a slow, shallow camera move. The final timing should be reviewed against the vocal phrasing. The song's purpose is to leave the reader with the breadth and warmth of her childhood.

The in-game film has Pause/Resume, Space to pause, Skip, and Escape to return to the ending. Reduced motion removes camera moves and dissolves. If an audio backend provides no position (for example when muted), a fallback clock keeps the visuals progressing. Skipping while paused does not leave replay paused. Continue after finishing returns to the end card.

Two additional illustrations use the built-in image_gen tool and approved references: `game/images/backgrounds/book-one/garden-wonders.png` and `game/images/cg/book-one/treehouse-friends.png`. Their exact prompts, source references and selected output hashes are recorded in [environment-assets.json](environment-assets.json) and [assets.json](assets.json). The friendship scene depicts an earlier happy memory, without new story events. The original character-free backgrounds and separate sprites remain available.

## Reproduce and adjust

Edit the shot entries in `game/closing_theme.json`, then run:

```sh
python3 -m pip install --target .cache/video-tools imageio-ffmpeg==0.6.0
python3 scripts/render_closing_theme.py
```

Use `--source /path/to/song.wav` when the author's original WAV is elsewhere; `--width 1280` gives a smaller review render. The default source is the workspace-root upload. The renderer removes its temporary shot clips and replaces the current MP4 only after decoding the entire result and checking the expected frame count. The original WAV remains untouched. The title overlay is programmatic typography; scene artwork is copied from selected generated pixels without retouching.

The native sequence uses Ren'Py's [creator-defined displayable API](https://www.renpy.org/doc/html/cdd.html), with audio-position timing and a pause-aware fallback. A standalone MP4 is for ordinary video players; the game itself does not depend on platform-specific movie decoding.

## Current afterword copy

**There is more to her story.**

Calista will carry these memories with her. Ahead lie new friendships, unfamiliar places, and adventures beyond anything she imagined in the treehouse. There will be laughter, love, and wonder, too.

Seeds of Youth is the first book of a larger story. We hope to bring the rest of Calista's journey to life as visual novels. Follow Astravus on itch.io and share your thoughts—your interest can help bring the next book to life.

This copy and the sequence remain open for the author's edits. Later friendships, art, love and travel are supported by the source; the card avoids revealing specific later events.
