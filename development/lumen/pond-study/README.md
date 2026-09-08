# The garden pond

Open the [comparison page](review.html) for the pond, waterwheel, overview, section, rescue and comfort views, with a divider and side-by-side comparisons. Its [Blender-file link](review.html#blend-link) opens the matching `.blend`, containing editable geometry, saved cameras and packed reference images and textures.

The study covers one pond and its immediate ground, planting and timber boundary. It reconstructs these from the current VN references, with no layout or terrain inherited from the rejected local model. The fragment does not establish a home, neighborhood or vessel plan.

Read the [source observations](source-observations.md) alongside the [garden pond](../../../visual-novel/game/images/backgrounds/book-one/garden-pond.png), [waterwheel](../../../visual-novel/game/images/backgrounds/book-one/waterwheel.png), [rescue](../../../visual-novel/game/images/cg/book-one/pond-rescue.png) and [comfort](../../../visual-novel/game/images/cg/book-one/pond-comfort.png) images. They guide shoreline, composition, supported positions and dry gathering space without supplying measured blueprints.

The current proposed inner shoreline spans approximately **3.8 × 2.8 metres**. Water sits **6.5 centimetres below the nominal paving top**, over a sloped bed with roughly **15–25 centimetres of water** across its shallow hollow. Individual stones and marginal surfaces vary. Broad dry paving continues beyond the water’s edge.

Those metre values follow a chosen camera: **1.7 metres above the paving, looking down 23°, with a 62° horizontal field of view**. The traced inner coping edge is projected onto the nominal paving plane at **z = 0**; water is placed below it separately. Fitting that edge does not independently prove the camera height, basin dimensions or depth. Different camera assumptions can produce a different physical reconstruction of the same illustration.

Flagstones form a fitted paving plan with narrow recessed joints. Their footprints are reconciled before the individual stones are built, replacing the overlapping rows and independently placed slabs. [Photographed CC0 rock maps](textures/README.md) provide surface colour, roughness and relief; the layout still comes from the reconstruction.

All published views share one saved scene. The wheel and feed fitting have a project state; rescue and comfort use static mannequins with proposed limb lengths and inspectable contacts. The checks do not establish character designs, whole-body collision clearance, balance or rescue dynamics. The section follows the modeled bed and cuts the actual paving meshes without vertical exaggeration.

CPU Cycles renders the native meshes and surface materials. The water has small modeled ripples, refraction and reflections of the surrounding scene. Reflection strength and transmitted shadows are adjusted for appearance; this does not validate fluid movement or the mechanics of the actions. Visual acceptance remains open. No canon, manuscript or VN changes are indicated by this study; its proposed details remain unadopted.

Each complete publication has a versioned folder. One manifest selects all six renders and their saved scene, preventing mixed revisions. Missing views remain unavailable, and individual camera renders stay private previews.

The study is built with **Blender 4.0.2**. Rebuilding the fitted paving requires the host `python3` to have **Shapely 2.1 or later**, backed by **GEOS 3.12 or later** for ordered Voronoi cells. This dependency belongs to the rebuild helper, outside Blender’s Python. The packed `.blend` does **not** require Shapely to open or render.

To rebuild and check the published set, run from the repository root:

```sh
blender --background --factory-startup --python development/lumen/pond-study/build_pond.py -- --render all
python3 development/lumen/pond-study/check_render_set.py
```

Publishing requires the full render set. The checker compares file hashes, build records and source revisions; source reading and visual inspection remain separate requirements.
