# Book I character visual keys

Open [the local review gallery](index.html) in a browser. It works directly from disk with no server, internet connection or external libraries. Choose a character and stage, use the zoom controls to inspect details, or open an original PNG. Calista, Cassia and Joren have an optional early/later comparison. Browser back/forward and the URL fragment preserve character/stage navigation.

The catalog covers the **14 human speakers and 3 familiars depicted in the current Book I visual novel**, across **20 visual sheets**. It does not claim coverage of future-book characters or unnamed crowds. [catalog.json](catalog.json) records the actual selected sheet paths, dimensions, source links, stage notes and production choices. The gallery embeds the same catalog so it remains usable under local-file browser restrictions.

| Group | Character notes and sheets |
| --- | --- |
| Parents | [Maia](maia/KEY.md), [Arin](arin/KEY.md), [Selene](selene/KEY.md), [Dorian](dorian/KEY.md), [Sage](sage/KEY.md) |
| Childhood friends | [Calista](calista/KEY.md), [Cassia](cassia/KEY.md), [Joren](joren/KEY.md): early and later childhood for each |
| Siblings | [Kael](kael/KEY.md), [Lyra](lyra/KEY.md) |
| Friends’ parents | [Thalia](thalia/KEY.md), [Lyron](lyron/KEY.md), [Soren](soren/KEY.md), [Kaleb](kaleb/KEY.md) |
| Familiars | [Shadow](shadow/KEY.md), [Barkley](barkley/KEY.md), [Nibble](nibble/KEY.md) |

## Reading the references

The [current manuscript](../../../revision/latest.md), established wiki details and author clarifications govern character identity and chronology. Precise costume cuts, palettes, staged poses and previously hidden surfaces are production constructions. A new key angle does not establish additional canon by itself.

The author's current direction is for a naturally human appearance below roughly 100. That guidance does not assign exact ages to the Book I adults or justify importing undated later-life aging into their earlier scenes. Genetic white hair, silver strands or a weathered face must be interpreted with the character's actual stage and source details.

Both friendship stages remain **childhood**. Later limbs and faces mature modestly; the later key is not a late-teen or adult design. Outfits should follow the activity and continuous scene. Home, workshop, exploration, festival, painting and mourning clothes are distinct uses rather than reasons to redraw the character's identity.

Use each key's expressions as a limited range, then choose the performance the scene calls for. Shared scene lighting must preserve complexion and iris pigment; the studio backing and lighting on a key are not a required game background. Sheets fill their own pages independently, so their page heights do not define relative stature. Apply the established cast proportions and familiar ordering: rat smaller than cat smaller than dog.

Lyron's gallery entry uses the current [key.png](lyron/key.png) with the revised asymmetric blue-gray wrap tunic. Earlier garment drafts are not gallery choices.

## Provenance

Per-character notes link prompts, sources and edit records. Detailed generation records include [parent changes](parents-changes.json), [supporting changes](supporting-changes.json) and [trio/familiar changes](trio-familiars-changes.json). Source snapshots and integration receipts retain the hashes and check counts recorded at their respective steps; they are historical evidence, not assertions that mutable production documents still have those hashes. Selected artwork and note hashes identify the current files. The image tool's backend version was not exposed, so these files do not assert verified access to GPT-Image-2.5.

To update the gallery, update `catalog.json` and the matching `catalog-data` JSON block in `index.html` together. Keep selected paths stable and verify every sheet, note and source link. Development discussion and implementation records belong here rather than in canon articles.

The local Chromium check opened all 20 sheets with external network requests blocked. Stage comparison, zoom/reset, deep-link reload and the mobile character selector passed, with no JavaScript errors or mobile page overflow. Desktop and mobile layouts were also visually inspected. This validates the review viewer, not the visual novel's runtime or every artistic decision in a sheet.
