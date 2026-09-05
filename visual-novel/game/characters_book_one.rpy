# Book I character designs. The chroma key is applied once inside each image.
# Use positional transforms at call sites; do not add the legacy clean_sprite.
# Palette, stage boundaries, and provenance: docs/CHARACTER_CONTINUITY.md.

image calista young = Transform("images/characters/book-one/calista-young.png", ysize=730, fit="contain", mesh=True, shader="astravus.chroma_green")
image cassia young = Transform("images/characters/book-one/cassia-young.png", ysize=740, fit="contain", mesh=True, shader="astravus.chroma_green")
image joren young = Transform("images/characters/book-one/joren-young.png", ysize=770, fit="contain", mesh=True, shader="astravus.chroma_green")

image calista home = Transform("images/characters/book-one/calista-home.png", ysize=730, fit="contain", mesh=True, shader="astravus.chroma_green")
image calista festival = Transform("images/characters/book-one/calista-festival.png", ysize=730, fit="contain", mesh=True, shader="astravus.chroma_green")
image calista festive = Transform("images/characters/book-one/calista-festive.png", ysize=730, fit="contain", mesh=True, shader="astravus.chroma_green")
image calista older = Transform("images/characters/book-one/calista-older.png", ysize=810, fit="contain", mesh=True, shader="astravus.chroma_green")
image calista frustrated = Transform("images/characters/book-one/calista-frustrated.png", ysize=810, fit="contain", mesh=True, shader="astravus.chroma_green")
image calista mourning = Transform("images/characters/book-one/calista-mourning.png", ysize=810, fit="contain", mesh=True, shader="astravus.chroma_green")
image calista painting = Transform("images/characters/book-one/calista-painting.png", ysize=810, fit="contain", mesh=True, shader="astravus.chroma_green")

image cassia older = Transform("images/characters/book-one/cassia-older.png", ysize=820, fit="contain", mesh=True, shader="astravus.chroma_green")
image cassia mourning = Transform("images/characters/book-one/cassia-mourning.png", ysize=820, fit="contain", mesh=True, shader="astravus.chroma_green")
image joren older = Transform("images/characters/book-one/joren-older.png", ysize=835, fit="contain", mesh=True, shader="astravus.chroma_green")
image joren frustrated = Transform("images/characters/book-one/joren-frustrated.png", ysize=835, fit="contain", mesh=True, shader="astravus.chroma_green")

image kael young = Transform("images/characters/book-one/kael-young.png", ysize=810, fit="contain", mesh=True, shader="astravus.chroma_green")
image lyra young = Transform("images/characters/book-one/lyra-young.png", ysize=655, fit="contain", mesh=True, shader="astravus.chroma_green")

image maia home = Transform("images/characters/book-one/maia-home.png", ysize=850, fit="contain", mesh=True, shader="astravus.chroma_green")
image arin everyday = Transform("images/characters/book-one/arin-everyday.png", ysize=835, fit="contain", mesh=True, shader="astravus.chroma_green")
image selene everyday = Transform("images/characters/book-one/selene-everyday.png", ysize=810, fit="contain", mesh=True, shader="astravus.chroma_green")
image dorian everyday = Transform("images/characters/book-one/dorian-everyday.png", ysize=885, fit="contain", mesh=True, shader="astravus.chroma_green")
image sage everyday = Transform("images/characters/book-one/sage-everyday.png", ysize=835, fit="contain", mesh=True, shader="astravus.chroma_green")

# Supporting parents share the same portrait and compositing conventions.
image thalia everyday = Transform("images/characters/book-one/thalia-everyday.png", ysize=845, fit="contain", mesh=True, shader="astravus.chroma_green")
image lyron everyday = Transform("images/characters/book-one/lyron-everyday.png", ysize=880, fit="contain", mesh=True, shader="astravus.chroma_green")
image soren everyday = Transform("images/characters/book-one/soren-everyday.png", ysize=830, fit="contain", mesh=True, shader="astravus.chroma_green")
image kaleb everyday = Transform("images/characters/book-one/kaleb-everyday.png", ysize=880, fit="contain", mesh=True, shader="astravus.chroma_green")
