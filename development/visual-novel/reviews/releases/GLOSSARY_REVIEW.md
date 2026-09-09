# Glossary and final wording review — 0.1-alpha

Reviewed September 5, 2026 against the current three story scripts and Book I of [the aligned draft](../../../../revision/latest.md). This is an editorial source/sequence review and a focused glossary runtime review. Image identity, physical layout, audio listening, the full browser run, and final release packages have separate acceptance rows; they are not certified by this document.

## Reader behavior

**Glossary** is available beside People in the reading controls and reading menus. It starts empty. Unintroduced names, descriptions, placeholder rows, and future entry counts are hidden. Definitions update when their cue is displayed, so a reader can open the glossary immediately to understand the current line.

The selector uses the current reading's rollback-aware dialogue history and completed earlier scenes. It never uses persistent book completion or global “seen” dialogue. Loading an early save, rolling back, jumping backward, or beginning again removes later knowledge. Like People, a chapter jump reconstructs knowledge from scenes before its destination; the destination still has to display its own revelation lines. An older save with shortened history recovers completed-scene entries without guessing ahead within the current scene. People and Glossary share Lumen's revealed description.

Keyboard focus, Return/Escape, touch clicks, wheel scrolling and Page Up/Down use the existing menu controls. Scrollbars hide when all content fits. No new pop-up interrupts dialogue. Current menus fit within the 1920×1080 layout, including the additional sidebar and reading-control button.

## Definitions and limits

Exact source anchors and actual display cues are recorded in [game/glossary.json](../../../../visual-novel/game/glossary.json). [The validator](../../../../visual-novel/scripts/check_glossary.py) rejects missing, repeated or moved cue lines and changed source anchors. The following table is the editorial acceptance contract, not a list shown to players.

| Entry / stage | Display cue | Permitted definition | Material deliberately left unrevealed |
| --- | --- | --- | --- |
| First Breath | Scene 1, `opening_003`, “They told me about the Sanctuary…” | A child's birth and welcome; Cali's parents remember hers. Source opening paragraph and Sanctuary's “Birth and First Breath.” | Birth mechanisms, later parenting, Core, transcendence. |
| Sanctuary | Same displayed line | Where children are born and welcomed by waiting parents. | Its placement inside living ships, speculative biotechnology, later characters. |
| Lumen, first description | Scene 1, `opening_008`, “Lumen, the child of Aurora and Nyx…” | Cali's young home and its already-named parentage. Source paragraph begins with the same parentage. | Living-ship identification and later travel. |
| Constellation | Scene 1, `opening_010`, “With Lyra's arrival…” | A committed romantic partnership among adults; the five parents form one and raise a wider family. | No claim that children or familiars are members of the romantic partnership. Author clarification overrides broader wiki usage. |
| Astravus | Scene 7, Sage's “They lived aboard an Astravus…” | A living ship traveling through the cosmos and housing a community, as in the embedded Aria/Bram/Cora story. Source story begins “aboard a great Astravus traveling through the cosmos.” | Does not identify Lumen as that kind of home before scene 9. |
| Tree of Echoes, first description | Scene 9, “The Tree of Echoes. Dorian told us about it.” | The old hollow tree the children have just found, remembered from Dorian's stories. | Gifted seed, transplantation and any claim that its creaks are supernatural speech. |
| Tree of Echoes, expanded | Scene 9, “It grew from a seed another Astravus gave…” | Ancient gifted seed and transplantation when Lumen was founded. Source Tree of Echoes paragraph states both. | No identity swap with the garden's treehouse oak; no mystic mechanism. |
| Lumen, expanded | Scene 9, “Lumen was a living ship…” | Lumen as a young living Astravus, plus the already-revealed parentage and community. Source tree passage identifies the living ship. | No later integration/romance/family history. |
| Astraviin | Scene 25, “In our world, where transcendence…” | The people who live within and share a close bond with an Astravus. Source opening establishes their bond with home; this is the term's first use in the adaptation. | No future ages, Core mechanics or Book II encounters. |
| Transcendence | Same displayed line | Joining with one's Astravus, ordinary in this world and distinct from death. This is the limited contrast made in the source loss passage. | No later explanations by Theron, timelines, sensory experiences, or claim that Joren transcended. |

## Wording changes and retained teaching

Only one story block changes in this round. The opening now says, “With Lyra's arrival, my parents' constellation had three children to raise together.” It uses the term within the family recollection instead of interrupting to define it. The optional definition carries the adults/household distinction. Cali's People entry also replaces its terminology lesson with the immediate family relationships.

Sage's introduction to the living ship remains: it establishes a bedtime story's setting for children. Maia's phototropism explanation remains: Cali has asked why the seedling bends, and this is a teaching scene. Moving either into an optional glossary would remove the characters' reason to speak. Ordinary vocabulary such as prototype and irrigation has enough local context and does not need a lore entry.

The complete scene 24–25 prose is unchanged from HEAD `7b1c760`. The argument, compromise, reflection, explicit turn toward tragedy, moon expedition, malfunction, unsuccessful rescue, shock, mortality reflection and immediate aftermath remain in their source order. Glossary definitions add no new metaphysical explanation to that passage.

## Full sequence editorial check

Every row below passed this reading for source event, order, voice and wording. These are script-level findings; runtime timing, character depiction and audible mix are independently checked in the release matrix.

| Scene | Source passage / required beat | Current finding |
| --- | --- | --- |
| 01 · First memory | First Breath; five parents; older Kael, later Lyra; household and pets | Borrowed memory remains a recollection told by parents. The newborn image ends before Lyra's arrival. Constellation uses the clarified adult meaning and glossary defers the explanation. Lumen begins as a young world. |
| 02 · A small beginning | Maia's sunflower seed and patient care | A physical planting task leads into repeated visits. Marker stone and watering mishap are small connective actions, without new lore or a second invented incident. |
| 03 · Room for both | Kael's light and Cali's pond placement; compromise | Pots, reflections and a shared curved arrangement give the disagreement a concrete resolution. The script requires dry working ground beside the pond. |
| 04 · The scattered pieces | Spilled screws; practical reassurance from Arin | Gathering and sorting precede the reassurance; no mechanical maxim interrupts the child's concern. Three trays are a small adaptation of the source sorting action. |
| 05 · A color you can hear | First shaky flute lesson and Selene's color association | A broken single note precedes “There was a note in there,” followed by a longer attempt, hesitant notes and the invitation to listen. Selene's pale blue is a source-backed association with sound. |
| 06 · Routes through a story | Dorian's history and Kael's wish to follow explorers | His source advice stays connected to the map and children's interest. No invented historical expedition or unexplained visions. |
| 07 · Three ways forward | Dessert hurt; Sage's fictional siblings cooperate | Aria's failed search, Bram's diagnosis, Cora's filter and shared repair remain ordered. Astravus is introduced within that story; it does not assert the siblings are residents of Lumen. |
| 08 · The days between | Repeated home routines and developing skills | Explicitly many days, not one crowded day. Kael's crystals are a dream; Nibble the mouse is a fictional bedtime namesake of the real rat. Practice succeeds after the first lesson. |
| 09 · The Tree of Echoes | Separate ancient tree, gifted seed, listening, Lumen reveal | Tree history unfolds as Cali recalls it. Creaking wood suggests a voice without speaking. Lumen's living-ship description appears at the actual revelation, in both menus. |
| 10 · The shallow water | Lyra falls in a shallow pond; siblings help her out | Rescue precedes reassurance; wet clothes and the wait to stand carry the fear. No drowning injury or unsupported aftermath is added. |
| 11 · A little too much | Lyra's strong spice; Maia makes another batch with her | The mistake is repaired through tasting and smaller amounts. Lyra's intention survives; the scene does not humiliate her or reduce it to a lecture. |
| 12 · Wishes in the light | Annual festival, Maia's flowers, Selene's harp, wishes | Family experience leads into wider community and the next friendship. Cali's art wish and Kael's exploration wish remain. It is the same named central plaza as remembrance. |
| 13 · An invitation | Cassia's mythical-creature story and invitation | Cali participates and draws; purple/gold creature eyes belong to an explicitly imagined story, not either girl's real eyes. |
| 14 · Room for another story | Thalia's listening, Lyron's shared water, creative home | Two visits are separated by “On another evening.” Parents' work emerges through questions and activity. Shared living systems are ecological context, not magic. |
| 15 · Something worth finding | Joren's construction-zone challenge | Source challenge and eager acceptance are retained. No invented mystical blue-light meeting; the group explores ordinary construction passages. |
| 16 · Things we could make | Soren's systems work and Cali's rover idea | Drawing and parts are a beginning, not a completed new canon invention. Soren is Joren's mother. |
| 17 · Beyond the familiar paths | Kaleb's guided exploration | Distinguishes finding an unseen place from noticing something others missed. Recognizing the turning is an immediate practical action; no new expedition history. |
| 18 · Our place in the branches | Established upper treehouse, lower hollow, return promise | This is a familiar return, with a ladder and accumulated belongings. The lower hollow is distinct from the upstairs room. Their map is imaginary play; Joren's promise is established before loss. |
| 19 · A story under the rain | Shared rainy refuge and imagined talking trees | Cassia proposes an imagined world. The conversation never asserts the real treehouse oak talks. It ends as shared listening before the older-project sequence. |
| 20 · Something that turns | Growth transition, Arin's guidance, miniature waterwheel | “As we grew” precedes older-child staging. Failed clearance, correction and shared success make the project understandable; it remains a small pond wheel. |
| 21 · The unfinished world | Tools/scanner, siblings, construction machinery and blueprint | This later exploration follows the first meeting. Projected plans and autonomous machinery come from the source. The group returns home exhilarated. |
| 22 · A place beside us | Lyra feels excluded; apology and inclusion | “Sometimes” versus “not nearly enough” connects earlier participation honestly to her later hurt. She is included without promising the children will never get ahead again. |
| 23 · The view from above | Happy dome climb, imagined journeys, safe descent | The dome is an adventure they finish together, not the later fatal expedition. Its view becomes a concrete memory in scene 28. |
| 24 · Which way we go | Artifact-hunt dispute; Cassia/pets; cooperation reflection | Source ending and its “foundation for the challenges ahead” are preserved. No unrelated final line replaces the transition. |
| 25 · The news | Explicit tragic turn; routine moon trip; malfunction, failed rescue, grief | Connected source paragraphs remain intact and ordered. No invented casualty list, accident mechanism, farewell, ascension clarification or supernatural return. Glossary waits for the actual terms. |
| 26 · What comfort can do | Maia's source comfort and Cali's pain | “Spirit” is explicitly grounded in stories and memories. The embrace offers company; it does not resolve grief. |
| 27 · What the hand remembers | Painting and familiar companions | The task gives Cali something to do while grieving. Speaking to whoever is present, sometimes Shadow, is ordinary companionship. |
| 28 · Between the two of us | Cassia's question, shared handholding and remembered adventures | The treehouse promise and dome callback refer to earlier played scenes. No invented special blue light, ghost or metaphysical reassurance. |
| 29 · The names we carry | Plaza mourning; Soren's inventions; Kaleb's address | Public sorrow follows private grief. Source wording of Kaleb's tribute remains attached to a recognizable father and community, with time for silence. |
| 30 · A place to remember | Mural in Maia's garden | Painting recalls adventures already shared and imagined. The garden provides ordinary sound, visitors and activity around the work. |
| 31 · The rain returns | Treehouse drawings/messages, rain, remembering | New drawings are acts of remembrance, not adventures with a living Joren. The dome subject is already established; rain remains weather and shared memory. |
| 32 · What remains | Annual gatherings and continuing absence | Retrospective wording allows passing years without asserting a fixed sprite age at every anniversary. No new adventures with Joren. The hopeful afterword is a separate editorial invitation, not a new in-universe event. |

## Evidence and limits

- `python3 -m unittest discover -s tests -p 'test_glossary.py' -v`: **9/9 passed**, including every before/at cue boundary, source validation, old truncated history, future history rejection and current-reading reconstruction.
- `python3 scripts/check_glossary.py`: **8 entries / 10 reveal stages passed**.
- `python3 scripts/project.py test --headless --suite glossary_review`: **25/25 assertions passed**, real Linux Ren'Py 8.5.3 runtime. Log: `test-results/native-glossary.log`; screenshots: `test-results/screenshots/glossary-*.png`. Inspected menu empty state and early/late definitions at full screen; inactive scrollbars removed.
- Ren'Py lint passed after implementation: **658 dialogue blocks / 7,857 words**. This round changes only the six-word reduction in the constellation block.
- Browser harness now checks every actual reveal, saved full knowledge after reload, and glossary equivalence across all 32 chapter jumps. **Fresh integrated browser execution remains a release check**, not a pass claimed here.

Reviewed story-file SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `game/script.rpy` | `28e20b7d091628ae2ada9c1acebf80ecde01d5042fe26241d778875a9f5945fe` |
| `game/family_book_one.rpy` | `236741cddb927cfee503326f2c3549b8be8fa1d37b9e29bf904d6a7fa852a722` |
| `game/friendships_book_one.rpy` | `92a061d5ba9ecf9706434c3817c2c08fdec2fbfa916f182f9e1fb4c8530cef0b` |
| `../revision/latest.md` | `f42fbc68f9469a91f27cfe07903a7dfb9046dffbfb54e59d0ab1462ea83d59b3` |

The complete scene 24–25 dialogue, one decoded block per line, hashes to `32b00481d8b3014da8029c4882ad048a3d6825f329ae8acea58841732307f733` and matches HEAD. This hash covers the entire two-scene prose; the earlier review's differently delimited transition hash is not a replacement for it.
