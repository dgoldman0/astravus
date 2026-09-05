# Production ending stability

The last three closing-theme compositions now hold their geometry at zoom 1.0.
Earlier gentle movement, shot timing, the 1.2-second eased dissolves, credits and
title treatment remain unchanged. The shared cue file applies these holds to
both native playback and the standalone renderer.

The bounded investigation archived in Git stash
`c251e6da134771b833f84a6d9efa2104e878c08a` established two distinct causes of
unwanted texture movement: camera resampling and CRF18 delivery encoding. A
dissolve followed by identical input frames still produced visible texture
refresh with the old encoding settings. Clean timestamps and a small whole-frame
average were insufficient grounds for approval.

`render_closing_theme.py` now shares one delivery profile with the diagnostic:
H.264 constant QP14, stillimage tuning, no B-frames, no adaptive quantization,
no MB-tree/lookahead, equal I/P quantization ratios, and no periodic or scene-cut
keyframe refresh within the film. Lossless intermediate clips remain. The
encoder changes affect the MP4; native Ren’Py still playback does not use H.264.
The supplied WAV and runtime Ogg were verified unchanged during this check.

## Bounded verification

Run from `visual-novel/`:

```sh
python3 scripts/check_theme_stability.py
```

This writes one current six-second, silent 1080p60 diagnostic under
`build/graphics-polish/theme-stability/`, using the final two selected paintings,
an eased initial dissolve, then repeated identical RGB input frames. It imports
the production renderer's exact delivery settings, including the whole-film GOP
limit. The test does not render the full film or modify its current MP4.

The 2026-09-05 run fully decoded all 360 frames with no errors. Adjacent decoded
frames 90–359, after the intentional dissolve, yielded:

| Native 640×360 crop | Maximum mean RGB change (0–255) | 99th-percentile change | Largest channel change | Maximum changed pixels |
|---|---:|---:|---:|---:|
| Face/hair | 0.000307 | 0 | 2 | 0.0278% |
| Foliage | 0.000596 | 0 | 3 | 0.0504% |

The exact source, script, cue and output hashes, command, per-frame measurements
and full decode result are in
`build/graphics-polish/theme-stability/diagnostic.json`. Tiny lossy-codec rounding
differences remain; this is not mathematically lossless delivery.

The diagnostic isolates the encoder using pre-fitted RGB stills. It does not
exercise the complete film compositor, title fade, every painting, native player
or audio. It remains supporting evidence rather than a substitute for checking
the delivered film.

## Completed production delivery

The final approved art was rendered to `build/closing-theme.mp4` on 2026-09-05.
The actual delivery is 1920×1080 at 60 fps, **305,187,483 bytes (291.0 MiB)**,
SHA256 `0c6481a93fcb5eccf967b9c9718e69fd1e024c31f3b02c3a45e783a97f58a509`.
The renderer completed its full video/audio decode check before atomic replacement.
The separate [delivered-film review](graphics-film-review.md) verifies the final
three dissolves and every adjacent native face/foliage crop in their held periods,
excluding title/dissolve/fade frames. All 10,666 stored presentation timestamps are
unique and uniformly spaced at 1/60 second; the AAC track ends at 177.76 seconds.

The worst native detail pairs retain stable contours. Small codec differences
remain, strongest just after a dissolve; after half a second of each held shot,
the largest mean crop change is 0.001886/255 and the largest channel change is 4/255.
These are measured bounds for the inspected crops, not a claim of lossless pixels
or universal subjective smoothness. No real-time viewing or auditory listening
approval is claimed. The whole-film GOP may make arbitrary seeking more expensive;
the increased file size is now measured, but player seek performance is not.

The original WAV and runtime Ogg remain unchanged; their hashes and the final
cue/renderer/artifact evidence are recorded in the delivered-film review and its
receipt. The MP4 remains separate from runtime still/Ogg assets.
