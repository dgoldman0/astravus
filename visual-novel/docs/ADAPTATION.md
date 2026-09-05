# Book I adaptation — version 0.2.3

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

The approach builds on [the writing research notes](WRITING_NOTES.md). [Arimia's visual-novel guide](https://arimiadev.com/how-to-make-visual-novels/) supports a fixed story carried by writing and presentation; [Nathan Bransford's dialogue guidance](https://nathanbransford.com/blog/2022/10/seven-keys-to-writing-good-dialogue) informs purposeful exchanges and selective conversational detail. The examples in `WRITING_NOTES.md` describe the earlier 0.1.3 pass, not the current book's coverage or validation status.

Connective inventions include the seed marker, Cassia's winged creature and its extra feet, their evolving map, Cali's blue-edged-light drawing, screw sorting, and the particular negotiation over flower placement. These details belong to the adaptation. The imagined creature is not a new species in world lore, and Sage's three siblings remain characters in an embedded story. Remembered details must stay consistent with who originally said or did them.

## Revelation and chronology

The preview preserves the draft's gradual disclosure:

1. The opening identifies Lumen as a young world and the child of Aurora and Nyx, without explaining a starship.
2. Sage's embedded story introduces an Astravus as a living ship traveling through the cosmos. It does not yet directly identify Lumen that way.
3. The Tree of Echoes passage directly identifies Lumen as a living ship. Only then does the current reading's `lumen_known` state expand the People description.
4. The later loss establishes the difference between death and transcendence. Joren's death entry is shown only after that event in the current reading.

People has individual entries for all fourteen speakers, including each parent and sibling. Entries appear with their first spoken line, using the current dialogue history; completed scene progress restores earlier encounters in saves with shortened history. The compact name list makes additions visible. Shadow, Barkley, and Nibble have a separate Familiars section with illustrated profiles; their entries follow the narrated home introduction because they do not speak. These gates belong to the current save and rollback state; finishing the book once should not spoil a fresh beginning. Early backgrounds and menu text must not supply the explanation before the prose does.

The newborn illustration ends before later household life. Kael is already older than Cali; Lyra arrives afterward. The early family montage spans ordinary days without inventing exact ages. The water-wheel sequence marks a change to older childhood, not the late-teen period of Book II. Outfits change for home, the festival, later projects, disagreement, mourning, and painting; continuous activities can keep the same clothes. Parental biography ages refer to later life, and Selene's genetically white hair remains an identity trait.

## Staging and atmosphere

The setting must support the line currently being read. Family scenes use the family room, workshop, music room, library, Sage's room, and garden rather than one generic backdrop. Festival, water-wheel success, the dome view, mourning plaza, mural, and remembered treehouse have distinct views. The rain variant preserves the treehouse's open bays and furniture; rain sound begins with the weather change. The remembrance variant adds drawings while retaining that rainy room.

Standing portraits cannot depict playing a flute, climbing, sitting in someone's lap, an embrace, or a wet rescue. Hide the conflicting pose and let narration carry the action, or use an appropriate illustration. The preview has broader age, clothing, and expression coverage, but it does not animate every narrated movement or provide a portrait for every speaking person. See [art direction](ART_DIRECTION.md) and [character continuity](CHARACTER_CONTINUITY.md).

The expanded score preserves First Light's motif while providing family, discovery, wonder, festival, shelter, grief, and remembrance cues. Separate flute attempts make practice audible; environmental sound follows the room and weather. Silence has a place at the loss and in listening scenes. The [audio direction](AUDIO_DIRECTION.md) distinguishes measured technical checks from the listening review still needed for timbre and emotional balance.

## Review boundaries

This document describes the adaptation and its intended continuity; it does not certify the current integrated build. Actual playthrough results and platform limitations belong in [VALIDATION.md](VALIDATION.md). Review the full book from **Begin Book I** in version 0.2.3: an older save can skip revised material, and the rough draft's save format is intentionally excluded from this rewritten script.
