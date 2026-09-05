# Final closing-film review — 0.1-alpha

The current [standalone MP4](../build/closing-theme.mp4) was rendered from the final selected artwork on 2026-09-05 and independently checked after atomic replacement. It is **1920×1080, 60 fps**, **132,626,923 bytes (126.5 MiB)**. The game continues to use the cue-sheet stills and Ogg audio; this MP4 is a separate preview, with no backup movie added to runtime assets.

## Artifact and frozen inputs

- MP4 SHA-256: `fbec95c4272c568691950814b0f402add8d7f5fd12a991489dfbadea57404675`.
- Actual video: H.264 High, progressive yuv420p; **10,666 decoded frames**. Stored presentation timestamps are all unique and exactly 1/60 second apart, from 0.000 to 177.750 seconds; video presentation ends at 177.766667 seconds.
- Actual audio: AAC LC, 48 kHz stereo, about 257 kb/s. The complete 177.76-second supplied song is present. MP4 container duration rounds to 2:57.77.
- Original WAV SHA-256: `491ffdb74b0f6b2c02873eae485b6bfdb2506538236c007c7eec23bef2d314a4`.
- Cue sheet SHA-256: `6b5adf7e937d99d5a54d3870f380ce1d4f19e36eab923d3ce5c793f36cea1619`.
- Renderer SHA-256: `26eb13576242481b6813af625f2f47b7855d0c2099933b90c5376bf15808f45d`.
- The WAV, cue sheet, renderer, runtime player, fonts, Ogg and all 15 source-image hashes were captured before rendering and compared again after verification. None changed. The complete input map is in `test-results/final-film-inputs.json`.

The renderer completed its own full video/audio decode before replacing the prior preview. An independent full-resolution decode then measured every one of the 10,666 frames. A separate full audio decode and packet-timestamp audit also exited successfully without errors. Temporary lossless shot clips were removed automatically; no unrelated files were deleted.

## Composition and transitions

The settled-shot contact sheet was inspected for all 15 shots, followed by the full-resolution title frame and opening/title/ending contact sheet. Fourteen shots contain characters; the sole garden insert provides a brief close look at the setting. The opening includes the established Calista and Kael. The sequence moves through family guidance, friends, pets, projects, laughter, evening reading and another morning. These are childhood memories offered after the afterword; Joren’s appearance does not depict new events after his death. The final foreground portrait and readable title preserve a hopeful finish.

Every 1.2-second overlap was evaluated at its actual 60 fps timestamps. All 73 frames, including both boundaries, were projected onto the two held full-resolution endpoint images. The measurements include fitted opacity, smoothstep error, successive opacity steps, and residual RGB error. Seven sequential rendered samples per overlap were inspected visually. Both source compositions remain fixed during the mix; shallow camera motion belongs to the settled portions.

Across all 14 overlaps, the largest fitted smoothstep error was **2.177 percentage points**. The largest backward fitted step was **0.0082 percentage points**, consistent with compression noise rather than reversed motion. The largest residual was 2.318 RGB levels out of 255. These measurements describe a lossy delivery encode, not mathematically identical uncompressed blends.

| Overlap start | Incoming image | Maximum mix error | Visual finding |
| --- | --- | --- | --- |
| 10.400 s | A closer look at the garden | 0.828 percentage points | The opening pair fades into the sole character-free garden insert; leaf and path positions stay fixed through the mix. |
| 22.517 s | Gentle guidance | 1.298 percentage points | The garden insert gives way to the seated family guidance scene without changing either endpoint crop. |
| 33.000 s | Learning with Selene | 1.258 percentage points | The pond-side family scene blends into flute practice; face and timber contours stay in place as opacity changes. |
| 43.767 s | Following a new path together | 1.986 percentage points | The indoor lesson gives way to the three friends on the path; the close/wide change reads clearly without a camera snap. |
| 54.800 s | A tiny shared discovery | 1.034 percentage points | The path group fades into the smaller shared insect discovery; eyes, hands and flowers keep their positions. |
| 65.367 s | Nibble investigates | 1.895 percentage points | The insect close-up blends into Calista with Nibble; both compositions hold until the new image is clear. |
| 75.433 s | Come inside | 1.836 percentage points | Nibble gives way to the welcoming treehouse trio; the door, broad room, trunk and framing stay stable. |
| 89.883 s | Stories shared | 1.869 percentage points | The warm treehouse group blends into the evening courtyard story circle; the light change belongs to the montage rather than continuous doorway action. |
| 104.317 s | Friends by my side | 1.873 percentage points | The story circle gives way to the seated friends around the treehouse table with a continuous opacity change. |
| 114.633 s | We made it work | 1.632 percentage points | The table scene blends into the kneeling waterwheel project; the stable endpoint crops preserve the activity and support planes. |
| 127.167 s | The world grows wider | 1.728 percentage points | The project gives way to the wider dome view; no pan begins while both images are mixed. |
| 136.233 s | A sketch and a laugh | 1.827 percentage points | The wide dome composition blends into shared sketch laughter with the faces held steady. |
| 153.767 s | One more page before night | 2.177 percentage points | Shared laughter fades into solitary evening reading. The largest fitted one-frame mix step coincides with a delivery keyframe; the five adjacent full/detail frames show continuous blending with no spatial jump or gross flash. |
| 164.083 s | Another day to discover | 1.300 percentage points | Evening reading blends into the hopeful foreground portrait and canonical treehouse at dawn; the later title appears only after the overlap has completed. |

## Investigated compression outliers

Full-frame consecutive RGB differences identified periodic peaks at final H.264 keyframes, including held compositions. These were investigated explicitly rather than counted as camera failures or ignored. Five adjacent frames at 750, 1500, 5000, 7250, 8250, 9250 and 10250 were inspected as full compositions and native-pixel detail crops.

The three inspected held-shot keyframes had estimated translation below 0.004 pixel per axis, with mean channel changes below 0.066/255. The larger moving-shot estimates remained below 0.061 pixel per axis, consistent with the shallow ongoing camera moves. The frame at 154.167 seconds also lies within an intended dissolve; its blend continues forward. The image sequences show small fine-detail compression refresh, with no discernible spatial jump or gross whole-frame flash. Ordinary lossy pixel variation remains; this review does not claim a lossless movie.

## Song integrity

The original has 8,532,480 stereo sample frames. AAC decoding returns 8,532,992, including 512 trailing codec-padding frames (10.67 ms); it does not omit the supplied song. Relative to the matching source samples, the measured average level change is **-0.0556 dB**, the encoded peak is **-4.113 dBFS**, and sample alignment correlation is **0.998307**. The export applies no gain, EQ, edits, extra fades or dynamic-range compression to the song. The separate −6 dB in-game playback setting is unchanged.

## Evidence and limits

- `test-results/final-film-render.log`: complete final render and internal decode.
- `test-results/final-film/verification.json`: artifact/input hashes, full-frame diagnostics, all 1,022 overlap observations and individual review findings.
- `test-results/final-film/timestamps.json` and `video-packet-timestamps.sha256`: actual stored presentation-time audit.
- `test-results/final-film/audio-master-check.json`: source/AAC signal comparison.
- `test-results/final-film/transition-01.png` through `transition-14.png`: all reviewed overlap strips.
- `test-results/final-film/settled-shot-contact.png`, `opening-title-ending-contact.png`, and `title-full-frame.png`: composition/endpoints.
- `test-results/final-film/keyframe-outliers.json` and `keyframe-*-adjacent.png`: additional investigated frames.
- `test-results/final-film/verification-tools/`: exact local verification scripts, whose hashes are recorded in the report.

**Method limit:** this was a native-timestamp decoded-frame and signal review, not subjective real-time viewing or auditory listening. It does not verify word-by-word lyric timing, performance on every display or speaker quality. Native pause/replay/reduced-motion behavior is covered separately by the game’s runtime tests. The game and export read the same final cue sheet and source images; reduced motion intentionally holds frames and uses cuts.
