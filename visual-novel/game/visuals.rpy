# Images remain separate from script so a design can be replaced once.
image cg first_memory = Transform("images/cg/first-memory-young.png", size=(1920, 1080), fit="cover")
image bg garden = Transform("images/backgrounds/garden.png", size=(1920, 1080), fit="cover")
image bg garden_close = Transform("images/backgrounds/garden-close.png", size=(1920, 1080), fit="cover")
image bg family_home = Transform("images/backgrounds/family-home.png", size=(1920, 1080), fit="cover")
image bg community_courtyard = Transform("images/backgrounds/community-courtyard.png", size=(1920, 1080), fit="cover")
image bg construction_path = Transform("images/backgrounds/construction-path.png", size=(1920, 1080), fit="cover")
image bg treehouse = Transform("images/backgrounds/treehouse-shaded.png", size=(1920, 1080), fit="cover")
image bg treehouse_rain = Transform("images/backgrounds/treehouse-rain.png", size=(1920, 1080), fit="cover")
image calista = Transform("images/characters/calista.png", ysize=730, fit="contain")
image maia = Transform("images/characters/maia.png", ysize=850, fit="contain")
image cassia = Transform("images/characters/cassia.png", ysize=740, fit="contain")
image joren = Transform("images/characters/joren.png", ysize=770, fit="contain")

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

# The generator may flatten a neutral transparency-preview background into RGB.
# Remove that neutral light matte at render time, keeping source art untouched.
# This shader is shared by desktop and WebGL builds.
init python:
    renpy.register_shader("astravus.neutral_matte", fragment_300="""
        float high = max(gl_FragColor.r, max(gl_FragColor.g, gl_FragColor.b));
        float low = min(gl_FragColor.r, min(gl_FragColor.g, gl_FragColor.b));
        float neutral = 1.0 - smoothstep(0.035, 0.08, high - low);
        float paper = smoothstep(0.85, 0.93, low);
        gl_FragColor *= 1.0 - neutral * paper;
    """)

transform clean_sprite:
    mesh True
    shader "astravus.neutral_matte"
