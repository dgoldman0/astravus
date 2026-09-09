# Audio sequence review — 0.1-alpha

Reviewed September 5, 2026 by `matrix_release` against the current three story scripts, closing-theme screen, cue sheet and measured runtime report. This is **script/cue and measurement review**, not a claim of subjective listening through speakers or headphones. Final native playback and browser behavior have separate matrix rows.

| Beat | Current placement and continuity |
| --- | --- |
| First flute, scene 5 | The score stops before Selene asks for one note. `flute_attempt.wav` starts with “The first sound trembled, thinned, and broke” and stops before Calista lowers the flute. “There was a note in there” follows this single broken sound. The gentle retry is narrated; the actual multi-note cue begins later, after the discussion of what comes next. |
| Hesitant phrase, scene 5 | `flute_first.wav` plays at amplitude 0.75 while they go a few notes at a time. It stops as the flute rests, before the color conversation. Selene's pale-blue association belongs to the source music scene; it is not a supernatural visual event. |
| Later practice, scene 8 | A distinct later-evening sentence establishes progress before `flute_practice.wav`. Lyra's accelerating clapping and their laughter lead to the stop and resting pose. The home cue resumes after the musical exchange. |
| Tree of Echoes, scene 9 | Score fades away for the creak. The children identify wood moving with the branches; no voices are played. The wonder cue returns after the listening exchange. |
| Rain refuge, scene 19 | Existing ambience fades before the separate rain bed starts; the rain-refuge score and bed use their measured independent mixer levels. Roof patter accompanies a clearly imagined talking-tree story. |
| Scene 24→25 | The argument's shared-life reflection continues under the rain-refuge cue. Both music and ambience fade at the entry to the news. Joren's death and the cultural shock/mortality reflection remain in silence; grief music enters the following family scene with a four-second fade. |
| Adjacent everyday scenes | Repeated music and ambience uses carry `if_changed` rather than restarting the same cue. Explicit lesson/listening/loss stops remain. Quieter grief/rain arrangements and subtle room/garden/workshop/plaza beds retain their distinct roles. |
| Closing theme | Entry fades the prior music and ambience over half a second; the song plays on its own music-mixer channel with the cue sheet's −6 dB runtime gain. Hide/skip stops that channel and clears pause; return restores the home cue. Standalone audio mastering is handled separately. |

The fresh `audio-measurements` matrix run checks all 20 delivered files and four related-cue balances, including the supplied-song comparison, decoding, sample rates, peak/DC/loop checks and actual script gains. The measured song/home difference remains 0.4 LU, and hesitant/practice differs by 0.3 LU. The first broken breath remains quieter. The relevant source and evidence hashes are in the `audio-sequence` and `audio-measurements` receipts; no comparison audio copies were added.
