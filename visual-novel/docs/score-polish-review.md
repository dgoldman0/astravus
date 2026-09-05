# Score expansion — 0.1-alpha

The score now contains 15 core compositions and nine variations, approximately
38.09 minutes across 24 loops. The work is complete at this scope: distinct
music for observing, making, stories, friendship, exploration, comfort,
painting and remembrance, with reader-reached subscene changes throughout the
32 chapters. The version remains **0.1-alpha**.

The existing motifs return in longer arrangements. The new material uses
different melodic rhythms, rests, harmony, meter, instrumental exchanges and
accompaniment patterns. The [cue sheet](score-cue-sheet.md) ties those choices to
specific dialogue beats; the [catalog](score-catalog.json) records their forms
and level targets. Editable notation and MIDI reproduction remain outside the
runtime package.

The complete decoded audit covers 36 audio files and 30 balance checks. Ordinary
music measures −22.6 to −21.5 LUFS, reflective arrangements −24.0 to −23.9, and
grief arrangements −26.0 to −25.9. Every new score is within 0.2 LU of its target.
The home-to-closing-song difference is 0.8 LU. No clipping, DC, loop-boundary,
duration, inventory or master/encoding errors were found. Delivered audio totals
76.45 MiB, including the unchanged song, ambience and effects.

All story dialogue and the 12 non-score audio files remain byte-identical to
commit `001922b`. The deliberately poor flute performances remain story events
with their original timing and levels. Chapter 24 ends warmly; chapter 25 is
unscored. The memorial address also has silence before the remembrance music.

The 61 Python regression checks and clean Ren'Py lint pass. The native
`score_review` suite passes all 58 assertions and records 49 checkpoints across
all 32 chapter entries and the protected music changes, including waiting on a
line, rollback, save/load, flute cues, waterwheel success, the loss, memorial,
afterword and title cleanup. Its current results are recorded in
`test-results/score-runtime.json` and the release matrix's `score-runtime` row.

These are composition, integration and technical verification results. They do
not claim a human listening approval. The matrix keeps that editorial sign-off
separate. The existing review-build route allows the author to use the rebuilt
alpha without presenting the broader release matrix as fully approved.

Desktop and browser exports replace the same `0.1-alpha` filenames. The closing
movie needs no re-render for this underscore-only change. Archive verification
and a source-commit receipt in `build/score-polish/artifact-receipt.json` identify
the current packages; raw samples, WAV masters, MIDI files and test code are
excluded from them.
