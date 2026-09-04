# Images remain separate from script so a design can be replaced once.
image cg first_memory = Transform("images/cg/first-memory-young.png", size=(1920, 1080), fit="cover")
image bg garden = Transform("images/backgrounds/garden.png", size=(1920, 1080), fit="cover")
image bg garden_close = Transform("images/backgrounds/garden-close.png", size=(1920, 1080), fit="cover")
image bg family_home = Transform("images/backgrounds/family-home.png", size=(1920, 1080), fit="cover")
image bg community_courtyard = Transform("images/backgrounds/community-courtyard.png", size=(1920, 1080), fit="cover")
image bg construction_path = Transform("images/backgrounds/construction-path.png", size=(1920, 1080), fit="cover")
image bg treehouse = Transform("images/backgrounds/treehouse-shaded.png", size=(1920, 1080), fit="cover")
image bg treehouse_rain = Transform("images/backgrounds/treehouse-rain.png", size=(1920, 1080), fit="cover")
image maia = Transform("images/characters/maia.png", ysize=850, fit="contain")

transform at_left:
    xalign 0.18
    yalign 0.81

transform at_right:
    xalign 0.82
    yalign 0.81

transform at_center:
    xalign 0.50
    yalign 0.81

transform at_near_left:
    xalign 0.32
    yalign 0.81

transform at_near_right:
    xalign 0.72
    yalign 0.81

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
    # New actors use a deliberately saturated green backing. Key by dominance,
    # not an exact RGB value, and suppress spill only along keyed edges.
    # This preserves white hair and pale cloth that a neutral-paper key erases.
    renpy.register_shader("astravus.chroma_green", fragment_300="""
        float dominance = gl_FragColor.g - max(gl_FragColor.r, gl_FragColor.b);
        float key = smoothstep(0.06, 0.32, dominance);
        float spill = smoothstep(0.02, 0.18, dominance);
        gl_FragColor.g = mix(gl_FragColor.g,
            min(gl_FragColor.g, (gl_FragColor.r + gl_FragColor.b) * 0.5), spill);
        gl_FragColor *= 1.0 - key;
    """)
