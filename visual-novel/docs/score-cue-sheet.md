# Book I score cue sheet — 0.1-alpha

This sheet records the musical intent and reader-reached triggers for the expanded
instrumental score. The story remains authoritative: the score supports an event
after the reader reaches it. A loop may develop musically, but it must remain
within its current emotional purpose for as long as the reader stays there.

The runtime sources are [script.rpy](../game/script.rpy),
[family_book_one.rpy](../game/family_book_one.rpy), and
[friendships_book_one.rpy](../game/friendships_book_one.rpy). The composition source
and generated audio report provide the measured duration and musical construction
of each delivered cue. This document records intent, not a listening approval.

## Palette and recurring ideas

The 15 core cues and nine variations distinguish observing, making, imaginative
play, exploration, domestic comfort, and different ways of living with grief.
Recorded CC0 harp, piano, flute, cello, and viola remain the shared palette.
Variation must change phrasing, harmony, rhythmic motion, register, or texture;
changing only gain does not make a separate arrangement.

| Cue ID | Relationship | Scene purpose and audible character to review |
| --- | --- | --- |
| `first_light` | Core; curiosity | Spacious first memory, tenderness and a sense of beginning. No grand destiny or supernatural revelation. |
| `home_theme` | Core; home | Familiar domestic warmth, an expressive piano melody and an unhurried sense of welcome. Also supports the hopeful afterword. |
| `garden_growth` | Core; observing | Patient, light outdoor discovery. Small melodic exchanges leave room for the garden recording and a child's questions. |
| `workshop_play` | Core; making | Tactile, rhythmically varied piano and harp figures for experimenting, sorting, and constructing. Curious rather than comic mishap music. |
| `storytelling` | Core; imagining | A shaped, flowing melody for following a story or a route across a map. More narrative motion than a sustained wonder pad. |
| `friendship_theme` | Core; friendship | Answering phrases that suit making room for another person. Affection without romance or a premature farewell. |
| `discovery_theme` | Core; curiosity in motion | Bright melodic movement for Joren's invitation and the pleasure of finding how things work. |
| `outward_paths` | Core; exploring | Forward movement with space to notice things. Distinct from the busier workshop rhythm; no threat or chase. |
| `wonder_theme` | Core; scale and attention | Broad, open musical space for the old tree and the view over Lumen. Wonder at an actual place, without implying new metaphysical facts. |
| `festival_theme` | Core; community | The fullest celebratory cue, with melodic and rhythmic variety. Harp remains prominent during the scene's account of Selene performing. |
| `rain_refuge` | Core; shelter | Intimate companionship under the roof. Leave the audible rain room to carry the setting. |
| `grief_theme` | Core; grief | Fragmented, patient phrases and real rests for pain that Maia's comfort cannot immediately fix. |
| `painting_theme` | Core; making while grieving | Quiet purposeful movement and unsettled warmth. Calista can work with her hands without having stopped grieving. |
| `shared_grief` | Core; grief shared | Sparse answering voices for Calista and Cassia. Room for both "I miss him" and the warmer detail of remembering the dome together. |
| `remembrance_theme` | Core; memory in community | A changed return of earlier musical ideas: grief, affection, and continuing life together. No triumphant resolution. |
| `home_tender` | Home variation | Reduced, reassuring arrangement for someone being heard or comforted. Gentle enough for the aftermath of the pond scare. |
| `home_evening` | Home variation | A quieter evening register and slower domestic pulse for settling around a book or ending a day. |
| `storytelling_lullaby` | Storytelling variation | A softer, rocking treatment for Sage's bedtime storytelling; retain melodic identity without adventure-sized gestures. |
| `festival_lanterns` | Festival variation | Reduce the public bustle for personal wishes, then let the melody breathe over the rising lights. Keep the whole loop appropriate to either beat. |
| `friendship_play` | Friendship variation | Livelier call and response for shared maps and invented journeys. Light enough for an ordinary disagreement before it becomes hurtful. |
| `friendship_warm` | Friendship variation | Warm, secure belonging after Lyra is included and after the friends make a compromise. No elegy, ominous turn, or anticipation of Joren's death. |
| `workshop_success` | Workshop variation | The established making idea gains lift and room when the waterwheel actually turns. A child's achievement, not a victory fanfare. |
| `discovery_careful` | Discovery variation | Measured, deliberate movement while the children climb the scaffolding. Concentration without implying an accident is coming. |
| `remembrance_rain` | Remembrance variation | An intimate remembered-friendship texture under rain while the girls make room for old memories and another drawing. |

## Runtime transitions

- Every chapter explicitly plays or stops its score before its first story line.
  Direct chapter selection follows those same statements; it has no separate
  inherited-music lookup that could drift from ordinary reading.
- All plays use the `music` channel and `if_changed`. Adjacent passages sharing a
  cue keep it running. A different cue normally fades the old music out over
  1.5–3 seconds and fades the incoming cue in over 2–4 seconds, as specified in the
  script. These are sequential channel fades, not simultaneous crossfades.
- Music changes occur at script statements, never a timer that guesses when the
  player will finish a line. A cue repeats until a later reader-reached statement
  changes or stops it. Chapter jumps stop the former channels before entering the
  destination; rollback and save/load use Ren'Py's normal music state.
- Pauses inside compositions must remain valid for the entire current subscene.
  A fixed-time crescendo must not announce the waterwheel's success, Lyra's
  inclusion, or an emotional recovery before the corresponding narrative trigger.
- The flute lesson effects remain their own performances. Entry fades settle the
  score, and immediate stops before the actual flute effects prevent a remaining
  fade from masking a note when advancing rapidly. Their original sound files,
  order, and playback levels remain unchanged.
- The Tree of Echoes and the pond splash also finish pending score fades before
  their effects. Music gives way to the physical sounds being described.
- Chapter 25 is unscored. Entry fades remove the preceding warmth; immediate
  music and ambience stops before the accident sentence guarantee silence at the
  news even when the setup is advanced rapidly.

In the table below, an arrow means a reader-reached cue change. "Before" means the
cue statement precedes the quoted line. "After" means the player has dismissed
that line. A cue otherwise continues until the next listed change or chapter.

## Scene and subscene coverage

| Chapter / scene key | Entry and progression | Exact change point and purpose |
| --- | --- | --- |
| 01 `first_memory` | `first_light` → `home_theme` | First memory begins in spacious tenderness. Home enters before "The home I grew to know gathered around a round wooden table," as the story moves from birth into the household. |
| 02 `garden` | `garden_growth` | Entry before "One morning Maia cleared a little patch"; patient observation and planting continue through checking the marker stone. |
| 03 `plant_disagreement` | `garden_growth` | The same cue continues without restarting as the children arrange pots, disagree, and find a workable curve. This is a small practical disagreement, not dramatic tension. |
| 04 `workshop_first` | `workshop_play` → silence → `home_tender` | Stop over 0.4 seconds after "The tune stopped when my elbow caught the jar." Reassurance enters after Arin says "I'll take this side. You start by your feet." The adult is helping; Calista need not earn comfort by finishing the cleanup first. |
| 05 `music_first` | Silence → `home_tender` | No underscore beneath the single broken note or the later hesitant multiple notes. Tenderness enters only after "I raised the flute again. This time I wanted to hear what it would do," for the retrospective closing line. |
| 06 `dorian_stories` | `home_evening` → `storytelling` | Gathering in the library is domestic. Storytelling enters before "I tucked my feet beneath me. He began to tell us about the explorers," after Calista chooses to stay. |
| 07 `sage_story` | `home_tender` → `storytelling_lullaby` | Lyra's upset receives a quiet home arrangement. After "The candlelight moved over the folds of the blanket," the softer storytelling arrangement begins with Sage's tale and stays through bedtime. |
| 08 `family_rhythm` | `home_theme` → `garden_growth` → `workshop_play` → silence → `storytelling` → `home_evening` | Changes follow the montage's actual locations: before "In the garden, Maia showed me a seedling"; before "At Arin's bench"; stop at the music-room scene and again before the practiced flute; storytelling before "In the library, Kael began spreading out the maps himself"; evening music before "At dinner, there was always something to show." It continues through bedtime without another short restart. |
| 09 `tree_echoes` | `wonder_theme` → silence → `wonder_theme` | Fade out after "Let's listen," finish the stop immediately before `tree_creak.wav`, and remain unscored while they identify the moving wood. Wonder returns before "Lumen was a living ship," after Calista puts her ear to the bark. |
| 10 `pond_scare` | Silence → `home_tender` | The slip, splash, rescue, shaking, and initial reassurance stay unscored. Tenderness enters after Calista says "I know. You're here," once Lyra is safely out and held. It accompanies choosing the way home. |
| 11 `soup_experiment` | `home_theme` → silence → `home_tender` | Stop after "Her eyes filled. I set my spoon down quietly." Reassurance enters after Maia says "You can help me make another batch. We'll try the spice together." No comic sting at Lyra's expense. |
| 12 `festival_lights` | `festival_theme` → `festival_lanterns` | The public gathering and performance have the fuller arrangement. Lanterns enters before "Later, each of us took a lantern and made a wish," reducing the bustle for personal wishes and the shared release. |
| 13 `meeting_cassia` | `friendship_theme` | A child's invitation and making space on a blanket. Maintain a welcoming, unforced scale as sketching becomes a shared adventure. |
| 14 `cassia_home` | `friendship_theme` → `garden_growth` | Keep the friendship melody running from the prior chapter. After the explicit time transition, before "On another evening, her father showed us how the gardens shared water," shift to patient observing and connected systems. |
| 15 `meeting_joren` | `discovery_theme` | Joren's active invitation, running together, and wanting to explore again. This is his energy alive in the present. |
| 16 `joren_home` | `workshop_play` | Soren's inventions and the early rover sketch use the making palette, distinguished from running through the construction passages. |
| 17 `kaleb_walk` | `outward_paths` → `friendship_theme` | Forward-moving curiosity for Kaleb's walk and recognizing turnings. After the call returns, `after_joren_family` begins friendship music before "When I introduced Joren to Cassia," continuing through the shared map at home. |
| 18 `treehouse` | `friendship_theme` → `friendship_play` | Belonging during the climb and promise to return. Play enters after "I'll come too," before Joren unrolls the map, and supports the invented island, creature, and journeys. |
| 19 `rain_refuge` | `rain_refuge` | Shelter and companionship throughout the rainy storytelling. The rain itself carries the environment; no late cue change for only the closing sentence. |
| 20 `waterwheel` | `workshop_play` → `workshop_success` | Trying, scraping, measuring, and correcting stay in the working cue. Success enters only after "water pressed against the little wooden paddles," immediately before Lyra's "Look at it go!" |
| 21 `outer_exploration` | `outward_paths` → `discovery_theme` | Finding the way through unfamiliar passages precedes the discovery lift. Change only after the device has actually projected a blueprint and the friends gather around it. Continue through their excited report at home. |
| 22 `lyra_included` | `home_tender` → `friendship_warm` | Listen to Lyra feeling left out first. Warm belonging enters after Calista confirms "With us. Yes," and before the account of Cassia making room and Joren waiting for her. |
| 23 `dome_ascent` | `discovery_careful` → `wonder_theme` | Measured climbing gives way to the open view at the `bg dome` transition, before "Then we were on the platform." No triumphant or ominous climb treatment. |
| 24 `treehouse_dispute` | `friendship_play` → silence → `friendship_warm` | Ordinary shared planning becomes hurtful: stop before "You always want to be in charge." Keep the accusations, Cassia's intervention, and the agreement unscored. Warmth returns before "Through our projects and adventures, we bonded and grew," after the compromise. It remains warm through the last line of chapter 24. |
| 25 `loss` | Silence throughout | Stop the preceding score and ambience at entry. Finish both stops before "An unexpected malfunction caused a catastrophic accident." No score underneath the news, disbelief, comparison with earlier human lives, or empty treehouse. |
| 26 `family_grief` | `grief_theme` | Sparse grief begins only in the new chapter, with Maia trying to comfort Calista. It stays unresolved through the embrace; comfort does not erase the pain. |
| 27 `painting_grief` | `painting_theme` | Change at chapter entry, before "Eventually, I began painting." Room ambience also initializes here for chapter selection. Quiet activity has its own motion, distinct from the previous scene's acute grief. |
| 28 `cassia_grief` | `shared_grief` | Answering voices suit the two friends throughout "I miss him," holding hands, and remembering the dome. The arrangement must accommodate warmer details without overriding their loss. |
| 29 `community_memorial` | Silence → `remembrance_theme` | The plaza and Kaleb's complete speech remain unscored. Remembrance enters only after the reader dismisses "For a while, we stood with him in silence," beneath the communal closing reflection. |
| 30 `mural_remembrance` | `painting_theme` | The earlier act-of-making idea returns for the larger mural, color choices, remembering, and sudden quiet. This is continuing work, distinct from the public memorial's voice. |
| 31 `treehouse_remembrance` | `remembrance_rain` | An intimate remembrance arrangement with rain from entry. Stay gentle through the almost-laugh and the decision to draw the dome together. |
| 32 `annual_remembrance` | `remembrance_theme` → `home_theme` | The communal gathering returns to remembrance, including the line that there will be no new adventures with Joren. The home theme begins only once that final line has been dismissed and the hopeful afterword screen opens. |

## Review cases and acceptance evidence

The following are separate checks. Passing a source or numerical check does not
mean that a composition has passed a listening review.

| Check | Evidence required |
| --- | --- |
| Full coverage | Every one of the 32 chapter labels initializes music before its first narrative line. Every delivered instrumental cue has a reachable literal playback use. |
| Reader timing | Waterwheel success, inclusion, festival wishes, and the chapter-24 reconciliation change only at their documented script anchors. Slow reading must never trigger a future emotional change. |
| Protected silence | In actual runtime state, no underscore accompanies the flute performances, pond rescue, accident sentence, or Kaleb's memorial speech. Rapid advancement cannot leave a pending fade audible over the protected effects/news. |
| Chapter selection | Jump directly to formerly inherited scenes: Kaleb's walk, outer exploration, painting, Cassia's grief, mural, rainy remembrance, and annual remembrance. Verify the same entry cue as continuous reading. |
| Playback continuity | Adjacent identical cues do not restart; different cues make deliberate sequential fades. Save/load and rollback restore the reached musical state. Effects do not leak across their stop statements. |
| Musical variety | Compare making, outdoor observing, storytelling, friendship, festival, and grieving scenes. They must differ meaningfully in melodic development, rhythm, harmonic phrasing, and texture, not just names or volume. |
| Emotional fit | Listen to complete loops while holding an early line, then a later line, in each associated subscene. Reject a cue whose internal development implies a later event or an emotional resolution the current line has not earned. |
| Balance and rendering | Check decoded and true peaks, DC, stereo, loop boundaries, intended loudness groups, and the actual configured playback gains. Preserve intentional differences between celebration, intimacy, grief, effects, and the closing vocal song. |
| Ending contrast | Review chapter 24's last warm lines, the silent news, each distinct grief/remembrance scene, and the afterword in sequence. The score must preserve the sudden loss while allowing later activity and affection to have different musical voices. |

The supplied closing vocal song and its existing credit remain separate from this
instrumental cue map. It plays only when selected from the afterword/end screens;
the score expansion does not rewrite, normalize, or re-encode that performance.
