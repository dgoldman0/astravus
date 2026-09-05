"""Editable chamber-score notation; no audio/runtime dependencies.

All timing uses quarter beats. This is also the validation inventory: a new
cue must have a declared form, duration, dynamics and story use.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import re

from score_material import MATERIAL
from score_new_material import NEW_MATERIAL


# Bass plus close middle-register voicing. Inversions keep bass lines moving
# in smaller steps; sevenths/sixths add colour without a continuous high pad.
CHORDS = {
    "C": (48, 55, 60, 64), "Cmaj7": (48, 55, 59, 64), "C6": (48, 55, 57, 64),
    "C/E": (52, 55, 60, 64), "Am": (45, 52, 57, 60), "Am7": (45, 55, 60, 64),
    "Am/E": (52, 57, 60, 64), "F": (41, 53, 57, 60), "Fmaj7": (41, 52, 57, 60),
    "F6": (41, 50, 57, 60), "F/A": (45, 53, 57, 60), "G": (43, 55, 59, 62),
    "G6": (43, 52, 59, 62), "G7": (43, 53, 59, 62), "Gsus4": (43, 55, 60, 62),
    "G/B": (47, 55, 59, 62), "Dm": (50, 57, 62, 65), "Dm7": (50, 57, 60, 65),
    "Dm9": (50, 57, 60, 64), "Dm/F": (53, 57, 62, 65), "Em": (40, 52, 55, 59),
    "Em7": (40, 50, 55, 59), "E7": (40, 52, 56, 62), "D": (50, 57, 62, 66),
    "Dmaj7": (50, 57, 61, 66), "D/F#": (42, 57, 62, 66), "D7": (50, 57, 60, 66),
    "Bm": (47, 54, 59, 62), "Bm7": (47, 54, 57, 62), "Gmaj7": (43, 54, 59, 62),
    "A": (45, 57, 61, 64), "A7": (45, 55, 61, 64), "Asus4": (45, 57, 62, 64),
}


def parse_bar(text, meter):
    """Return (offset, MIDI or None, beats); reject malformed/overfull bars."""
    events, offset = [], 0.0
    for token in text.split():
        match = re.fullmatch(r"(r|[A-G][#b]?\d):([0-9]+(?:\.[0-9]+)?)", token)
        if not match:
            raise ValueError(f"Invalid score token: {token}")
        name, length = match.groups()
        length = float(length)
        if length <= 0:
            raise ValueError(f"Nonpositive note length: {token}")
        pitch = None
        if name != "r":
            pitch = 12 * (int(name[-1]) + 1) + dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)[name[0]]
            pitch += 1 if "#" in name else -1 if "b" in name else 0
        events.append((offset, pitch, length))
        offset += length
    if abs(offset - meter) > 1e-6:
        raise ValueError(f"Bar has {offset} beats, expected {meter}: {text}")
    return tuple(events)


@dataclass(frozen=True)
class Section:
    name: str
    bars: tuple
    lead: str
    texture: str
    energy: float = 1.0
    countermelody: bool = False


@dataclass(frozen=True)
class Score:
    name: str
    title: str
    bpm: float
    meter: int
    time_signature: str
    family: str
    balance_group: str
    target_lufs: float
    sections: tuple
    parent: str | None = None
    direction: str = ""

    @property
    def beats(self):
        return sum(len(section.bars) for section in self.sections) * self.meter

    @property
    def duration_seconds(self):
        return round(self.beats * 60 / self.bpm * 48000) / 48000

    @property
    def rms(self):
        return {"ordinary": .065, "reflective": .049, "grief": .040}[self.balance_group]


@dataclass(frozen=True)
class Note:
    beat: float
    length: float
    midi: int
    instrument: str
    gain: float
    role: str
    section: str


def core(name, data):
    lead, texture = data["lead"], data["texture"]
    A, B = tuple(data["A"]), tuple(data["B"])
    # A statement, conversational answer, contrasting middle and settled return.
    # Swapping the lead changes attack and sustain, not just instrument colour.
    answer = {"piano": "harp", "harp": "piano", "flute": "harp", "viola": "piano"}[lead]
    if texture in ("still", "intimate"):
        answer = "piano"
    sections = (
        Section("statement", A, lead, texture, .86),
        Section("answer", A, answer, texture, .94, texture not in ("still", "intimate")),
        Section("middle", B, lead, texture, 1.02, texture not in ("still", "intimate")),
        Section("return", A[:6] + B[6:], lead, texture, .90),
    )
    if name == "festival_theme":
        # A longer dance form, with an instrumental interlude between returns.
        sections = sections[:3] + (Section("interlude", B, "harp", "garden", .87),) + sections[1:2] + sections[3:]
    return Score(name, data["title"], data["bpm"], data["meter"], data["time_signature"],
                 data["family"], data["balance_group"], data["target_lufs"], sections,
                 direction=data.get("direction", ""))


SCORES = {name: core(name, data) for name, data in (MATERIAL | NEW_MATERIAL).items()}


def variant(name, parent, title, bpm, lead, texture, group, lufs, order, direction):
    source = SCORES[parent]
    A, B = source.sections[0].bars, source.sections[2].bars
    bars = {"A": A, "B": B, "R": A[:4] + B[4:]}
    sections = tuple(Section(("opening", "answer", "return")[i], bars[key],
                            lead if i != 1 else ("piano" if lead in ("harp", "viola") else "harp"),
                            texture, (.84, .94, .88)[i], i == 1 and texture not in ("still", "intimate"))
                     for i, key in enumerate(order))
    SCORES[name] = replace(source, name=name, title=title, bpm=bpm, balance_group=group,
                          target_lufs=lufs, sections=sections, parent=parent, direction=direction)


variant("home_tender", "home_theme", "Gentle Hands", 56, "piano", "intimate", "reflective", -24,
        "ARB", "Reassurance: slower piano breathing, small answering harp phrases, no domestic dance bass.")
variant("home_evening", "home_theme", "Before the Lamps Go Out", 58, "harp", "shelter", "reflective", -24,
        "BRA", "Wind-down: begin with the answering melody, lower harp and a widely spaced piano bass.")
variant("storytelling_lullaby", "storytelling", "The Last Page", 58, "piano", "shelter", "reflective", -24,
        "ARB", "Bedtime telling: shortened gestures, soft piano/harp exchange, no walking pulse.")
variant("festival_lanterns", "festival_theme", "A Wish of Our Own", 64, "harp", "open", "reflective", -24,
        "ABR", "Private wishes: the dance melody opens into a slower harp-led phrase with sustained support.")
variant("friendship_play", "friendship_theme", "Maps We Made", 84, "harp", "discovery", "ordinary", -22,
        "ABR", "Shared imagination: shorter plucked articulation, running answers and a light rhythmic bass.")
variant("friendship_warm", "friendship_theme", "Room for All of Us", 64, "piano", "duet", "ordinary", -22.5,
        "BRA", "Belonging after compromise: settled chamber duet, warm major harmony, no farewell swell.")
variant("workshop_success", "workshop_play", "And It Turned", 92, "harp", "walking", "ordinary", -22,
        "BAR", "The mechanism works: a flowing bass replaces the stop-start pattern; the tune passes to piano.")
variant("discovery_careful", "discovery_theme", "One Rung at a Time", 72, "piano", "measured", "reflective", -24,
        "ARB", "Concentration on the ascent: separated piano steps and rests, without danger stings.")
variant("remembrance_rain", "remembrance_theme", "The Drawing We Began", 58, "piano", "painting", "reflective", -24,
        "BRA", "Remembering while doing: piano and harp gently regain movement; rainfall remains separate.")


def validate_catalog():
    for spec in SCORES.values():
        if spec.bpm <= 0 or spec.meter not in (3, 4):
            raise ValueError(f"Invalid meter/tempo: {spec.name}")
        for section in spec.sections:
            for chord, melody in section.bars:
                if chord not in CHORDS:
                    raise ValueError(f"Unknown chord {chord} in {spec.name}")
                parse_bar(melody, spec.meter)


def compile_score(spec):
    """Realize separate chamber arrangements, retaining authored lead rhythms."""
    result, bar_index = [], 0

    def put(beat, length, midi, instrument, gain, role, section):
        if gain > 0 and length > 0:
            result.append(Note(beat, length, midi, instrument, gain, role, section))

    for section in spec.sections:
        texture, meter = section.texture, spec.meter
        quiet = texture in ("still", "intimate", "shelter", "painting", "open", "remember")
        for local_bar, (symbol, melody) in enumerate(section.bars):
            start, chord = bar_index * meter, CHORDS[symbol]
            # Four-bar phrases breathe at their cadences. This isn't a future
            # narrative cue: every section remains within the same mood.
            phrase_gain = (1.0, .95, 1.04, .86)[local_bar % 4] * section.energy
            def note(offset, length, midi, instrument, gain, role):
                put(start + offset, length, midi, instrument, gain * phrase_gain, role, section.name)

            events = parse_bar(melody, meter)
            for offset, midi, length in events:
                if midi is None:
                    continue
                instrument = section.lead
                # Acoustic plucks keep a decay beyond the notated finger lift;
                # wind/bow lengths leave real breath gaps between phrases.
                duration = length * (.88 if instrument == "flute" else .98)
                if instrument in ("harp", "piano"):
                    duration = max(length * 1.28, 1.05 if quiet else .72)
                if spec.name == "home_evening":
                    midi -= 12
                gain = {"piano": .28, "harp": .31, "flute": .20, "viola": .25}[instrument]
                note(offset, duration, midi, instrument, gain, "melody")

            # Bass is an independent voice, not a four-note string chord every bar.
            if texture not in ("still", "intimate") or local_bar % 2 == 0:
                bass_length = meter * (1.65 if texture in ("still", "intimate") else .98 if quiet else .85)
                bass_instrument = "cello" if texture in ("open", "remember", "still", "intimate") else "piano"
                note(0, bass_length, chord[0], bass_instrument, .095 if quiet else .13, "bass")
            if texture in ("discovery", "workshop", "walking", "dance"):
                note(meter / 2, meter / 2 * .75, chord[0] + 7, "piano", .065, "bass")

            upper = (chord[1], chord[2], chord[3], chord[1] + 12)
            if texture == "hearth":
                # Piano waltz: small inner dyads, moving inversion on beat three.
                for off in (1, 2):
                    for midi in (upper[off - 1], upper[2]):
                        note(off, .85, midi, "piano", .055, "harmony")
            elif texture in ("dance", "walking", "discovery", "workshop"):
                patterns = {
                    "dance": ((.5, 0), (1, 2), (2, 1), (2.5, 2)),
                    "walking": tuple((step + .5, (step + local_bar) % 3) for step in range(meter)),
                    "discovery": ((.5, 0), (1.5, 2), (2.75, 1), (3.5, 3)),
                    "workshop": ((.75, 0), (1.5, 2), (2.5, 1), (3.25, 2)),
                }
                for off, index in patterns[texture]:
                    if off < meter and not (local_bar % 4 == 3 and off > meter - 1):
                        note(off, .72, upper[index] + (12 if texture == "dance" else 0),
                             "harp", .085 if texture != "workshop" else .10, "figure")
            elif texture in ("garden", "light", "tale", "duet"):
                patterns = {"garden": ((.5, 0), (1.5, 2), (2.5, 1)),
                            "light": ((.5, 0), (2.5, 2)),
                            "tale": ((1, 1), (2, 2)),
                            "duet": ((.5, 0), (1.5, 1), (2.5, 2), (3.5, 1))}
                for off, index in patterns[texture]:
                    if off < meter:
                        note(off, 1.4, upper[index], "harp" if section.lead != "harp" else "piano", .074, "figure")
            elif texture in ("shelter", "painting", "measured"):
                for off, index in ((.5, local_bar % 2), (meter / 2 + .5, 2)):
                    note(off, 1.65 if texture != "measured" else .75, upper[index], "harp", .072, "figure")
            elif texture in ("open", "remember"):
                if local_bar % 2 == 0:
                    note(1, meter * 1.65, upper[1], "viola", .063, "harmony")
                note(meter - 1, 2, upper[2], "harp", .066, "figure")
            elif texture in ("still", "intimate"):
                if local_bar % 2 == 1:
                    note(.5, 2.0, upper[1], "harp", .049, "harmony")

            # Bowed interior voice appears as a phrase, never as the same
            # four-note pad under every arrangement. Leave exposed solo bars.
            if texture in ("hearth", "garden", "light", "duet", "shelter", "painting") and local_bar in (0, 4):
                note(.1, meter * 1.75, upper[1], "viola", .060, "harmony")

            # Answer in actual melodic rests, never continuously double the tune.
            if section.countermelody and local_bar % 2 == 1:
                rests = [(off, length) for off, midi, length in events if midi is None and length >= 1]
                for off, length in rests[-1:]:
                    instrument = "piano" if section.lead == "flute" else "flute"
                    note(off, length * .78, upper[2] + 12, instrument, .105, "answer")

            # Only the communal dance has a tiny original tuned pulse.
            if texture == "dance":
                note(0, .23, 45, "pulse", .009, "pulse")
                note(1.5, .19, 52, "pulse", .0055, "pulse")
            bar_index += 1
    return tuple(sorted(result, key=lambda item: (item.beat, item.role, item.midi)))


validate_catalog()
