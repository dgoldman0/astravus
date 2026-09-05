# Delivered closing film — graphics polish review

The current separate MP4 is **305,187,483 bytes (291.0 MiB), 1920×1080 at 60 fps**, rendered from the approved production cue sheet and images. SHA256: `0c6481a93fcb5eccf967b9c9718e69fd1e024c31f3b02c3a45e783a97f58a509`. This report supersedes the old 126.5 MiB artifact facts in FINAL_FILM_REVIEW.md; it does not reuse that older movie's motion approval.

The delivered ending shows continuous eased dissolves and stable spatial contours in the inspected native frames. Fine lossy pixel variation remains, particularly just after a dissolve. This is decoded-frame analysis, **not subjective real-time playback or auditory listening**; it cannot establish performance on every player/display or guarantee that no viewer will perceive any shimmer.

## Actual delivery and frozen inputs

- H.264 High, progressive yuv420p, square pixels; 10,666 frames. The stored presentation/decode timestamps are equal, unique and strictly monotonic at exactly 1/60-second intervals, from 0 to 177.750 seconds. Video presentation ends at 177.766667 seconds.
- AAC LC, 48 kHz stereo, approximately 257 kbps according to demux metadata. Its packet timeline ends at 177.76 seconds, matching all 8,532,480 sample frames of the supplied WAV. The first AAC packet has the normal −1,024-sample priming timestamp. This verifies the track timeline, not a fresh sample-by-sample mastering comparison.
- Runtime Ogg SHA256: `460ad7c6fdc1c2a6b058b3e8d610bc7f9cc355655b96e9081fe6d1c27f8baa05` (unchanged separate Vorbis asset; MP4 uses the original WAV).
- Original WAV SHA256: `491ffdb74b0f6b2c02873eae485b6bfdb2506538236c007c7eec23bef2d314a4`.
- Shared cue SHA256: `1ced60548d388801dd655f7de96b001e04b0fa6379cdb8447a5b3d4d5a70865e`.
- Production renderer SHA256: `07fd19e20da7e1386a8294622c5b16a8a121a561ded57b0e6b9968e25df8d6c8`.

The check imports the renderer's actual QP14 delivery profile: stillimage tuning, no B-frames, a whole-film GOP with scene-cut refresh disabled, no adaptive quantization/MB-tree/lookahead and equal I/P quantization ratios. The final three cue compositions are fixed at zoom 1.0 with no focus movement. Earlier camera moves were not re-reviewed by this bounded ending check.

The renderer's complete video/audio decode succeeded before atomic output replacement; its current log and exact movie/image/cue/renderer snapshot are `build/graphics-polish/film-render.log` and `film-render-inputs.json`. This independent check matched that output SHA and all recorded render inputs, audited timestamps for all 10,666 video packets, and decoded frames 8,173–10,031 for the ending measurements. The movie and review inputs were unchanged during verification. `ffprobe` is not installed in this environment; equivalent stream metadata came from the bundled FFmpeg demuxer, with exact packet timestamps and independent OpenCV video metadata/decode. No tool installation was needed.

## Final three dissolves

All 73 native-timestamp frames of each 1.2-second overlap were measured. Whole-composition opacity fitting uses 480×270 area-downsampled copies; the visual review also inspected seven delivered composition samples per transition and native-pixel beginning/mid/end face-detail crops. Downsampled fitting alone is not a native-detail quality test.

| Incoming shot / actual start | Maximum fitted opacity error | Minimum / maximum one-frame opacity step | Observation |
|---|---:|---:|---|
| Sketch laughter  / 136.233 s |1.460 percentage points |0.000007 /0.026634 | Wide dome view blends into the close group sketch. Faces/curls retain their positions during the deliberate composition change; no hard cut or endpoint crop snap observed. |
| Evening reading  / 153.767 s |1.209 percentage points |0.000011 /0.026495 | Group drawing blends continuously into the seated reading view. Face/wood details stay spatially fixed as their opacity changes. |
| Morning outlook  / 164.083 s |1.172 percentage points |0.000015 /0.023878 | Reading gives way to the bright garden and foreground Calista. The sunlight/light-level change belongs to the images; the transition itself remains a blended progression. |

All measured opacity steps are forward. Maximum fitted residual at the 480×270 measurement size is 1.197 RGB levels out of 255. The native midpoint samples show the expected overlapping compositions, without a geometric camera jump. These findings apply to the inspected final three overlaps, not an unseen new full-film visual review.

## Held native detail, including the largest residual changes

Dissolves, title appearance and fades were excluded. Measured windows: 137.450–153.750s for sketch laughter;154.983–164.067s for reading;165.300–167.183s for morning. The script measures every adjacent pair within each window using explicit native face/hair and foliage rectangles. I inspected all six worst-pair native strips, not just averages.

| Hold | Pairs per crop | Maximum face/hair mean RGB change | Maximum foliage mean RGB change | Maximum local channel change |
|---|---:|---:|---:|---:|
| Sketch laughter |978 |0.045472 /255 |0.053068 /255 |7 |
| Reading |545 |0.052225 /255 |0.064248 /255 |11 |
| Morning |113 |0.032839 /255 |0.025641 /255 |9 |

The strongest changes are in the first few held frames immediately after the dissolve, then decay. They are retained in the table rather than discarded as an inconvenient average. After the first half-second of each hold, maximum mean crop changes are 0.000227/0.001250 for sketch face/foliage, 0.000535/0.001782 for reading and0.000757/0.001885 for morning. At that settled stage, the largest local channel change is 4/255 and at most 0.158% of pixels change in any inspected crop pair.

The worst native pairs preserve visible eye/face contours, curls, leaf shapes, timber rails and branch positions. The remaining measured differences are fine pixel changes, without a visible contour displacement in these paired frames. This supports the fixed-composition approach while retaining the honest limit that the lossy MP4 is not bit-identical from frame to frame. Normal-speed subjective shimmer perception has not been tested here.

## Reproduction and evidence

From visual-novel:

```sh
python3 scripts/review_graphics_film.py
```

The script reads the delivered MP4, shared cue file, production encoder profile and current render snapshot. It does not render another film or change runtime assets. Outputs under ignored `test-results/graphics-film/` total about 9 MiB: the metadata text, exact timestamp/input/artifact receipt, per-frame crop measurements, three whole-composition overlap strips, three native overlap-detail strips and six native worst-pair strips. `verification.json` contains the explicit manual visual findings and hashes of all inspected strips; a fresh script run intentionally resets manual visual status to pending.

The standalone MP4 remains separate from the game's still/Ogg runtime. Its larger size is measured; the long-GOP tradeoff for arbitrary player seeking is not performance-tested by this review. No full-frame export sequence or alternate runtime movie was retained.
