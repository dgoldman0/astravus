# Writing the kinetic adaptation

**Historical craft notes:** the 0.1.3 examples below do not govern the current script. The 0.2.5 source review removed the invented blue-light/pencil interaction and extra-feet exchange. Their earlier justification was insufficient: natural-sounding stage business still needs to preserve the source encounter’s purpose. Current decisions are in [REVIEW_0_2_5.md](REVIEW_0_2_5.md).

Research reviewed September 4, 2026. These are craft suggestions applied to this story, not rules that override its voice or the author's request to preserve the opening's breathing room.

## Guidance consulted

- VN developer Arimia's [How to Make Visual Novels](https://arimiadev.com/how-to-make-visual-novels/) treats linear novels as a valid form and recommends improving writing and cinematography instead of inserting unrelated gameplay. A visual novel's length should serve its story. For Astravus, reader-controlled timing and changes of scene can support a fixed plot.
- Author/editor Nathan Bransford's [How to write good dialogue in a novel](https://nathanbransford.com/blog/2022/10/seven-keys-to-writing-good-dialogue) emphasizes what speakers want, selective rather than literal conversation, subtext, purposeful physical action, and avoiding exposition between people who already know the facts. This is general dialogue craft, not specifically a kinetic-novel guide.
- VN Paths' [How to Write a Good Visual Novel Story](https://vnpaths.com/how-to-write-a-good-visual-novel-story/) discusses click-paced reading, coordinating text with visuals and sound, varying scene intensity, and checking dialogue aloud. It is supplemental editorial guidance; its route-design advice and general suggestions to shorten prologues are not requirements for this project.

## Application in 0.1.3

The following are adaptation decisions drawn from that guidance and the source audit:

| Concern | Decision and example |
| --- | --- |
| Each line sounded like a polished lesson or setup for a joke | Give the speaker a concrete immediate interest. Cali wants to plant and later draw; Cassia wants someone to join her story; Joren wants to find things. Mild friction comes from those interests, without making friends hostile. |
| Naturalness edits changed characterization | Restore Cali's eager acceptance of Joren's challenge and his curiosity about talking trees. Preserve Maia's affectionate sunflower comparison. Casual wording does not justify a different personality. |
| Facts were delivered for the reader alone | Keep necessary family orientation in retrospective narration. Children discuss the creature, map and tree they are actually imagining, without explaining Lumen's nature to each other. |
| Emotional meaning was over-explained | Cassia asks whether they will still want to visit. Cali initially considers the room's physical size; Joren answers the actual worry. The exchange stays anchored to the draft's promise. |
| Action felt like decorative stage business | Joren's tapping disturbs Cali's drawing; stopping and holding her pencils shows consideration. Maia steadies the watering can. Retain these actions because they affect the interaction. |
| A slow opening stayed on one image | Keep the reflective passage and change its visual context: newborn welcome, later family home, garden. Pauses and transitions follow changes in time or attention. |
| The picture contradicted the line being read | Provide an actual rainy version of the retained room, distinct encounter locations, and earlier-life parents. Remove unsupported movement of furniture. Do not describe an expression change as visible when there is only one sprite pose. |

The line-by-line cadence review checks how each response follows the previous line, whether names are known before use, and whether information is introduced before a later line relies on it. For example, Cassia now establishes four feet before Cali objects to adding two more. The revised build is also checked in the engine for text fit and scene timing.

This is still a quiet childhood chapter. Not every line needs conflict or a joke, and not every click needs a new image. Repetition can carry affection or rhythm; remove it when it merely restates information. The next writing review should assess emotional continuity across the currently omitted family scenes, alongside broader sprite expressions and poses.
