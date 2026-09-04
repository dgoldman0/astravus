# Book I character continuity

The preview covers **Book I: Seeds of Youth**, ending before Book II's late-teen period. Character designs distinguish the early family memories and first friendships from the later childhood projects, conflict, loss, and remembrance. These stages are adaptation choices; the draft does not date every scene or give the children exact ages for those events.

The authority for events and their order is [`revision/latest.md`](../../revision/latest.md). The [Calista](../../wiki/bios/Calista.md), [Cassia](../../wiki/bios/Cassia.md), [Joren](../../wiki/bios/Joren.md), [Kael](../../wiki/bios/Kael.md), and [Lyra](../../wiki/bios/Lyra.md) biographies supply physical details. Their later-life descriptions must not be treated as photographs of the people in every earlier scene.

## Stages and wardrobe

| Stage | Actor design | Wardrobe and staging |
| --- | --- | --- |
| First Breath | Existing `cg first_memory` | Five earlier-life parents and newborn Cali. No older-child sprite; Lyra has not yet been born. |
| Early family memories | `calista home` | Teal tunic, ochre sash, russet trousers; empty hands for home and learning scenes. |
| Sunflower lesson and first friends | `calista young`, `cassia young`, `joren young` | Their original faces, poses, and play clothes remain the earliest friendship designs, with new backgrounds for clean compositing. |
| Festival of Lights | `calista festival` | Midnight-blue and gold tunic, plum leggings; holds a small amber lantern. It must not appear before she has the lantern or after she sets it down. |
| Later childhood projects and exploration | `calista older`, `cassia older`, `joren older` | Longer limbs and less round faces, with new practical clothes. Introduce at the source's “As we grew older” transition; never regress to young sprites afterward within the continuous story. |
| Treehouse disagreement | `calista frustrated`, `joren frustrated` | Same later-childhood outfits, visibly tense expressions. Change expressions back when the disagreement eases. |
| Grief and remembrance | `calista mourning`, `cassia mourning` | Quiet faces and separate subdued everyday clothes. These are personal clothes, not an invented cultural mourning uniform. |
| Painting the memorial | `calista painting` | Later-childhood face, paint-marked work apron and sleeves; holds brush and palette. Use only when she is painting. |

Outfits are a production design choice, not an assertion that a color, embroidery pattern, or garment was specified in the manuscript. Reusing clothes within one continuous day is deliberate; changing clothes marks different activities and days without forcing a change at every camera cut.

Kael remains Cali's older brother and Lyra her younger sister. Kael has deep warm brown skin, dark tousled hair, and gold-hazel eyes; Lyra has golden-tan skin with olive undertones, golden freckles, unruly golden-blonde curls, and green eyes. Their exact age gaps are not newly specified. Keep Lyra visibly smaller in group blocking. Do not show a smiling dry sprite during the pond rescue or frightened aftermath.

## Parent identities

New parent sprites use the approved First Memory composition as the identity reference. Their everyday appearance belongs to Cali's childhood, with only modest visual aging from that opening. The biographies' later-life “125+” labels do not establish an age at Cali's birth, and Astraviin longevity does not justify applying ordinary human age arithmetic.

| Character | Preserve | Everyday staging |
| --- | --- | --- |
| Maia | Warm brown skin, amber-green eyes, dark curls and small braids; silver streaks are present in the childhood draft. | `maia home` wears a blue-teal blouse and ochre vest, has empty hands, and listens with a tender, concerned expression. Her old seed-holding gardening pose stays in the seed lesson. |
| Arin | Pale freckled skin, short auburn hair, blue eyes, androgynous appearance, capable forearms. | `arin everyday` wears workshop clothes and keeps tools in the apron. Do not stage an exact finger injury date: the biography does not establish when it occurred relative to these scenes. |
| Selene | Deep bronze skin, pure white hair, violet eyes, petite build, long musician's fingers. | `selene everyday` wears plum and teal, with relaxed hands. White hair is genetic, beginning early in adult life; it must not turn the character into an elderly parent in First Memory. |
| Dorian | Rich dark brown skin, glasses, brown eyes, broad shoulders, mixed dark/gray hair. | `dorian everyday` has limited silver at this stage and a notebook in his left hand. No claim that he has already reached the mostly silver beard of the later-life biography. |
| Sage | Warm tan skin with rosy undertones and freckles, short sandy hair, gray eyes, soft androgynous features. | `sage everyday` wears green and russet with bare feet for indoor scenes. Do not use this pose to depict physically holding Lyra; switch staging for that action. |

## Production checks

- Keep faces, skin tone, eye color, and recognizable hair identity stable across wardrobe and emotion variants.
- Distinguish an age change from a wardrobe change. Scaling a young sprite taller alone does not establish aging.
- A standing sprite cannot depict a character sitting in someone's lap, playing an absent instrument, climbing, or embracing another character. Hide it or use a scene illustration for those actions.
- Use restrained grief expressions; a brighter memory may briefly recall Joren, but never imply he is physically present after his death.
- Validate edges against both dark treehouse and brighter garden backgrounds. The generator returned RGB art with a baked transparency preview despite alpha requests. Selected new actors therefore use generated saturated-green backgrounds, removed once by the runtime `astravus.chroma_green` shader. This preserves Selene's white hair and pale highlights that the older light-matte shader could remove. The manifest records actual file modes; runtime compositing must not be described as authored alpha. Call sites apply positioning only, without the legacy `clean_sprite` transform.
- Full prompts, input relationships, output identifiers, dimensions, and hashes live in [`character-assets.json`](character-assets.json). Selected PNGs remain unmodified generated artwork; discarded candidates belong in ignored staging.
