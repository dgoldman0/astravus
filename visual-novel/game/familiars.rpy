# The same selected artwork supplies scene companions and guide illustrations.
# Paws/tails stay above the dialogue panel. Scale and placement belong to each
# setting; Nibble is much smaller than Shadow, who is smaller than Barkley.
image shadow = Transform("images/familiars/shadow.png", mesh=True, shader="astravus.chroma_blue")
image barkley = Transform("images/familiars/barkley.png", mesh=True, shader="astravus.chroma_green")
image nibble = Transform("images/familiars/nibble.png", mesh=True, shader="astravus.chroma_green")

# Shadow's green eyes must survive compositing, so her backing uses blue.
init python:
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
            # The generic path coordinates cross the equipment shelves here.
            return {820: (820, 870, 185), 1090: (1150, 915, 310),
                    670: (735, 860, 90)}.get(x, (x, y, height))
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

transform nibble_path:
    # Passing the resolved tuple also restarts this transform on a location
    # change; reusing identical ATL arguments can preserve its previous pose.
    familiar_at(*familiar_surface_position(670, 755, 90))
