"""Original melodic material for the expanded Book I underscore.

Durations are quarter-note beats, including in the two triple-meter cues.
Each section has eight complete bars.  A return can therefore retain its
recognizable phrase while the renderer changes register and accompaniment.
The comments describe musical intent; they do not establish story facts.
"""


NEW_MATERIAL = {
    # Patient observation rather than a discovery fanfare: the initial rising
    # second opens into a fifth, then leaves space for the garden.  A alternates
    # short questions and longer answers.  B turns toward E minor, reaches its
    # modest high point on C, and descends through a suspended dominant.  Keep
    # the harp attacks round and the accompaniment lightly spaced; a continuous
    # stream of arpeggios would erase the pauses that give this melody its shape.
    "garden_growth": {
        "title": "Room to Grow",
        "bpm": 68,
        "meter": 4,
        "time_signature": "4/4",
        "family": "curiosity",
        "balance_group": "ordinary",
        "target_lufs": -22,
        "lead": "harp",
        "texture": "garden",
        "A": [
            ("G", "r:0.5 G4:0.5 A4:1 D5:1 B4:0.5 r:0.5"),
            ("Cmaj7", "E5:1.5 D5:0.5 B4:1 r:1"),
            ("Em7", "B4:0.5 A4:0.5 G4:1 E4:1 r:1"),
            ("D", "F#4:1 A4:0.5 B4:0.5 A4:1 r:1"),
            ("G/B", "B4:0.5 D5:0.5 G5:1 D5:1 B4:1"),
            ("C6", "A4:1 E5:1 D5:0.5 C5:0.5 r:1"),
            ("Am7", "C5:1 B4:0.5 A4:0.5 E4:1 G4:0.5 A4:0.5"),
            ("D", "F#4:1 A4:1 D5:1 r:1"),
        ],
        "B": [
            ("Em", "r:1 E5:1 B4:0.5 D5:0.5 E5:1"),
            ("Bm7", "F#5:1.5 E5:0.5 D5:1 r:1"),
            ("Cmaj7", "G5:1 E5:0.5 D5:0.5 C5:1 B4:0.5 A4:0.5"),
            ("G/B", "B4:2 D5:1 r:1"),
            ("Am7", "r:0.5 A4:0.5 C5:1 E5:0.5 D5:0.5 C5:1"),
            ("C6", "A4:1.5 G4:0.5 E4:1 r:1"),
            ("G", "G4:1 B4:0.5 D5:0.5 B4:1 A4:1"),
            ("D", "F#4:1 E4:0.5 F#4:0.5 A4:1 r:1"),
        ],
    },
    # A small hands-on invention: displaced piano attacks and the occasional
    # dotted figure provide movement without turning work into slapstick.  The
    # opening fourth and its answering third are the recognizable hook.  B
    # changes the spacing, briefly leans into B minor, and gathers its fragments
    # back into an ordinary dominant cadence.  The groove belongs in the piano
    # and harp interlock; sustained strings should stay out of their way.
    "workshop_play": {
        "title": "Pieces into Motion",
        "bpm": 88,
        "meter": 4,
        "time_signature": "4/4",
        "family": "making",
        "balance_group": "ordinary",
        "target_lufs": -22,
        "lead": "piano",
        "texture": "workshop",
        "A": [
            ("D", "D5:0.5 r:0.5 A4:0.5 D5:1 F#5:0.5 r:1"),
            ("G", "B4:0.5 D5:0.5 r:0.5 E5:0.5 D5:1 B4:0.5 r:0.5"),
            ("D/F#", "A4:0.5 D5:0.5 F#5:0.5 E5:0.5 D5:1 r:1"),
            ("A7", "C#5:0.5 r:0.5 B4:0.5 A4:0.5 G4:1 E4:0.5 r:0.5"),
            ("Bm7", "F#4:0.5 B4:1 D5:0.5 F#5:0.5 E5:0.5 r:1"),
            ("G", "D5:1.5 B4:0.5 A4:0.5 B4:0.5 G4:1"),
            ("D", "r:0.5 A4:0.5 D5:0.5 F#5:0.5 E5:0.5 D5:0.5 A4:1"),
            ("A", "C#5:0.5 B4:0.5 A4:1 E4:1 r:1"),
        ],
        "B": [
            ("Bm", "r:1 B4:0.5 C#5:0.5 D5:1 F#5:1"),
            ("Gmaj7", "E5:0.5 D5:1 B4:0.5 A4:1 r:1"),
            ("Em7", "G4:0.5 B4:0.5 E5:1 r:0.5 F#5:0.5 G5:1"),
            ("A7", "E5:1 C#5:0.5 B4:0.5 A4:0.5 G4:0.5 E4:1"),
            ("D/F#", "r:0.5 F#4:0.5 A4:1 D5:0.5 r:0.5 F#5:1"),
            ("G", "G5:0.5 F#5:0.5 E5:1 D5:1 B4:0.5 r:0.5"),
            ("D", "A4:0.5 D5:0.5 F#5:1 E5:0.5 D5:0.5 r:1"),
            ("A7", "G4:0.5 A4:0.5 C#5:1 E5:1 r:1"),
        ],
    },
    # A conversational triple-meter tune with an actual breath at each reply.
    # The flute can be warm and plain; it is score instrumentation, not the
    # child's in-world flute performance.  A rises from the middle register in
    # two short arcs.  B begins below it, lets the minor harmony suggest the
    # changing possibilities inside a tale, then finds a gentle falling answer.
    # Avoid a heavy bass/chord/chord waltz pattern or mystical drone treatment.
    "storytelling": {
        "title": "The Next Part of the Tale",
        "bpm": 70,
        "meter": 3,
        "time_signature": "3/4",
        "family": "stories",
        "balance_group": "ordinary",
        "target_lufs": -22,
        "lead": "flute",
        "texture": "tale",
        "A": [
            ("C", "E5:1 G5:0.5 E5:0.5 D5:1"),
            ("Fmaj7", "C5:1 A4:1 r:1"),
            ("C/E", "G4:0.5 C5:0.5 E5:1 G5:1"),
            ("G", "A5:0.5 G5:0.5 D5:1 r:1"),
            ("Am", "E5:1.5 C5:0.5 A4:1"),
            ("Dm7", "D5:0.5 E5:0.5 F5:1 A5:0.5 G5:0.5"),
            ("C", "E5:1 D5:0.5 C5:0.5 G4:1"),
            ("G7", "B4:1 D5:1 r:1"),
        ],
        "B": [
            ("Am", "r:0.5 A4:0.5 C5:1 E5:1"),
            ("Em7", "B4:1 D5:0.5 E5:0.5 G5:1"),
            ("F", "A5:1 G5:0.5 F5:0.5 E5:0.5 D5:0.5"),
            ("C/E", "E5:2 r:1"),
            ("Dm7", "F5:0.5 E5:0.5 D5:1 A4:1"),
            ("Am/E", "C5:1 E5:1 r:1"),
            ("Fmaj7", "A4:0.5 C5:0.5 E5:1 D5:0.5 C5:0.5"),
            ("G7", "B4:1 G4:1 r:1"),
        ],
    },
    # Belonging is carried by a simple falling-third answer, not a sweeping
    # romantic swell.  A begins with a clear question and leaves enough air for
    # an answering harp voice.  B starts in B minor, reaches a brief higher
    # register, then returns by a lower, more settled route.  Retain the same
    # identifiable contour in later friendship variants; do not substitute a
    # generic minor-key lament when this theme acquires memories of loss.
    "friendship_theme": {
        "title": "A Place Beside Us",
        "bpm": 66,
        "meter": 4,
        "time_signature": "4/4",
        "family": "friendship",
        "balance_group": "ordinary",
        "target_lufs": -22,
        "lead": "piano",
        "texture": "duet",
        "A": [
            ("D", "F#4:1 A4:1 B4:0.5 A4:0.5 F#4:1"),
            ("Gmaj7", "G4:1 B4:1 A4:1 r:1"),
            ("D/F#", "F#4:0.5 A4:0.5 D5:1 C#5:0.5 B4:0.5 A4:1"),
            ("A", "E5:1 C#5:1 B4:0.5 A4:0.5 r:1"),
            ("Bm7", "F#4:1 B4:0.5 D5:0.5 F#5:1 D5:1"),
            ("G", "E5:1.5 D5:0.5 B4:1 G4:1"),
            ("D", "A4:1 F#4:1 E4:0.5 F#4:0.5 A4:1"),
            ("A7", "G4:1 E4:1 r:1 A4:1"),
        ],
        "B": [
            ("Bm", "D5:2 F#5:1 E5:1"),
            ("Gmaj7", "D5:1 B4:0.5 A4:0.5 G4:1 r:1"),
            ("Em7", "B4:0.5 D5:0.5 E5:1 G5:1 F#5:1"),
            ("A", "E5:1.5 C#5:0.5 A4:1 r:1"),
            ("G", "B4:1 A4:0.5 G4:0.5 D4:1 G4:1"),
            ("D/F#", "F#4:1 A4:1 D5:1 r:1"),
            ("Em7", "G4:1 B4:1 A4:0.5 G4:0.5 E4:1"),
            ("A7", "G4:1 E4:0.5 F#4:0.5 E4:1 r:1"),
        ],
    },
    # Walking brings a steadier pulse than the workshop, but the tune repeatedly
    # rests to let the surroundings matter.  Its long-short-short opening grows
    # into a broader phrase rather than a heroic march.  B changes the harmonic
    # path through E minor and C, then follows a descending line home.  Use a
    # restrained bass pulse and open harp voicings; no grand percussion, ominous
    # anticipation, or triumphant climax belongs underneath ordinary exploring.
    "outward_paths": {
        "title": "Beyond the Familiar Paths",
        "bpm": 84,
        "meter": 4,
        "time_signature": "4/4",
        "family": "exploration",
        "balance_group": "ordinary",
        "target_lufs": -22,
        "lead": "harp",
        "texture": "walking",
        "A": [
            ("G", "D5:1.5 B4:0.5 G4:0.5 A4:0.5 B4:1"),
            ("D", "A4:1 D5:1 F#5:1 r:1"),
            ("Em7", "G5:1 E5:0.5 D5:0.5 B4:1 A4:0.5 G4:0.5"),
            ("C", "E5:2 D5:1 r:1"),
            ("G/B", "D5:0.5 G5:1 B5:0.5 A5:1 G5:1"),
            ("Am7", "E5:1.5 C5:0.5 A4:1 C5:1"),
            ("G", "B4:1 D5:0.5 E5:0.5 D5:1 B4:0.5 A4:0.5"),
            ("D", "F#4:1 A4:1 D5:1 r:1"),
        ],
        "B": [
            ("Em", "E5:1 B4:1 r:0.5 D5:0.5 E5:1"),
            ("Cmaj7", "G5:1.5 E5:0.5 D5:1 C5:1"),
            ("Am7", "A4:0.5 C5:0.5 E5:1 G5:1 A5:0.5 G5:0.5"),
            ("D", "F#5:1 E5:0.5 D5:0.5 A4:1 r:1"),
            ("G", "G5:1 D5:0.5 B4:0.5 G4:1 B4:1"),
            ("C6", "A4:1 C5:1 E5:0.5 D5:0.5 C5:1"),
            ("Em7", "B4:1 G4:1 E4:0.5 G4:0.5 A4:1"),
            ("D", "F#4:1 A4:0.5 B4:0.5 A4:1 r:1"),
        ],
    },
    # Quiet work has a pulse even while grief remains.  Small piano gestures
    # collect into a line, with genuine rests between them; this is neither a
    # funeral procession nor an assertion that painting cures the loss.  A
    # stays close to A minor and its surrounding major chords.  B begins in C,
    # makes one gently brighter rise, and returns with a descending, unfinished
    # answer.  Accompaniment should mark activity without becoming a ticking
    # ostinato or covering the sound of the remembered moments.
    "painting_theme": {
        "title": "What the Hand Remembers",
        "bpm": 62,
        "meter": 4,
        "time_signature": "4/4",
        "family": "remembrance",
        "balance_group": "reflective",
        "target_lufs": -24,
        "lead": "piano",
        "texture": "painting",
        "A": [
            ("Am", "r:1 E4:0.5 A4:0.5 C5:1 B4:0.5 A4:0.5"),
            ("Fmaj7", "G4:1 A4:1 E4:1 r:1"),
            ("C/E", "E4:0.5 G4:0.5 C5:1 E5:1 D5:1"),
            ("G", "B4:1 D5:1 r:2"),
            ("Dm7", "A4:1 F4:0.5 A4:0.5 C5:1 D5:1"),
            ("Am/E", "C5:1.5 B4:0.5 A4:1 r:1"),
            ("F6", "A4:1 G4:0.5 F4:0.5 D4:1 A4:1"),
            ("Em7", "G4:1 E4:1 B4:1 r:1"),
        ],
        "B": [
            ("C", "G4:1 C5:1 E5:1 r:1"),
            ("G/B", "D5:1 B4:0.5 A4:0.5 G4:2"),
            ("Fmaj7", "A4:0.5 C5:0.5 E5:1 G5:1 E5:1"),
            ("Dm7", "F5:1.5 E5:0.5 D5:1 r:1"),
            ("Am", "E5:1 C5:1 A4:1 G4:1"),
            ("F", "F4:1 A4:0.5 C5:0.5 A4:1 r:1"),
            ("Dm7", "D5:1 C5:0.5 A4:0.5 F4:1 E4:1"),
            ("Em7", "G4:1 B4:1 E4:1 r:1"),
        ],
    },
    # Two people can sit with the same absence without continually finding new
    # words for it.  This melody leaves whole beats empty and favors a middle
    # viola register, allowing an occasional piano answer rather than a thick
    # string pad.  The warmer F and C harmonies in B permit a remembered smile
    # without resolving the grief.  There is no climactic high note: the bowing
    # and the spaces between phrases should carry the feeling at a quiet level.
    "shared_grief": {
        "title": "Between the Two of Us",
        "bpm": 56,
        "meter": 3,
        "time_signature": "3/4",
        "family": "friendship",
        "balance_group": "grief",
        "target_lufs": -26,
        "lead": "viola",
        "texture": "intimate",
        "A": [
            ("Am", "E4:2 r:1"),
            ("Fmaj7", "F4:1 A4:1 r:1"),
            ("C/E", "G4:2 E4:1"),
            ("Em7", "B3:1 r:2"),
            ("Dm7", "D4:1 F4:2"),
            ("Am/E", "E4:2 r:1"),
            ("Fmaj7", "A4:1 G4:1 E4:1"),
            ("Em7", "E4:1 r:2"),
        ],
        "B": [
            ("F", "A4:2 C5:1"),
            ("C/E", "G4:2 r:1"),
            ("Dm7", "F4:1 A4:1 G4:1"),
            ("C", "E4:1 r:2"),
            ("Fmaj7", "C4:1 E4:1 A4:1"),
            ("Dm", "F4:2 D4:1"),
            ("Am", "E4:1 C4:1 r:1"),
            ("Em7", "B3:1 r:2"),
        ],
    },
}
