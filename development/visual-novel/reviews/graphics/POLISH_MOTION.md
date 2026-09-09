# Closing-theme motion review — 0.1-alpha

The previous version had floating-point camera placement, but that alone did not cover frame scheduling, audio-buffer timing, image blending, or compression. This pass keeps all 15 pictures, their musical cue starts, and the complete 177.76-second song.

## Changes

- **Continuous in-game timing.** The old player replaced its visual position with every audio-position report. A backend reporting buffered updates therefore made animation wait and then jump. The player now advances on the display clock and corrects only sustained audio drift above 100 ms, at no more than a 5% speed adjustment. It freezes while paused and continues if a backend reports no audio position.
- **Display refresh.** Native rendering requests the next display frame, instead of using a 50 fps timer that does not divide evenly into a common 60 Hz refresh. Paused and reduced-motion playback use a low-frequency redraw. The MP4 is 60 fps.
- **Composed overlaps.** Both pictures hold their camera positions during each 1.2-second dissolve. The mix follows a smoothstep curve with gentle starts and stops. Movement begins after the incoming picture is clear and settles before the next blend begins. Cue times are rounded to the nearest output frame only for the MP4 (at most 8.34 ms).
- **One lossy video encode.** Review of the old movie found pronounced frame-difference spikes at some intermediate clip keyframes, including 10.00 seconds. Double compression of detailed painted textures was a plausible contributor. Temporary clips are now lossless 4:4:4 H.264; only the final delivery encode uses lossy 4:2:0 H.264 at CRF 18. Temporary clips are automatically removed.
- **Song playback level.** The game applies −6 dB to the song through Ren'Py's supported `Play(relative_volume=...)` argument. The WAV and stored Ogg remain untouched. The standalone MP4 retains the supplied master level because it is played independently of the quieter game music.

## Focused verification

`python3 scripts/project.py test --headless --suite closing_theme_review` passed **19/19 assertions** under Ren'Py 8.5.3.26051504 with game version `0.1-alpha`. These cover ordinary and reduced motion, pause/resume, silent-backend fallback, replay after skipping while paused, natural completion, returning to the end card, and cleanup of the theme channel. A new regression feeds the real clock an 80 ms buffered audio position, missing values, a paused interval, and a stale resumed value; visual steps stay positive and within the allowed rate correction.

A 14-second, 640×360 preview decoded all **840 frames at 60 fps**. Fitting the rendered transition frames to the two held endpoint pictures found a maximum smoothstep blend error of **1.41 percentage points** and no backward mix change larger than **0.000001** (compression noise). This covers an actual crossfade, which the earlier single-marker movement test did not.

Local evidence:

- `test-results/theme-song/polish-native.log`
- `test-results/screenshots/theme-blended-transition.png`
- `test-results/theme-song/polish-transition-review.png`
- `test-results/theme-song/polish-motion-measurements.json`

The focused tests establish timing behavior and image-blend continuity; they do not certify every display's performance or word-level synchronization with the vocals. The final full-resolution export is verified separately after the identity-corrected art is selected.

## Final full-resolution export

The final 1080p at 60 fps export is complete. [FINAL_FILM_REVIEW.md](FINAL_FILM_REVIEW.md) records all 10,666 decoded frames, all 14 overlap inspections, the investigated compression outliers, the unchanged input hashes, and the source/AAC signal comparison. The review uses native-timestamp frame analysis and explicitly does not claim subjective real-time viewing or auditory listening.
