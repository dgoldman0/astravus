# Book I adaptation — version 0.1-alpha

The preview now adapts **all of Book I: Seeds of Youth**, from First Breath to the closing acts of remembrance. It ends before **Book II: Growing Up**, which opens with Calista entering her late teens. The current script organizes that arc into **32 scenes**, defined in `game/book_structure.rpy`. These are production scene divisions, not newly invented source chapters.

The authority for events, relationships, and order is [revision/latest.md](../../revision/latest.md), the aligned prose at commit `23f9766`. Wiki biographies support physical and cultural details; expanded wiki dialogue is not automatically canonical action. When a supporting page conflicts with the draft, follow the draft and document the discrepancy rather than inventing a reconciliation in dialogue.

Version 0.1.3 was a rough opening selection ending at the rainy talking-tree conversation. That first draft remains preserved at commit `3dfcf6c`; [DRAFT_ONE.md](DRAFT_ONE.md) records its scope and limitations. The earlier omissions are not the scope of this version.

## Coverage and condensation

The [detailed coverage map](BOOK_ONE_COVERAGE.md) provides passage anchors and line references. The implemented sequence is:

| Scenes | Source development | Adaptation treatment |
| --- | --- | --- |
| 1–2 | Borrowed First Breath, family orientation, and sunflower lesson | Preserve the contemplative opening. Shift from the newborn illustration to the later household before Lyra and the three-child family are described. The marker stone and watering mishap make care tangible. |
| 3–7 | Plant disagreement, Arin's spilled screws, Selene's first flute lesson, Dorian's explorers, and Sage's bedtime story | Restore individual relationships with each parent. Preserve the conflicts, mistakes, encouragement, and sibling responses through playable exchanges. Sage's Aria/Bram/Cora tale retains its failed search, diagnosis, adapted filter, and cooperation. |
| 8 | Ordinary family days | Combine repeated visits and practice into a retrospective montage through the appropriate rooms. Garden observation, workshop learning, music, maps, meals, sibling rivalry, and bedtime remain present without repeating every introductory explanation. |
| 9–12 | Tree of Echoes, Lyra's pond fall, the soup experiment, and Festival of Lights | Restore discovery, sibling responsibility, repair after a mistake, and the wider community celebration. The tree is separate from Maia's treehouse oak; the pond remains shallow. |
| 13–19 | Meeting Cassia and Joren, visits with both families, Kaleb's walk, the familiar treehouse, and rainy storytelling | Preserve Cassia's invitation and Cali's eager acceptance of Joren's challenge. Establish Thalia, Lyron, Soren, and Kaleb before the later loss. The treehouse visit begins with existing possessions and shared history. |
| 20–24 | Water-wheel project, outer construction exploration, Lyra's exclusion, dome climb, and treehouse dispute | Introduce visibly older childhood designs at the source's growth transition. Preserve the collaborative successes, Lyra's hurt, the happy expedition, and both friends' capacity to argue and compromise. |
| 25–29 | Joren's fatal expedition, family grief, painting, Cassia's grief, and community mourning | Keep the accident on a routine research expedition to a nearby moon, separate from the dome climb. Do not invent a technical cause beyond the malfunction, other casualties, a farewell scene, or a supernatural return. Family comfort and art cannot undo the death. |
| 30–32 | Garden mural, treehouse drawings, rain, and recurring remembrance | New acts of remembrance can continue, but no new adventures with Joren can be added. The annual gatherings are retrospective, without claiming an unchanged child sprite depicts every future year. |

This is a full-book narrative adaptation, not a verbatim reading. Room inventories and repeated explanatory passages are compressed into art, behavior, or montage. Some physical details and minor exchanges are added so a prose summary becomes a playable scene. There are no Book II romances, late-teen pursuits, later expeditions, or alternate endings in this preview.

## Dialogue and voice

Cali's child dialogue is labeled **Cali**. The adult recollection uses **Calista · remembering**, alongside first-person narrative text. A child can speak with enthusiasm, uncertainty, irritation, or care; polishing a line must not turn eager Cali into a habitual skeptic or adventurous Joren into someone who dismisses wonder.

**Constellation** names the adults' romantic partnership. **Family** or **household** includes the children and familiars they live with and care for. Cali's five parents form a constellation; Lyra's arrival grows their family. This follows the author's September 4, 2026 clarification. Some supporting wiki descriptions currently fold children and familiars into the term; use the clarified distinction in the adaptation and People guide.

The expanded scenes give speakers immediate interests: choosing where a plant belongs, finding spilled parts, producing a note, tracing a route, including a sibling, or deciding which way an adventure should go. Gesture and sound should carry part of the meaning before narration names a lesson. Quiet scenes and repeated acts of affection are intentional; brevity alone is not the standard for natural dialogue.

The transition from scene 24 to 25 preserves the source's connected paragraphs. Cassia and the familiars help the children compromise; their shared experiences teach cooperation and empathy, “building a foundation for the challenges ahead.” Scene 25 opens with “However, life has a way of introducing unforeseen tragedies,” followed by the routine expedition and fatal accident. These reflections are part of the narrative connection, not optional summaries to replace with an unrelated afternoon. The source's shock at such a rare death and Cali's thought about mortality remain in their original order, before Cassia's embrace, Lyra's confusion and the empty treehouse. The prose is divided into reading beats while retaining its wording. Maia's comfort keeps the source exchange about Joren living on in their stories, Cali's “But it hurts so much,” and the family leaning on one another. “Spirit” remains the source's language of affection and remembrance.

The approach builds on [the writing research notes](WRITING_NOTES.md). [Arimia's visual-novel guide](https://arimiadev.com/how-to-make-visual-novels/) supports a fixed story carried by writing and presentation; [Nathan Bransford's dialogue guidance](https://nathanbransford.com/blog/2022/10/seven-keys-to-writing-good-dialogue) informs purposeful exchanges and selective conversational detail. The examples in `WRITING_NOTES.md` describe the earlier 0.1.3 pass, not the current book's coverage or validation status.

The 0.2.5 story pass removes the invented blue-light encounter and its grief callback. Joren's introduction follows the draft's challenge and Cali's eager participation; later remembrance recalls the already-played dome visit. Cassia's invitation again draws Cali into her mythical-creature story, with the aligned wiki's shared imagining of its eyes. Dorian's historical advice and Kaleb's memorial address retain the source's words. The source transition from cooperation to tragedy remains intact. See [the complete story and visual review](REVIEW_0_2_5.md).

Small connective details remain: the seed marker, the evolving imaginary map, sorting the source's spilled screws into three trays, and the flower-placement negotiation. They support the existing action and are not new history or world mechanics. The creature and Sage's three siblings remain explicitly fictional; Kael's crystal cave is explicitly a dream. Selene's association of music with color is in the source. The Tree of Echoes makes creaking sounds that suggest speech. Affectionate references to Joren's spirit concern stories and memories, without a supernatural return.

## Revelation and chronology

The preview preserves the draft's gradual disclosure:

1. The opening identifies Lumen as a young world and the child of Aurora and Nyx, without explaining a starship.
2. Sage's embedded story introduces an Astravus as a living ship traveling through the cosmos. It does not yet directly identify Lumen that way.
3. The Tree of Echoes passage directly identifies Lumen as a living ship. That displayed line expands both Glossary and People; the current reading's `lumen_known` flag follows when it is dismissed.
4. The later loss brings the source's reflection on ordinary transcendence, rare death and mortality. Joren's death entry is shown only after the fatal news in the current reading.

People has individual entries for all fourteen speakers, including each parent and sibling. Entries appear with their first spoken line, using the current dialogue history; completed scene progress restores earlier encounters in saves with shortened history. The compact name list makes additions visible. Shadow, Barkley, and Nibble have a separate Familiars section with illustrated profiles; their entries follow the narrated home introduction because they do not speak. These gates belong to the current save and rollback state; finishing the book once should not spoil a fresh beginning. Early backgrounds and menu text must not supply the explanation before the prose does.

The optional Glossary follows the same reading-local principle. Eight terms appear only when their first cue is displayed; Lumen and the Tree of Echoes expand at later lines in their scenes. There are no locked placeholders or future-entry counts. Definitions cite source passages in the data, remain within knowledge available at their cues, and omit later-book mechanics. The opening uses “constellation” in the household recollection without stopping to define it; the glossary carries the adults' partnership definition. Genuine teaching remains in the story, including Maia's phototropism lesson and Sage's introduction to the setting of their bedtime tale. See [the glossary and wording review](GLOSSARY_REVIEW.md).

The chapter picker remains available in the alpha. It reconstructs earlier scene state and encounters, resets the current history and rollback boundary, and resumes the ordinary story flow. The selected scene still delivers its own introductions and revelations. Jumping backward therefore removes later knowledge; it does not unlock the entire People guide. A separate spoiler warning uses the engine's persistent record of viewed dialogue. A jump cannot mark its skipped prefix as read. Readers may cancel, proceed or disable these warnings in Settings. Both desktop and browser builds include this control, independently of Ren'Py's developer-console setting.

After the final story scene, an explicitly separate afterword looks ahead to Calista's friendships, discoveries and adventures. It invites interest and feedback on itch.io for possible adaptations of later books. It adds no new in-universe event and promises no release date.

The newborn illustration ends before later household life. Kael is already older than Cali; Lyra arrives afterward. The early family montage spans ordinary days without inventing exact ages. The water-wheel sequence marks a change to older childhood, not the late-teen period of Book II. Outfits change for home, the festival, later projects, disagreement, mourning, and painting; continuous activities can keep the same clothes. Parental biography ages refer to later life, and Selene's genetically white hair remains an identity trait.

## Staging and atmosphere

The setting must support the line currently being read. Family scenes use the family room, workshop, music room, library, Sage's room, and garden rather than one generic backdrop. Festival, memorial and annual remembrance share one Central Plaza layout and a substantial community crowd. Plant placement uses a broad, dry working area beside the pond and a kneeling illustration; the shallow rescue has separate rescue and comfort illustrations. The miniature waterwheel remains a small project at the garden pond. The dome, mural and remembered treehouse keep their own views. The rain variant preserves the treehouse's open bays and furniture; rain sound begins with the weather change. The remembrance variant adds drawings while retaining that rainy room.

Standing portraits cannot depict playing a flute, climbing, sitting in someone's lap, an embrace, or a wet rescue. Flute playing/resting, the pond rescue/recovery, Cassia's courtyard story, Maia's embrace, and the girls' shared grief use illustrations for those specific actions. Other movements use narration and a speaker portrait when the standing pose is hidden. An illustration suppresses the portrait only for a speaker actually depicted in it; Lyra still has a portrait when she joins the flute practice. The preview has age, clothing, and expression coverage, and all fourteen speaking people have portraits. It does not animate every narrated movement. See [art direction](ART_DIRECTION.md) and [character continuity](CHARACTER_CONTINUITY.md).

The expanded score preserves First Light's motif while providing family, discovery, wonder, festival, shelter, grief, and remembrance cues. Separate flute attempts make practice audible; environmental sound follows the room and weather. Silence has a place at the loss and in listening scenes. The [audio direction](AUDIO_DIRECTION.md) distinguishes measured technical checks from the listening review still needed for timbre and emotional balance.

## Review boundaries

This document describes the adaptation and its intended continuity; it does not certify the current integrated build. Actual playthrough results and platform limitations belong in [VALIDATION.md](VALIDATION.md). The [0.1-alpha story and audio review](POLISH_STORY_AUDIO.md) records the final source pass and measured mix checks. Review the full book from **Begin Book I**: an older save can skip revised material, and the rough draft's save format is intentionally excluded from this rewritten script.
