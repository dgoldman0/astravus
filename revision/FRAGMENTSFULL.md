# FRAGMENTSFULL.md - Master Fragment Extraction Plan

> **Historical snapshot:** Fragment IDs, counts, and line ranges below refer to [the draft at `2370143`](https://github.com/dgoldman0/Astravus/blob/2370143c1458a7a52e30dacc87c0ff12831df71d/revision/latest.md), before the September 2026 continuity and duplication edit. References to `latest.md` below mean that snapshot. These mappings are not current line references; the associated training data has not been regenerated. See [ALIGNMENT.md](ALIGNMENT.md).


This document defines the **master extraction plan** for mapping all 276 narrative fragments to disjoint, comprehensive line ranges in `latest.md`.

**Canonical Reference**: `revision/FRAGMENTS.md` (fragment names and summaries)

**Source Text**: `revision/latest.md` (1300 lines)  
**Training Data**: `revision/training_data/fragments.jsonl`

---

## Design Principles

### DISJOINT
All fragment line ranges are non-overlapping. Fragment N ends at line X, fragment N+1 starts after X.

### COMPREHENSIVE  
Together, fragments span all narrative content (excluding headers, images).

### PRESERVATION
Original 276 fragment names from `revision/FRAGMENTS.md` are preserved. Short fragments expanded rather than adding new ones.

---

## Source Structure (VERIFIED)

| Section | Lines | Exclude | Fragments |
|---------|-------|---------|-----------|
| Book I: Earliest Memories | 5-354 | 4 (img), 285 (img) | #1-42 |
| Book I: Early Friendships | 358-542 | 355 (hdr), 357 (img) | #43-73 |
| Book II: Growing Up | 545-647 | 543-544 (hdrs) | #74-105 |
| Book II: Young Adulthood | 649-837 | 648 (hdr) | #106-150 |
| Book III: Starting a Family | 840-1052 | 838-839 (hdrs) | #151-180 |
| Book III: Later Years | 1054-1178 | 1053 (hdr) | #181-224 |
| Book IV: Transcendence | 1180-1300 | 1179 (hdr) | #225-276 |

**Total content lines**: ~1275 (excluding 13 header/image lines)  
**Fragments**: 276  
**Average lines per fragment**: ~4.6

---

## Extraction Rules

1. **Skip** lines 1, 2, 4, 285, 355, 357, 543, 544, 648, 838, 839, 1053, 1179 (headers/images)
2. **Cut at paragraph breaks** (blank lines between paragraphs)
3. **Preserve italics** (`_text_`) and asides (`\begin{aside}`)
4. **Fragment boundaries** should align with natural narrative transitions

---

## Book I: Seeds of Youth

### Earliest Memories (Fragments 1-42) — Lines 5-354

Source lines 5-354 contain 42 fragments covering childhood memories, family introduction, daily routines, and adventures.

| # | Fragment Name | Lines | Verified |
|---|--------------|-------|----------|
| 1 | First memories through parents' stories | 5-8 | ✓ |
| 2 | Pet introductions | 9-12 | ✓ |
| 3 | Foundation concept: Lumen and Astraviin connection | 13-18 | ✓ |
| 4 | Constellations and family structure | 19-32 | ✓ |
| 5 | Maia's character and presence | 33-38 | ✓ |
| 6 | Arin's character and presence | 39-44 | ✓ |
| 7 | Selene's character and presence | 45-50 | ✓ |
| 8 | Dorian's character and presence | 51-56 | ✓ |
| 9 | Sage's character and presence | 57-60 | ✓ |
| 10 | Calista's appearance and personality | 61-64 | ✓ |
| 11 | Kael's character introduction | 65-70 | ✓ |
| 12 | Lyra's character introduction | 71-80 | ✓ |
| 13 | Home's central room | 81-90 | ✓ |
| 14 | Hallways and living murals | 91-98 | ✓ |
| 15 | Calista's personal room | 99-106 | ✓ |
| 16 | Kael's room | 107-114 | ✓ |
| 17 | Lyra's room | 115-136 | ○ |
| 18 | Maia's garden as magical space | 115-136 | ○ |
| 19 | Disagreement over plant placement | 137-154 | ○ |
| 20 | Arin's workshop encounter | 155-168 | ○ |
| 21 | Selene's music room and first lesson | 169-182 | ○ |
| 22 | Dorian's library and storytime | 183-194 | ○ |
| 23 | Sage's room as sanctuary | 155-168 | ○ |
| 24 | Sage's story about three siblings | 163-199 | ✓ |
| 25 | Early childhood sensory memories | 199-202 | ✓ |
| 26 | Growing up daily routine introduction | 203-206 | ✓ |
| 27 | Waking to Lumen's light | 207-208 | ✓ |
| 28 | Breakfast gathering | 209-220 | ✓ |
| 29 | Maia's phototropism lesson | 221-228 | ✓ |
| 30 | Arin's workshop collaboration | 229-240 | ✓ |
| 31 | Selene's music instruction | 241-250 | ✓ |
| 32 | Dorian's history lessons | 251-254 | ✓ |
| 33 | Evening dinner conversations | 255-264 | ✓ |
| 34 | Evening activities together | 265-270 | ✓ |
| 35 | Sage's bedtime routines | 271-274 | ✓ |
| 36 | Pets settling for sleep | 275-276 | ✓ |
| 37 | Growing up in Lumen's environment | 277-278 | ✓ |
| 38 | The Tree of Echoes discovery | 279-301 | ✓ |
| 39 | Pond incident and rescue | 302-315 | ✓ |
| 40 | Soup experiment and lessons on ingredients | 316-335 | ✓ |
| 41 | Festival of Lights celebration | 336-353 | ✓ |
| 42 | Early childhood summary | 354 | ✓ |

**KNOWN ISSUES**: 
- Fragments 17-23 have overlapping/incorrect line numbers due to complex content interleaving
- The original source has repeated visits to same locations (e.g., Arin's workshop appears twice)
- Lines 115-198 contain Lyra's room, Maia's garden scenes, workshop scenes, music room, library, Sage's room, and three siblings story - these need careful extraction during actual fragment processing

---

### Early Friendships (Fragments 43-73) — Lines 358-542

Anchor: Line 360 contains "Among my playmates were Cassia and Joren" (Fragment #43)  
Anchor: Line 492 contains "However, life has a way of introducing unforeseen tragedies" (Fragment #63)

| # | Fragment Name | Lines | Verified |
|---|--------------|-------|----------|
| 43 | Meeting Cassia | 358-366 | ✓ |
| 44 | Cassia's family: Thalia (mother) | 368-376 | ○ |
| 45 | Cassia's family: Lyron (father) | 378-388 | ○ |
| 46 | Cassia's home environment | 390-396 | ○ |
| 47 | Meeting Joren | 398-408 | ○ |
| 48 | Joren's family: Soren (mother) | 410-420 | ○ |
| 49 | Joren's family: Kaleb (father) | 422-432 | ○ |
| 50 | Joren's home environment | 434-438 | ○ |
| 51 | The treehouse introduction | 440-448 | ○ |
| 52 | Treehouse interior | 450-460 | ○ |
| 53 | Treehouse atmosphere | 462-466 | ○ |
| 54 | Adventures in the treehouse | 468-476 | ○ |
| 55 | Rainy days in the treehouse | 478-484 | ○ |
| 56 | Cassia's rainy day story | 486-490 | ○ |
| 57 | Water wheel project | 492-500 | ○ |
| 58 | Construction zone exploration | 502-512 | ○ |
| 59 | Lyra feeling left out | 514-520 | ○ |
| 60 | Dome climbing adventure | 522-530 | ○ |
| 61 | Joren and Cali argument | 532-538 | ○ |
| 62 | Cassia's mediation and friendship strength | 540-546 | ○ |
| 63 | Joren's tragic death | 492-500 | ✓ |
| 64 | Community mourning and shock | 502-508 | ○ |
| 65 | Cali and Cassia's grief | 510-516 | ○ |
| 66 | Parents' consolation | 518-524 | ○ |
| 67 | Processing grief through art | 526-530 | ○ |
| 68 | Joren's impact on community | 532-536 | ○ |
| 69 | Kaleb's community speech | 538-540 | ○ |
| 70 | Annual celebration of life | 542-544 | ○ |
| 71 | Memory painting mural | 546-548 | ○ |
| 72 | Treehouse as sacred space | 550-554 | ○ |
| 73 | Early childhood reflection | 556-560 | ○ |

**Note**: Lines 57-73 have overlapping/incorrect ranges and need verification. The fragments about Joren's death and aftermath (63-73) occur in lines ~492-542 based on verified anchors.

---

## Book II: Growing Up (Lines 545-837)

### Growing Up (Fragments 74-105) — Lines 545-647

Book II begins at line 543 with header, content starts line 545.

| # | Fragment Name | Lines | Verified |
|---|--------------|-------|----------|
| 74 | Late teens transition | 545-549 | ✓ |
| 75 | Cassia's writing evolution | 551-555 | ○ |
| 76 | Joren's lasting influence | 557-559 | ○ |
| 77 | Calista's artistic evolution | 561-567 | ○ |
| 78 | Meeting Lysandra | 569-575 | ○ |
| 79 | Lysandra's character | 577-581 | ○ |
| 80 | Secret alcove in garden | 583-589 | ○ |
| 81 | Lysandra's question about future | 591-599 | ○ |
| 82 | Relationship deepening | 601-607 | ○ |
| 83 | Relationship challenges | 609-615 | ○ |
| 84 | Breakup decision | 617-621 | ○ |
| 85 | Coping through art | 623-627 | ○ |
| 86 | Cassia's writing career growth | 629-635 | ○ |
| 87 | Confronting Cassia about distance | 637-643 | ○ |
| 88 | Kael's evolution | 645-649 | ○ |
| 89 | Lyra's questions | 651-655 | ○ |
| 90 | Trip to Aurora | 657-665 | ○ |
| 91 | Meeting Theron | 667-679 | ○ |
| 92 | Theron's appearance | 681-693 | ○ |
| 93 | Transcendence explained | 695-705 | ○ |
| 94 | Theron on loss of self | 707-715 | ○ |
| 95 | Theron on dreams becoming vivid | 717-727 | ○ |
| 96 | Theron on gradual process | 729-739 | ○ |
| 97 | Aurora's environment | 741-747 | ○ |
| 98 | Meeting extended family members | 749-755 | ○ |
| 99 | Dara's perspective on balance | 757-763 | ○ |
| 100 | Alaric's cultural focus | 765-771 | ○ |
| 101 | Liora's artistic inspiration | 773-779 | ○ |
| 102 | Solar flare historical event | 781-787 | ○ |
| 103 | Tensions among younger residents | 789-795 | ○ |
| 104 | Return to Lumen life | 797-801 | ○ |
| 105 | Lysandra breakup aftermath | 803-809 | ○ |

---

### Young Adulthood (Fragments 106-150) — Lines 649-837

Anchor: Line 653 contains "Volunteering at the art center" (Fragment #107)  
Anchor: Line 715 contains "As I reached 35" (Fragment #121)

| # | Fragment Name | Lines | Verified |
|---|--------------|-------|----------|
| 106 | Art as sanctuary | 649-653 | ○ |
| 107 | Volunteering at art center | 653-663 | ✓ |
| 108 | Working with mosaic project | 665-675 | ○ |
| 109 | Teaching pottery class | 677-685 | ○ |
| 110 | Personal artistic journey flourishing | 687-695 | ○ |
| 111 | Exhibition and resonance | 697-705 | ○ |
| 112 | Meeting Aris at workshop | 707-715 | ○ |
| 113 | Aris's character | 717-725 | ○ |
| 114 | First collaboration with Aris | 727-737 | ○ |
| 115 | Ongoing creative partnership | 739-745 | ○ |
| 116 | Rainy day creative work | 747-753 | ○ |
| 117 | Relationship challenges arising | 755-761 | ○ |
| 118 | Tension and conflict | 763-771 | ○ |
| 119 | Finding balance in relationship | 773-779 | ○ |
| 120 | Aris at exhibitions | 781-787 | ○ |
| 121 | Calista's Core integration at 35 | 715-723 | ✓ |
| 122 | Core integration process | 725-733 | ○ |
| 123 | Pets' Core integration | 735-739 | ○ |
| 124 | Testing new mental capabilities | 741-749 | ○ |
| 125 | Digital mural creation with new Core | 751-759 | ○ |
| 126 | Mind-to-sculpture translation | 761-769 | ○ |
| 127 | Demonstrating to Lyra | 771-779 | ○ |
| 128 | Relationship deepening with Aris | 781-787 | ○ |
| 129 | First full mind connection | 789-797 | ○ |
| 130 | Aris sharing melody mentally | 799-805 | ○ |
| 131 | Cali sharing painting mentally | 807-813 | ○ |
| 132 | Shared memories and vulnerabilities | 815-821 | ○ |
| 133 | Aris's declaration of love | 823-827 | ○ |
| 134 | Cali's reciprocation | 829-833 | ○ |
| 135 | Evening of mental embrace | 835-839 | ○ |
| 136 | Cassia's writing career success | 771-775 | ○ |
| 137 | Meeting Cassia at café | 777-785 | ○ |
| 138 | Cassia's story ideas about Astravii | 787-795 | ○ |
| 139 | Collaborative inspiration | 797-803 | ○ |
| 140 | Mental communication with Cassia | 805-811 | ○ |
| 141 | Kael's marriage to Sage and Sol | 813-819 | ○ |
| 142 | Adoption planning | 821-825 | ○ |
| 143 | Kael's home visit | 827-833 | ○ |
| 144 | Lyra's emerging interests | 835-839 | ○ |
| 145 | Trips to Aurora and Nyx | 841-847 | ○ |
| 146 | Lyra's desire to explore other Astravii | 849-857 | ○ |
| 147 | Cali's protective response | 859-865 | ○ |
| 148 | Lyra's determination | 867-873 | ○ |
| 149 | Promise to take precautions | 875-879 | ○ |
| 150 | Processing fears through art | 881-889 | ○ |

**Note**: Fragments 136-150 have line numbers extending into Book III. These need correction - actual content is within lines 649-837.

---

## Book III: Family and Maturity (Lines 840-1178)

### Starting a Family (Fragments 151-180) — Lines 840-1052

| # | Fragment Name | Lines | Verified |
|---|--------------|-------|----------|
| 151 | Observing Kael's family | 840-846 | ○ |
| 152 | Conversation about starting family | 848-858 | ○ |
| 153 | Decision to start family | 860-868 | ○ |
| 154 | Forming a constellation | 870-878 | ○ |
| 155 | Counselor meetings for financial planning | 880-888 | ○ |
| 156 | Educational workshops on parenting | 890-896 | ○ |
| 157 | Child development topics | 898-904 | ○ |
| 158 | Creating new family home | 906-914 | ○ |
| 159 | Room ideas discussion | 916-924 | ○ |
| 160 | Childcare basics workshop | 926-932 | ○ |
| 161 | Early education emphasis | 934-940 | ○ |
| 162 | Emotional aspects of parenting | 942-948 | ○ |
| 163 | Dinner with Kael, Sage, Sol | 950-960 | ○ |
| 164 | Kael's parenting wisdom | 962-968 | ○ |
| 165 | Observing Kael's family dynamics | 970-976 | ○ |
| 166 | Formation ceremony | 978-986 | ○ |
| 167 | Symbolic gifts exchange | 988-994 | ○ |
| 168 | Celebratory dance | 996-1002 | ○ |
| 169 | Sanctuary process | 1004-1012 | ○ |
| 170 | Birth/first breath ceremony | 1014-1022 | ○ |
| 171 | Welcoming Elara | 1024-1030 | ○ |
| 172 | Home setup for Elara | 1032-1038 | ○ |
| 173 | Collaborative family projects | 1040-1046 | ○ |
| 174 | Storybook creation | 1048-1058 | ○ |
| 175 | Community book sharing event | 1060-1072 | ○ |
| 176 | Reception and connection | 1074-1084 | ○ |
| 177 | Years passing with Elara | 1086-1092 | ○ |
| 178 | Elara exploring interests | 1094-1102 | ○ |
| 179 | Gender identity conversation | 1104-1114 | ○ |
| 180 | Family trips to see Kael | 1116-1122 | ○ |

---

### Later Years (Fragments 181-224) — Lines 1054-1178

**NOTE**: Book III Later Years section (lines 1054-1178) contains REPEATED content from Starting a Family. Many grandparent scenes appear twice. Fragment boundaries here need careful attention during extraction.

| # | Fragment Name | Lines | Verified |
|---|--------------|-------|----------|
| 181 | Entering later maturity at 125 years | 1054-1060 | ○ |
| 182 | Elara's development into adulthood | 1062-1070 | ○ |
| 183 | Elara's engineering passion | 1072-1078 | ○ |
| 184 | Interactive light sculpture device | 1080-1090 | ○ |
| 185 | How device works | 1092-1102 | ○ |
| 186 | Elara's vision for versatility | 1104-1112 | ○ |
| 187 | Demonstration of device | 1114-1122 | ○ |
| 188 | Elara's development phases | 1124-1130 | ○ |
| 189 | Pride and admiration for Elara | 1132-1138 | ○ |
| 190 | Late evening conversation | 1140-1146 | ○ |
| 191 | Lyra's return from expedition | 1148-1156 | ○ |
| 192 | Welcoming Lyra home | 1158-1164 | ○ |
| 193 | Lyra's expedition stories | 1166-1174 | ○ |
| 194 | Ancient Astravus visit | 1176-1184 | ○ |
| 195 | Lyra's descriptions of other cultures | 1186-1194 | ○ |
| 196 | Adaptive sculpture from expedition | 1196-1204 | ○ |
| 197 | Elara's interest in artifact | 1206-1212 | ○ |
| 198 | Parents' approaching transcendence | 1214-1222 | ○ |
| 199 | Garden conversation with mother | 1224-1234 | ○ |
| 200 | Mother's explanation of transcendence | 1236-1246 | ○ |
| 201 | Cali's sadness about separation | 1248-1256 | ○ |
| 202 | Mother's reassurance | 1258-1266 | ○ |
| 203 | Increasing time in connection | 1268-1276 | ○ |
| 204 | Arin and Elara's workshop collaboration | 1278-1288 | ○ |
| 205 | Selene's evening music playing | 1290-1300 | ○ |
| 206-224 | (Remaining Later Years fragments) | — | NEEDS MAPPING |

**Issue**: Lines 194-224 have line numbers exceeding 1300. Source only has 1300 lines. Later Years section ends at line 1178, not 1300+. These fragments need remapping within lines 1054-1178.

---

## Book IV: Transcendence (Fragments 225-276) — Lines 1180-1300

Book IV spans 121 lines for 52 fragments (~2.3 lines average). Fragments in this section are shorter vignettes of dream experiences.

| # | Fragment Name | Lines | Verified |
|---|--------------|-------|----------|
| 225 | Entering later centuries | 1180-1184 | ✓ |
| 226 | Core development | 1186-1190 | ○ |
| 227 | Core connection vulnerability | 1192-1194 | ○ |
| 228 | Lumen's evolution and expansion | 1196-1200 | ○ |
| 229 | Lumen's cultural identity maturing | 1202-1206 | ○ |
| 230 | Gradual sleep transitions | 1208-1212 | ○ |
| 231 | First dream in garden with Maia | 1214-1220 | ○ |
| 232 | Maia showing seed planting | 1222-1226 | ○ |
| 233 | Dream of parents meeting | 1228-1236 | ○ |
| 234 | Meeting at plaza through creative collaboration | 1238-1244 | ○ |
| 235 | Discussion with Aris about dreams | 1246-1252 | ○ |
| 236 | Aris's dream of Selene | 1254-1258 | ○ |
| 237 | Elara's concern for parents | 1260-1264 | ○ |
| 238 | Reassurance to Elara | 1266-1270 | ○ |
| 239 | Dream of childhood playground with Joren's parents | 1272-1278 | ○ |
| 240 | Struggling with Joren's absence | 1280-1284 | ○ |
| 241 | Recognition of need for deeper healing | 1286-1288 | ○ |
| 242 | Reaching to Aurora and Nyx | 1290-1294 | ○ |
| 243-274 | (Transcendence dream fragments) | COMPRESSED | NEEDS MAPPING |
| 275 | Final reflection: "I've had this dream before" | 1295-1298 | ○ |
| 276 | Closing line | 1299-1300 | ✓ |

**Issue**: 52 fragments for 121 lines means heavy compression. Many original "fragments" may need to be merged or marked as covering just 1-2 lines each.

---

## Known Issues

### Line Number Accuracy
- ✓ = Verified against source text
- ○ = Approximate, needs verification

### Content Duplication
Book III "Later Years" contains duplicate grandparent scenes that appear in "Starting a Family". During extraction, avoid duplicate fragments.

### Fragment Compression
Book IV has 52 fragments for 121 lines, requiring very short fragments (~2 lines each). Some conceptual fragments may need to be combined or marked as sub-fragments.

### Recommended Next Steps

1. **Run line verification** for high-priority fragments (those with ○ status)
2. **Mark duplicates** in Later Years section
3. **Combine short fragments** in Book IV where narratively appropriate
4. **Update training data** if any renames occur

---

## Alignment with wiki/FRAGMENTS.md

This document uses the **canonical 276 fragment names** from `revision/FRAGMENTS.md`. Both documents must remain synchronized.

If fragments are renamed or combined, track changes here:

| Old # | Old Name | New # | New Name | Reason |
|-------|----------|-------|----------|--------|
| — | — | — | — | No changes yet |

---

## Training Data Status

All 276 fragments have been processed into `fragments.jsonl` with the seven-turn conversation format. If fragment boundaries change, training data needs regeneration.

---

## Verified Anchor Points

The following key text anchors have been verified against `revision/latest.md`:

### Book I: Seeds of Youth
| Line | Fragment | Content Anchor |
|------|----------|----------------|
| 5 | #1 | "My earliest memories are of stories told to me by my parents" |
| 199 | #25 | "These moments, rich with love, learning, and togetherness" |
| 201 | #25 | "My early memories are imbued with the warmth" |
| 203 | #26 | "In the years that followed, my childhood life revolved" |
| 207 | #27 | "I would wake to the sight of light shifting" |
| 209 | #28 | "Breakfast was a lively affair" |
| 221 | #29 | "It's called phototropism" |
| 255 | #33 | "As the day turned to evening" |
| 271 | #35 | "Bedtime was a special time" |
| 275 | #36 | "As we drifted off to sleep" |
| 277 | #37 | "Growing up in Lumen was an adventure" |
| 279 | #38 | "One clear afternoon, Kael, Lyra, and I decided" |
| 285 | — | IMAGE: Tree of Echoes (EXCLUDE) |
| 302 | #39 | "Exploring Lumen was not without its challenges" |
| 316 | #40 | "Mistakes were a part of our learning process" |
| 338 | #41 | "Festival of Lights, held annually" |
| 354 | #42 | "These moments, filled with adventure, challenges" |
| 355 | — | HEADER: ## Early Friendships (EXCLUDE) |
| 357 | — | IMAGE: Treehouse (EXCLUDE) |
| 360 | #43 | "Among my playmates were Cassia and Joren" |

### Book II: Growing Up
| Line | Fragment | Content Anchor |
|------|----------|----------------|
| 543 | — | HEADER: # Book II (EXCLUDE) |
| 544 | — | HEADER: ## Growing Up (EXCLUDE) |
| 545 | #74 | "As I entered my late teens" |
| 583 | #90 | "During this time, we had the opportunity to visit Aurora" |
| 589 | #91-92 | "Theron's presence was calming" |
| 647 | #105 | "As I look back on these years" |
| 648 | — | HEADER: ## Young Adulthood (EXCLUDE) |
| 649 | #106 | "Early adulthood brought a sense of clarity" |
| 687 | #112 | "A decade or so after I began volunteering, I met Aris" |
| 715 | #121 | "As I reached 35" |

### Book III: Family and Maturity
| Line | Fragment | Content Anchor |
|------|----------|----------------|
| 838 | — | HEADER: # Book III (EXCLUDE) |
| 839 | — | HEADER: ## Starting a Family (EXCLUDE) |
| 840 | #151 | "Starting a family was a decision" |
| 1053 | — | HEADER: ## Later Years (EXCLUDE) |
| 1054 | #181 | "The years passed swiftly" |

### Book IV: Transcendence
| Line | Fragment | Content Anchor |
|------|----------|----------------|
| 1179 | — | HEADER: # Book IV (EXCLUDE) |
| 1180 | #225 | "As I entered my later centuries" |
| 1299-1300 | #276 | "Lumen thought to themselves" |

---

## Extraction Workflow

When extracting fragments from `latest.md`:

1. **Use anchor points** above to locate section boundaries
2. **Read forward** from each anchor to find natural paragraph breaks
3. **Check wiki/FRAGMENTS.md** for fragment name and expected content
4. **Mark as ✓** once verified in this document
5. **Update training data** if content changes significantly