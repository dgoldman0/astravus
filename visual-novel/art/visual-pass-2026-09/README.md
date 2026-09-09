# Book I visual pass

The [before/after viewer](review.html) shows the nine selected artwork changes. The [character-key gallery](../character-keys/index.html) covers all fourteen named human characters and three familiars depicted in Book I, with twenty sheets including separate early and later childhood keys for Cali, Cassia and Joren.

The opening trial was committed as `41c410e` before this pass. Its accepted Arin/Sage refinement is now installed in the game and carried into their everyday sprites. Arin has paler freckled skin and a defined auburn crop; Sage has a rounder face, softer neck and medium build. The two remain recognizably distinct while sharing the tender opening pose.

Lyra's eyes are slightly smaller in her sprite and three illustrations: rescue, comfort and insect discovery. The sprite uses native GIMP geometry; the illustrations use generated facial paint under native GIMP masks. Frightened upward attention, subdued recovery and curious delight remain separate performances. Thalia's sprite irises now read deep green.

Lyron's first sheet over-preserved the inherited denim-shirt and cargo-trouser costume. Following the author's correction, the selected key and sprite use an overlapping blue-gray woven garment, integrated fastening, plain trousers and quiet woven shoes. His face, hazel eyes, salt-and-pepper hair and gentle manner remain. The exact garment construction is a production interpretation of Lumen's materials and culture. Other wardrobes remain selected, as the author clarified that the issue was mainly Lyron.

## Scope and continuity

All 78 selected images were reviewed: 29 human/familiar sprites, 20 illustrations and 29 backgrounds. Nine images changed; the other 69 retain their pixels. [The visual audit](VISUAL_AUDIT.md) records why the scenes, age progression, lighting and remaining artwork were retained. This is Book I coverage, not a claim to key every later-book character or incidental crowd member.

Later childhood starts at the manuscript's growing-older transition, with longer limbs, less rounded faces and activity-specific clothes. No exact new ages are assigned. Parents do not acquire their biographies' later-life appearance in the newborn scene. The author's guidance that younger Astraviin can look mostly human governs anatomy; it does not justify importing a complete contemporary costume. The closing montage recalls different childhood moments, including Joren before his death.

## Tools and reproducibility

All new paint and sheets used the built-in image tool. The backend model version is not exposed, so these results do not independently establish GPT Image 2.5 access. Exact prompts, source images, output IDs and selected hashes are retained in the character-key records and this directory. No API/CLI fallback was used.

GIMP 2.10 creates the masks, composites and editable XCFs. For the three Lyra illustrations, [verification.json](verification.json) records 7,081 / 11,632 / 40,219 changed pixels, respectively, with zero differences outside the actual native masks. Reopening each XCF reproduces its selected composite; hiding the edit restores the original. Facial paint is slightly smoother under extreme magnification, but no conspicuous seams were seen at scene size or in the independent enlarged review.

The native assembly is [assemble_lyra_cg_keys.scm](../../scripts/assemble_lyra_cg_keys.scm). Run it from `visual-novel` with GIMP's Script-Fu batch interpreter and an `audit-dir` string pointing to an existing temporary directory. It writes the three PNG/XCF/mask sets here and reopened/restored checks to that temporary directory. The [opening reproduction](../character-refinement-test/run-gimp-test.sh), [parent reproduction](../character-keys/run-parent-sprite-gimp.sh) and [supporting reproduction](../../scripts/rebuild_supporting_sprites.sh) retain their own recipes. Rebuilds can change PNG container metadata; decoded-pixel equality is the preservation test, while selected file hashes identify the installed copies.

[Production integration](cg-integration.json) and `docs/graphics-edits.json` bind the four installed illustration changes to their immutable inputs and scripts. The original trial's before image is frozen in its own directory, so adopting it does not turn its comparison into an after/after view. Production notes remain outside the canon wiki.

The [viewer check](viewer-check.json) covers the nine source-art comparisons, including split endpoints, detail views and mobile layout. Native Ren'Py results are recorded separately in `runtime-checks.json`; a browser art viewer is not a game-rendering test.
