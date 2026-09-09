# The same selected artwork supplies scene companions and guide illustrations.
# Paws/tails stay above the dialogue panel. Scale and placement belong to each
# setting; Nibble is much smaller than Shadow, who is smaller than Barkley.
image shadow = Transform("images/familiars/shadow.png", mesh=True, shader="astravus.chroma_blue")
image barkley = Transform("images/familiars/barkley.png", mesh=True, shader=("astravus.chroma_green", "astravus.barkley_edge"))
image nibble = Transform("images/familiars/nibble.png", mesh=True, shader="astravus.chroma_green")

# Shadow's green eyes must survive compositing, so her backing uses blue.
init python:
    # Barkley's source has a few green-dominant flecks 9–14 source pixels
    # inside the tail fringe. This extra, source-local probe is exclusive to
    # him: natural gold fur (red > green) and every other actor are unchanged.
    renpy.register_shader("astravus.barkley_edge", variables="""
        uniform sampler2D tex0;
        uniform vec2 res0;
        varying vec2 v_tex_coord;
    """, fragment_350="""
        vec3 barkley_source = texture2D(tex0, v_tex_coord, -10.0).rgb;
        float barkley_dominance = barkley_source.g - max(barkley_source.r, barkley_source.b);
        if (barkley_dominance > 0.0 && gl_FragColor.a > 0.0) {
            float barkley_edge = 0.0;
            for (int y = -2; y <= 2; y++) {
                for (int x = -2; x <= 2; x++) {
                    vec2 offset = vec2(float(x), float(y)) * 8.0 / res0;
                    vec3 nearby = texture2D(tex0, v_tex_coord + offset, -10.0).rgb;
                    float backing = smoothstep(0.32, 0.48, nearby.g - max(nearby.r, nearby.b))
                        * smoothstep(0.55, 0.75, nearby.g);
                    barkley_edge = max(barkley_edge, backing);
                }
            }
            float barkley_spill = barkley_edge * smoothstep(0.0, 0.06, barkley_dominance);
            gl_FragColor.g = mix(gl_FragColor.g,
                min(gl_FragColor.g, gl_FragColor.r * 0.8 + gl_FragColor.b * 0.2), barkley_spill);
            gl_FragColor *= 1.0 - barkley_edge * smoothstep(0.02, 0.20, barkley_dominance);
        }
    """)

    renpy.register_shader("astravus.chroma_blue", fragment_300="""
        float dominance = gl_FragColor.b - max(gl_FragColor.r, gl_FragColor.g);
        float key = smoothstep(0.06, 0.32, dominance);
        float spill = smoothstep(0.02, 0.18, dominance);
        gl_FragColor.b = mix(gl_FragColor.b,
            min(gl_FragColor.b, (gl_FragColor.r + gl_FragColor.g) * 0.5), spill);
        gl_FragColor *= 1.0 - key;
    """)

    def familiar_surface_position(x, y, height):
        if renpy.showing("bg construction_room"):
            # Keep the small companions above the dialogue gradient: Shadow
            # on the doorway floor, Nibble on the clear front workbench.
            return {820: (1360, 760, 185), 1090: (1150, 915, 310),
                    670: (760, 610, 90)}.get(x, (x, y, height))
        if renpy.showing("bg music_room") and (x, y, height) == (910, 735, 90):
            # Nibble scurries past on the floor, below the piano bench.
            return (910, 825, 90)
        return (x, y, height)

transform familiar_at(x, y, height):
    anchor (0.5, 1.0)
    pos familiar_surface_position(x, y, height)[:2]
    ysize familiar_surface_position(x, y, height)[2]
    fit "contain"

# Home: Shadow on the sofa, Barkley by the open door, Nibble on the table.
transform shadow_home:
    familiar_at(185, 545, 215)

transform barkley_home:
    familiar_at(1640, 760, 380)

transform nibble_home:
    familiar_at(775, 595, 105)

# Open foreground between the standing children, clear of their faces/hands.
transform shadow_path:
    # Construction has no floor at the generic waist-high display line. The
    # companions sit on the foreground paving; Nibble can use the work ledge.
    familiar_at(*((835, 1020, 165) if renpy.showing("bg construction_path") else (820, 760, 225)))

transform barkley_path:
    familiar_at(*((1040, 1030, 300) if renpy.showing("bg construction_path") else (1090, 780, 335)))
    # The clearing's cool skylight softens his sunlit source without losing
    # the golden coat. Other scenes retain its original color and alpha.
    matrixcolor TintMatrix("#d5e3f5" if renpy.showing("bg echoes") else "#ffffff")

transform nibble_path:
    # Passing the resolved tuple also restarts this transform on a location
    # change; reusing identical ATL arguments can preserve its previous pose.
    familiar_at(*familiar_surface_position(670, 755, 90))
