# Worldbuilding work

For Lumen spatial design, start with `development/lumen/Lumen-Space-Inventory.md` and query its source register with `python3 development/lumen/lumen-study/space_inventory.py`. Run `--check` to find stale sources or unmapped scenes/images. This is a reading aid, not a substitute for reading the relevant narrative and viewing the actual current VN images.

Before drawing or sizing a home/neighborhood, account for every required space in scope, including work, music, reading, care, each resident's privacy, household outdoors and shared places. An unresolved attachment stays explicitly unplaced; it is not permission to omit the space. Record any deliberate combination of uses. Do not treat a room symbol, a source hash or complete scene-ID coverage as proof of a complete architectural program.

The current inventory covers Book I and selected supporting wiki provisions. Extend it from full relevant source reads before claiming all-books or whole-vessel coverage. Current author clarifications and VN visual priority control the study. Keep canon in the wiki; label proposals and any required manuscript/VN changes. The old household/neighborhood sketches are withdrawn as layout bases.

`development/lumen/Lumen-Local-Connections.md` records the current LC01 connection proposal. Read it before developing the local model; its room attachments and upper private passage remain proposed. Run `python3 development/lumen/lumen-study/build_connections.py --check` when changing the proposal. A passed route check does not establish dimensions, camera fit or a validated 3D layout.

# Committing

Use detailed informative commit messages. Do not amend existing commits; use follow-up commits.

# Canon and development

The wiki is for established canon, lore and information about the canon. Keep design proposals, source audits, numerical experiments, implementation notes, ideation and development logs in `development/`; production records can remain beside the manuscript or VN they concern. Use `development/README.md` to find active work and `development/LOG.md` for history. When a detail is settled, describe the resulting fact in the wiki without copying its planning discussion there.

The earlier dialogue collection is now `development/dialogue/`. It mixes excerpts with expanded scenes and is not a transcript of the current story. Check quotations and added staging against current sources before using them as canon evidence.

# Generated writing

Python and other generators may help assemble reference material. Review the resulting content for factual quality, readable wording, repetition and presentation before considering it finished. Keep the main Lumen proposal manually edited; generators may build its detailed reference tools. Do not let generated inventories or design records become wiki articles by default.
