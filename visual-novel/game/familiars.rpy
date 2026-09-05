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

transform familiar_at(x, y, height):
    anchor (0.5, 1.0)
    pos (x, y)
    ysize height
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
    familiar_at(820, 760, 225)

transform barkley_path:
    familiar_at(1090, 780, 335)

transform nibble_path:
    familiar_at(670, 755, 90)
