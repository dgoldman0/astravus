# Alpha polish — 0.2.6

The title, credits and packages identify this as an alpha. The story and art from 0.2.5 are retained.

## Reading-time estimate

Ren'Py lint counts **7,934 words in 667 dialogue blocks**. At an assumed 200–250 words per minute, uninterrupted reading takes **31.7–39.7 minutes**. Allowing roughly 8–10 minutes for advancing text, scene transitions, looking at the artwork and the brief afterword gives the displayed estimate of **about 40–50 minutes**. Faster readers can finish sooner; exploring People, lingering over music or rereading will take longer. This is a planning estimate, not a timed human playthrough. Automated test duration is not used as a reading-time measurement.

## Chapter warnings

All 32 destinations remain available. Before entering a chapter the reader has not reached, the game checks whether any earlier chapter has unread dialogue. If so, **Spoilers ahead** offers **Go back** and **Jump anyway**. Escape also cancels. The popup does not describe the later plot. **Settings → Chapter spoiler warnings** turns the warning on or off and saves the preference immediately.

The check uses `renpy.seen_translation()` for the compiled dialogue identifiers, including the three connecting lines after Kaleb's walk. The pinned SDK's translation catalog supplies these identifiers; the native test verifies coverage of every story dialogue block. This reuses existing reading history across saves, rollback, restarts and compatible upgrades. Updated or added lines can correctly count as unread.

`visited_scenes`, encounter flags and the completed-book flag are deliberately not evidence of reading: chapter selection reconstructs those values. A confirmed jump neither marks its skipped dialogue as viewed nor removes warnings for other unread gaps. Returning to a reached chapter is allowed, as is beginning the next chapter once all earlier dialogue has been viewed. As with Ren'Py's ordinary skip feature, “viewed” means the engine processed the dialogue, not a claim to measure attention or comprehension.

## Credits and afterword

Credits show [dgoldman0](https://github.com/dgoldman0/Astravus) as a link to the Astravus repository, plus a separate visible button to [the itch page](https://arcadiumgames.itch.io/astravus-calista). Existing art, engine, font and audio attribution remains.

A separate **Beyond Book I** afterword follows the final story line. The garden background and home theme accompany a short look ahead to Calista's friendships, discoveries and adventures, followed by an invitation to support future adaptations through interest and feedback. It provides the same itch link and a **Finish Book I** button. The completed-book autosave follows the afterword, so Continue returns to the ending controls.

Checks and package verification are recorded in [VALIDATION.md](VALIDATION.md).
