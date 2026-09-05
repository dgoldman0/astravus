# Current closing film

The current [standalone MP4](../build/closing-theme.mp4) is **1920×1080 at 60 fps, 305,028,419 bytes (290.9 MiB)**. Its SHA256 is `87f20bf84d226d4a523f60ff42f5132b19ac9830351e10f1ca6605965ea7dd34`. This delivery includes the corrected low-bank planting CG.

See [graphics-film-review.md](graphics-film-review.md) for the current artifact/input evidence, reproducible checker and bounded visual findings. The full renderer video/audio decode succeeded before replacement. The subsequent independent audit found 10,666 uniformly timed video frames, exactly 1/60 second apart, ending at 177.766667 seconds. AAC LC 48 kHz stereo ends at the supplied song's 177.76 seconds; its complete encoded packet hash matches the preceding delivery. The actual planting shot was inspected at its incoming start, midpoint and settled frame, where the revised low coping and dry working bank are visible.

The planting image is the only changed render input. The final three images still hold their camera geometry. The preceding delivery's detailed ending review found continuously progressing 1.2-second dissolves and stable held face/foliage contours, with fine lossy pixel variation especially immediately after a dissolve. Those are prior measurements with unchanged ending images/cues/renderer, not measurements repeated on this replacement. Current delivery uses the production QP14 stillimage profile described in [GRAPHICS_MOTION.md](GRAPHICS_MOTION.md).

Original WAV SHA256: `491ffdb74b0f6b2c02873eae485b6bfdb2506538236c007c7eec23bef2d314a4`. Runtime Ogg SHA256: `460ad7c6fdc1c2a6b058b3e8d610bc7f9cc355655b96e9081fe6d1c27f8baa05`. Both remain unchanged. The game uses the still/Ogg presentation; the MP4 is a separate artifact.

This is timestamp and decoded-frame analysis, not subjective real-time viewing or auditory listening. Arbitrary player seeking, every display's perceived smoothness, speaker quality and word-level lyric synchronization have not been verified by this check. The long-GOP delivery may make arbitrary seeking more expensive; file size is measured, seek performance is not.
