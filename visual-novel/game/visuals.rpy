# Images remain separate from script so a design can be replaced once.
image cg first_memory = Transform("images/cg/first-memory-young.png", size=(1920, 1080), fit="cover")
image cg garden_compromise = Transform("images/cg/book-one/garden-compromise.png", size=(1920, 1080), fit="cover")
image cg flute_playing = Transform("images/cg/book-one/flute-playing.png", size=(1920, 1080), fit="cover")
image cg flute_rest = Transform("images/cg/book-one/flute-rest.png", size=(1920, 1080), fit="cover")
image cg pond_rescue = Transform("images/cg/book-one/pond-rescue.png", size=(1920, 1080), fit="cover")
image cg pond_comfort = Transform("images/cg/book-one/pond-comfort.png", size=(1920, 1080), fit="cover")
image cg cassia_storytelling = Transform("images/cg/book-one/cassia-storytelling.png", size=(1920, 1080), fit="cover")
image cg family_embrace = Transform("images/cg/book-one/family-embrace.png", size=(1920, 1080), fit="cover")
image cg cassia_comfort = Transform("images/cg/book-one/cassia-comfort.png", size=(1920, 1080), fit="cover")
image cg treehouse_friends = Transform("images/cg/book-one/treehouse-friends.png", size=(1920, 1080), fit="cover")
image bg garden = Transform("images/backgrounds/garden.png", size=(1920, 1080), fit="cover")
image bg garden_close = Transform("images/backgrounds/garden-close.png", size=(1920, 1080), fit="cover")
image bg family_home = Transform("images/backgrounds/family-home.png", size=(1920, 1080), fit="cover")
image bg community_courtyard = Transform("images/backgrounds/community-courtyard.png", size=(1920, 1080), fit="cover")
image bg construction_path = Transform("images/backgrounds/construction-path.png", size=(1920, 1080), fit="cover")
image bg treehouse = Transform("images/backgrounds/treehouse-shaded.png", size=(1920, 1080), fit="cover")
image bg treehouse_rain = Transform("images/backgrounds/treehouse-rain.png", size=(1920, 1080), fit="cover")
image maia = book_actor("images/characters/maia.png")

init python:
    def book_stage(side):
        # Positions describe the visible floor, not character height. The
        # treehouse's clear floor is farther back than its foreground furniture;
        # both children receive the same camera-distance multiplier there.
        if any(renpy.showing(name) for name in ("bg treehouse", "bg treehouse_rain", "bg treehouse_later", "bg treehouse_memory")):
            return ({"left": .335, "near_left": .365, "center": .395,
                     "near_right": .425, "right": .455}[side], 825, 0.76)
        if renpy.showing("bg construction_path"):
            return ({"left": .42, "near_left": .46, "center": .50,
                     "near_right": .54, "right": .58}[side], CHARACTER_LAYOUT["foot_y"], 1.0)
        return ({"left": .18, "near_left": .32, "center": .50,
                 "near_right": .72, "right": .82}[side], CHARACTER_LAYOUT["foot_y"], 1.0)

transform at_left:
    xalign book_stage("left")[0]
    yanchor 1.0
    ypos book_stage("left")[1]
    zoom book_stage("left")[2]

transform at_right:
    xalign book_stage("right")[0]
    yanchor 1.0
    ypos book_stage("right")[1]
    zoom book_stage("right")[2]

transform at_center:
    xalign book_stage("center")[0]
    yanchor 1.0
    ypos book_stage("center")[1]
    zoom book_stage("center")[2]

transform at_near_left:
    xalign book_stage("near_left")[0]
    yanchor 1.0
    ypos book_stage("near_left")[1]
    zoom book_stage("near_left")[2]

transform at_near_right:
    xalign book_stage("near_right")[0]
    yanchor 1.0
    ypos book_stage("near_right")[1]
    zoom book_stage("near_right")[2]

# The two speaking voices of Calista are distinguished by name and typography.
define n = Character(None, what_color="#f0e9dc")
define r = Character("Calista · remembering", who_color="#cdb78e", what_italic=True, what_font="fonts/Lato-Italic.ttf")
define c = Character("Cali", who_color="#c9d7b0")
define m = Character("Maia", who_color="#e4bb88")
define a = Character("Cassia", who_color="#d3b1c8")
define j = Character("Joren", who_color="#e6b095")

# Selected RGB actors have a deliberate green backing, removed during rendering.
# Source art remains unmodified; desktop and WebGL use the same shader.
init python:
    # Only a nearby confidently green backing permits edge cleanup. This keeps
    # green eyes/cloth intact and catches yellow spill in blonde hair, where red
    # is too strong for a simple green-minus-red key. White hair remains opaque.
    renpy.register_shader("astravus.chroma_green", variables="""
        uniform sampler2D tex0;
        uniform vec2 res0;
        varying vec2 v_tex_coord;
    """, fragment_functions="""
        float astravus_green_backing(vec3 color) {
            return smoothstep(0.32, 0.48, color.g - max(color.r, color.b))
                * smoothstep(0.55, 0.75, color.g);
        }
    """, fragment_300="""
        float dominance = gl_FragColor.g - max(gl_FragColor.r, gl_FragColor.b);
        float backing = astravus_green_backing(gl_FragColor.rgb);
        float natural_green = gl_FragColor.r * 0.8 + gl_FragColor.b * 0.2;
        float green_spill = max(0.0, gl_FragColor.g - natural_green);
        float edge = backing;
        // Skin, white hair, and clear backing do not need neighborhood reads.
        if (green_spill > 0.0 && backing < 1.0) {
            for (int y = -3; y <= 3; y++) {
                for (int x = -3; x <= 3; x++) {
                    vec2 offset = vec2(float(x), float(y)) / res0;
                    // Probe the source level: mipmaps hide tiny backing gaps.
                    edge = max(edge, astravus_green_backing(texture2D(tex0, v_tex_coord + offset, -10.0).rgb));
                }
            }
        }
        float key = max(backing, edge * max(smoothstep(0.06, 0.32, dominance),
                                           smoothstep(0.0, 0.14, green_spill)));
        // Color spill reaches slightly farther into fine blonde curls than
        // the alpha matte. Broaden only the color cleanup, preserving the
        // established silhouette and isolated green irises/interior colors.
        float spill_edge = edge;
        if (green_spill > 0.0 && backing < 1.0) {
            for (int y = -1; y <= 1; y++) {
                for (int x = -1; x <= 1; x++) {
                    vec2 offset = vec2(float(x), float(y)) * 5.0 / res0;
                    spill_edge = max(spill_edge, astravus_green_backing(texture2D(tex0, v_tex_coord + offset, -10.0).rgb));
                }
            }
        }
        float spill = spill_edge * smoothstep(0.01, 0.08, green_spill);
        gl_FragColor.g = mix(gl_FragColor.g,
            min(gl_FragColor.g, natural_green), spill);
        gl_FragColor *= 1.0 - key;
    """)
