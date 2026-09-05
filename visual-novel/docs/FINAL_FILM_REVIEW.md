# Current closing film

The current [standalone MP4](../build/closing-theme.mp4) is **1920×1080 at 60 fps, 305,187,483 bytes (291.0 MiB)**. Its SHA256 is `0c6481a93fcb5eccf967b9c9718e69fd1e024c31f3b02c3a45e783a97f58a509`. This replaces the earlier 126.5 MiB delivery; its old review details remain in Git.

See [graphics-film-review.md](graphics-film-review.md) for the current artifact/input evidence, reproducible checker and bounded visual findings. The full renderer video/audio decode succeeded before replacement. The subsequent independent audit found 10,666 uniformly timed video frames, exactly 1/60 second apart, ending at 177.766667 seconds. AAC LC 48 kHz stereo ends at the supplied song's 177.76 seconds.

The final three images now hold their camera geometry. Their 1.2-second dissolves progressed continuously in the inspected full/native frame strips, and held face/foliage contours remained stable in the worst adjacent detail pairs. Fine lossy pixel variation persists, especially immediately after a dissolve; the movie is not mathematically lossless. Current delivery uses the production QP14 stillimage profile described in [GRAPHICS_MOTION.md](GRAPHICS_MOTION.md).

Original WAV SHA256: `491ffdb74b0f6b2c02873eae485b6bfdb2506538236c007c7eec23bef2d314a4`. Runtime Ogg SHA256: `460ad7c6fdc1c2a6b058b3e8d610bc7f9cc355655b96e9081fe6d1c27f8baa05`. Both remain unchanged. The game uses the still/Ogg presentation; the MP4 is a separate artifact.

This is timestamp and decoded-frame analysis, not subjective real-time viewing or auditory listening. Arbitrary player seeking, every display's perceived smoothness, speaker quality and word-level lyric synchronization have not been verified by this check. The long-GOP delivery may make arbitrary seeking more expensive; file size is measured, seek performance is not.
