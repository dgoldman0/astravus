# Book I character designs. The chroma key is applied once inside each image.
# Use positional transforms at call sites; do not add the legacy clean_sprite.
# Palette, stage boundaries, and provenance: docs/CHARACTER_CONTINUITY.md.

init -6 python:
    import json

    with renpy.file("character_layout.json") as layout_file:
        CHARACTER_LAYOUT = json.load(layout_file)

    def book_actor(path):
        framing = CHARACTER_LAYOUT["actors"][path]
        left, top, right, bottom = framing["bounds"]
        # Keep the authored horizontal composition; remove only the variable
        # padding above the hair and below the feet before applying body height.
        # Fine translucent hair tips can vanish while shrinking the source. The
        # reviewed correction is under 1%; native captures verify visible height.
        source = (Transform(path, mesh=True, shader="astravus.chroma_green")
                  if framing["key"] == "green" else path)
        return Transform(source, crop=(0, top, framing["size"][0], bottom - top),
                         ysize=int(round(CHARACTER_LAYOUT["heights"][framing["group"]] * framing["sampling_scale"])),
                         fit="contain")

image calista young = book_actor("images/characters/book-one/calista-young.png")
image cassia young = book_actor("images/characters/book-one/cassia-young.png")
image joren young = book_actor("images/characters/book-one/joren-young.png")

image calista home = book_actor("images/characters/book-one/calista-home.png")
image calista festival = book_actor("images/characters/book-one/calista-festival.png")
image calista festive = book_actor("images/characters/book-one/calista-festive.png")
image calista older = book_actor("images/characters/book-one/calista-older.png")
image calista frustrated = book_actor("images/characters/book-one/calista-frustrated.png")
image calista mourning = book_actor("images/characters/book-one/calista-mourning.png")
image calista painting = book_actor("images/characters/book-one/calista-painting.png")

image cassia older = book_actor("images/characters/book-one/cassia-older.png")
image cassia mourning = book_actor("images/characters/book-one/cassia-mourning.png")
image joren older = book_actor("images/characters/book-one/joren-older.png")
image joren frustrated = book_actor("images/characters/book-one/joren-frustrated.png")

image kael young = book_actor("images/characters/book-one/kael-young.png")
image lyra young = book_actor("images/characters/book-one/lyra-young.png")

image maia home = book_actor("images/characters/book-one/maia-home.png")
image arin everyday = book_actor("images/characters/book-one/arin-everyday.png")
image selene everyday = book_actor("images/characters/book-one/selene-everyday.png")
image dorian everyday = book_actor("images/characters/book-one/dorian-everyday.png")
image sage everyday = book_actor("images/characters/book-one/sage-everyday.png")

# Supporting parents share the same portrait and compositing conventions.
image thalia everyday = book_actor("images/characters/book-one/thalia-everyday.png")
image lyron everyday = book_actor("images/characters/book-one/lyron-everyday.png")
image soren everyday = book_actor("images/characters/book-one/soren-everyday.png")
image kaleb everyday = book_actor("images/characters/book-one/kaleb-everyday.png")
