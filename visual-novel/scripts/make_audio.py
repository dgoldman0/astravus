#!/usr/bin/env python3
"""Render Astravus's original Book I audio with NumPy, SciPy, and SoundFile.

No recordings, samples, downloaded impulse responses, or audio-generation models.
Each asset has its own seed. Looping mixes wrap notes and room tails across the
boundary; use playback fades, rather than adding silence to every repetition.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path
import sys
import wave
import numpy as np
from scipy.signal import butter, sosfilt

RATE = 24000
OUT = Path(__file__).resolve().parents[1] / "game" / "audio"
MASTER_OUT = OUT.parents[1] / ".cache" / "audio-masters"
# An optional project-local dependency install never enters the game package.
sys.path.append(str(OUT.parents[1] / ".cache" / "audio-tools"))
try:
    import soundfile as sf
except ImportError as error:
    raise SystemExit("Audio rendering/checking requires SoundFile 0.13.1. See docs/AUDIO_DIRECTION.md.") from error
VORBIS_COMPRESSION = .15  # libsndfile quality = .85; favour timbre over minimum size.
TAU = 2 * np.pi


def canonicalize_ogg(path):
    """Fix only the random Ogg stream serial/checksums for repeatable artifacts.

    Ogg page layout/CRC: https://xiph.org/ogg/doc/framing.html . Compressed
    packets, sample positions, and codec headers remain unchanged.
    """
    table = []
    for value in range(256):
        crc = value << 24
        for _ in range(8):
            crc = ((crc << 1) ^ (0x04C11DB7 if crc & 0x80000000 else 0)) & 0xFFFFFFFF
        table.append(crc)
    data = bytearray(path.read_bytes())
    serial = hashlib.sha256(path.stem.encode("utf-8")).digest()[:4]
    offset = 0
    while offset < len(data):
        if data[offset:offset + 4] != b"OggS" or len(data) - offset < 27:
            raise ValueError(f"Malformed Ogg page in {path}")
        segments = data[offset + 26]
        header_end = offset + 27 + segments
        end = header_end + sum(data[offset + 27:header_end])
        if end > len(data):
            raise ValueError(f"Truncated Ogg page in {path}")
        data[offset + 14:offset + 18] = serial
        data[offset + 22:offset + 26] = bytes(4)
        crc = 0
        for value in data[offset:end]:
            crc = ((crc << 8) & 0xFFFFFFFF) ^ table[((crc >> 24) ^ value) & 0xFF]
        data[offset + 22:offset + 26] = crc.to_bytes(4, "little")
        offset = end
    path.write_bytes(data)


def encode_master(master):
    data, rate = sf.read(master, dtype="float64", always_2d=True)
    target = OUT / (master.stem + ".ogg")
    sf.write(target, data, rate, format="OGG", subtype="VORBIS",
             compression_level=VORBIS_COMPRESSION)
    canonicalize_ogg(target)
    print(f"{target.name:25} {len(data) / rate:6.2f}s  Ogg Vorbis  {target.stat().st_size / 1024:7.1f} KiB", flush=True)


def hz(midi):
    return 440 * 2 ** ((midi - 69) / 12)


def smooth_edges(signal, attack=.02, release=.06):
    signal = signal.copy()
    for length, beginning in ((attack, True), (release, False)):
        n = min(len(signal), max(2, round(length * RATE)))
        envelope = np.sin(np.linspace(0, np.pi / 2, n)) ** 2
        if not beginning:
            envelope = envelope[::-1]
        if signal.ndim == 2:
            envelope = envelope[:, None]
        if beginning:
            signal[:n] *= envelope
        else:
            signal[-n:] *= envelope
    signal[0] = signal[-1] = 0
    return signal


def band_noise(n, rng, low=150, high=4000):
    return sosfilt(butter(2, [low, high], btype="bandpass", fs=RATE,
                          output="sos"), rng.normal(size=n))


def pluck(midi, seconds, rng, velocity=.7):
    """Damped modes, faster upper-partial decay, and a quiet pick transient."""
    t = np.arange(round(seconds * RATE)) / RATE
    signal = np.zeros(len(t))
    for k in range(1, 12):
        frequency = hz(midi) * k * np.sqrt(1 + .000035 * k ** 2)
        if frequency >= RATE * .44:
            break
        amplitude = (1 - .26 * np.cos(k * 1.73)) / k ** 1.5
        signal += amplitude * np.sin(TAU * frequency * t) * np.exp(-t * (1 + .21 * k) / 1.6)
    signal += .021 * band_noise(len(t), rng, 280, 3000) * np.exp(-t * 35)
    return smooth_edges(signal * velocity, .014, .15)


def felt(midi, seconds, rng, velocity=.7):
    t = np.arange(round(seconds * RATE)) / RATE
    signal = np.zeros(len(t))
    for k, amplitude in enumerate((1, .32, .13, .065, .02), start=1):
        frequency = hz(midi) * k * np.sqrt(1 + .00006 * k ** 2)
        voice = sum(np.sin(TAU * frequency * (1 + d) * t) for d in (-.0009, .0009)) / 2
        signal += amplitude * voice * np.exp(-t * (1 + .32 * k) / 2.8)
    signal += .008 * band_noise(len(t), rng, 100, 1800) * np.exp(-t * 55)
    return smooth_edges(signal * velocity, .025, .2)


def bowed(midi, seconds, rng):
    t = np.arange(round(seconds * RATE)) / RATE
    phase = rng.uniform(0, TAU)
    vibrato = .0014 * np.sin(TAU * 4.6 * t + phase) * (1 - np.exp(-t))
    signal = np.zeros(len(t))
    for harmonic, amount in ((1, 1), (2, .22), (3, .14), (4, .045), (5, .024)):
        for detune in (-.0018, .0018):
            frequency = hz(midi) * harmonic * (1 + detune + vibrato)
            signal += amount * .5 * np.sin(TAU * np.cumsum(frequency) / RATE + phase)
    signal *= .92 + .08 * np.sin(TAU * .41 * t + phase)
    return smooth_edges(signal, min(1.1, seconds * .25), min(1.8, seconds * .35))


def flute(midi, seconds, rng, tentative=False):
    t = np.arange(round(seconds * RATE)) / RATE
    wander = .0028 * np.sin(TAU * 1.1 * t + .2) if tentative else .0007 * np.sin(TAU * .8 * t)
    vibrato = .0022 * np.sin(TAU * 4.8 * t) * (1 - np.exp(-t * 2))
    # An uncertain breath settles into pitch, without a comic wrong-note gag.
    pitch = hz(midi) * (1 + wander + vibrato - (.023 if tentative else .003) * np.exp(-t * 9))
    phase = TAU * np.cumsum(pitch) / RATE
    voice = np.sin(phase) + .16 * np.sin(2 * phase) + .058 * np.sin(3 * phase)
    voice += (.14 if tentative else .055) * band_noise(len(t), rng, 650, 4800)
    if tentative:
        voice *= .8 + .2 * np.sin(TAU * 2.3 * t) ** 2
    return smooth_edges(voice, .065 if tentative else .10, .11)


def percussion(seconds, rng, pitch=130):
    t = np.arange(round(seconds * RATE)) / RATE
    voice = np.sin(TAU * (pitch * t + 2.6 * (1 - np.exp(-t * 22)))) * np.exp(-t * 18)
    voice += .08 * band_noise(len(t), rng, 300, 3700) * np.exp(-t * 34)
    return smooth_edges(voice, .004, .035)


def add(mix, voice, seconds, gain=1, pan=0, circular=True):
    start = round(seconds * RATE)
    angle = (np.clip(pan, -1, 1) + 1) * np.pi / 4
    stereo = voice[:, None] * np.array([np.cos(angle), np.sin(angle)]) * gain
    if not circular:
        end = min(len(mix), start + len(voice))
        if end > start:
            mix[start:end] += stereo[:end - start]
        return
    start %= len(mix)
    first = min(len(mix) - start, len(stereo))
    mix[start:start + first] += stereo[:first]
    if first < len(stereo):
        mix[:len(stereo) - first] += stereo[first:]


def circular_filter(signal, high=6500, low=35):
    """FFT shaping has periodic state and introduces no filter-start seam."""
    spectrum = np.fft.rfft(signal, axis=0)
    frequency = np.fft.rfftfreq(len(signal), 1 / RATE)
    response = 1 / np.sqrt(1 + (frequency / high) ** 8)
    response *= frequency ** 2 / (frequency ** 2 + low ** 2)
    spectrum *= response[:, None]
    return np.fft.irfft(spectrum, n=len(signal), axis=0)


def room(mix, rng, wet=.16, circular=True):
    reflections = np.zeros_like(mix)
    delays = np.r_[.043, .071, .113, np.linspace(.15, 1.9, 24)]
    for i, delay in enumerate(delays):
        samples = round((delay + rng.uniform(-.006, .006)) * RATE)
        source = mix[:, ::-1] if i % 2 else mix
        decay = np.exp(-delay * 2.1) * rng.uniform(.7, 1.1) / 5
        if circular:
            reflections += np.roll(source, samples, axis=0) * decay
        elif samples < len(source):
            reflections[samples:] += source[:-samples] * decay
    return mix + wet * circular_filter(reflections, high=2600, low=150)


def save(name, signal, rng, rms, peak=.40, loop=True):
    signal = circular_filter(signal, high=6500, low=35)
    signal -= signal.mean(axis=0)
    signal *= min(rms / max(np.sqrt(np.mean(signal ** 2)), 1e-9),
                  peak / max(np.max(np.abs(signal)), 1e-9))
    if not loop:
        signal = smooth_edges(signal, .01, .12)
    # Triangular dither prevents correlated low-level quantization distortion.
    dither = (rng.uniform(-.5, .5, signal.shape) + rng.uniform(-.5, .5, signal.shape)) / 32768
    pcm = np.rint((signal + dither) * 32767).astype("<i2")
    OUT.mkdir(parents=True, exist_ok=True)
    target = (MASTER_OUT if loop else OUT) / name
    target.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(target), "wb") as output:
        output.setnchannels(2)
        output.setsampwidth(2)
        output.setframerate(RATE)
        output.writeframes(pcm.tobytes())
    if loop:
        encode_master(target)
    else:
        print(f"{name:25} {len(signal) / RATE:6.2f}s  stereo PCM", flush=True)


C = (48, 55, 62, 64)
A = (45, 52, 60, 67)
F = (41, 53, 60, 64)
G = (43, 55, 62, 69)
D = (50, 57, 60, 65)
E = (40, 52, 59, 67)


@dataclass(frozen=True)
class Cue:
    name: str
    seed: int
    bpm: float
    chords: tuple
    melody: tuple
    instrument: str = "harp"
    rms: float = .067
    pad: float = .060
    arpeggio: float = .045
    reed: bool = False
    pulse: bool = False


# Each item is an original two-bar phrase. First Light retains C-D-E-G-C-A-G-C
# in its opening phrases, with answering variations rather than one exact repeat.
CUES = (
    Cue("first_light", 1047, 60, (C, A, F, G, C, A, F, G),
        ((72, 74), (76,), (67, 72), (69, 67), (72, 76), (74, 72), (69, 67), (72,)), arpeggio=.032),
    Cue("home_theme", 1051, 58, (C, F, A, G, C, E, F, G),
        ((64, 67, 72), (69, 67), (64, 67), (62, 67), (64, 72, 74), (71, 67), (69, 65), (67, 62)),
        instrument="felt", pad=.048, arpeggio=.040),
    Cue("discovery_theme", 1057, 78, (C, G, A, F, C, D, F, G),
        ((72, 74, 76, 79), (74, 71, 67), (72, 76, 74), (69, 72), (79, 76, 74), (77, 74), (76, 72, 69), (74, 71, 67)),
        pad=.030, arpeggio=.054),
    Cue("wonder_theme", 1061, 50, (A, F, C, G, A, D, F, G),
        ((72,), (69, 76), (74,), (67, 74), (76, 72), (77,), (76, 69), (74, 67)),
        rms=.061, pad=.066, arpeggio=.016, reed=True),
    Cue("festival_theme", 1063, 84, (C, F, G, C, A, F, D, G),
        ((72, 76, 79, 76), (77, 76, 72), (74, 71, 67, 71), (72, 76, 79), (81, 79, 76), (77, 76, 72), (74, 77, 76), (74, 71, 67)),
        rms=.073, pad=.032, arpeggio=.060, reed=True, pulse=True),
    Cue("rain_refuge", 1069, 55, (A, F, C, G, A, E, F, G),
        ((64, 67), (65,), (64, 62), (67,), (72, 67), (64,), (65, 64), (62,)),
        instrument="felt", rms=.050, pad=.039, arpeggio=.010),
    Cue("grief_theme", 1087, 48, (A, E, F, D, A, E, F, A),
        ((64,), (), (65, 64), (), (60, 64), (), (65,), (64, 60)),
        instrument="felt", rms=.042, pad=.035, arpeggio=0),
    Cue("remembrance_theme", 1091, 54, (C, A, F, G, A, F, D, G),
        ((72, 74), (76,), (67, 72), (69, 67), (72, 76), (72, 69), (65, 69), (67,)),
        instrument="felt", rms=.055, pad=.045, arpeggio=.022, reed=True),
)


def score(cue):
    rng = np.random.default_rng(cue.seed)
    beat = 60 / cue.bpm
    mix = np.zeros((round(64 * beat * RATE), 2))
    instrument = felt if cue.instrument == "felt" else pluck
    for phrase, chord in enumerate(cue.chords):
        start = phrase * 8 * beat
        arc = (.86, .92, .98, .90, 1.0, 1.06, .97, .83)[phrase]
        for i, midi in enumerate(chord):
            add(mix, bowed(midi, 9.2 * beat, rng), start - .6 * beat,
                cue.pad * arc / (1 + .22 * i), (-.55, .30, -.22, .54)[i])
        add(mix, felt(chord[0] - 12, 6.5 * beat, rng, .6), start + .04, .10 * arc, -.12)
        if cue.arpeggio:
            pattern = (0, 2, 1, 3, 2, 1) if cue.pulse else (0, 2, 1, 3)
            for j, index in enumerate(pattern):
                offset = (j * 7 / len(pattern) + .65) * beat
                add(mix, pluck(chord[index] + 12, 3.8 * beat, rng),
                    start + offset + rng.uniform(-.018, .018),
                    cue.arpeggio * arc * rng.uniform(.84, 1.04), -.4 + .8 * j / len(pattern))
        notes = cue.melody[phrase]
        for i, midi in enumerate(notes):
            timing = .9 + i * (5.7 / max(1, len(notes)))
            length = min(4.3, 8 - timing) * beat
            add(mix, instrument(midi, length, rng, rng.uniform(.58, .77)),
                start + timing * beat + rng.uniform(-.023, .025), .19 * arc, .16)
        if cue.reed and phrase in (2, 4, 6):
            add(mix, flute(chord[2] + 12, 2.7 * beat, rng), start + 4.5 * beat, .038 * arc, -.30)
        if cue.pulse:
            for step in (0, 3, 4, 7):
                add(mix, percussion(.4, rng, 116 if step % 4 == 0 else 170),
                    start + step * beat, .021 if step % 4 == 0 else .012, -.1)
    mix = room(mix, rng, .30 if cue.name == "wonder_theme" else .19)
    save(cue.name + ".wav", mix, rng, cue.rms)


def environment(name, seconds, seed):
    rng = np.random.default_rng(seed)
    n = round(seconds * RATE)
    t = np.arange(n) / RATE
    noise = rng.normal(size=(n, 2))
    noise = .7 * noise[:, :1] + .3 * noise
    low = circular_filter(noise, high=900, low=130)
    high = circular_filter(noise, high=4200, low=700)
    swell = .85 + .10 * np.sin(TAU * t / seconds) + .05 * np.sin(TAU * 3 * t / seconds + 1.2)
    if name == "garden_air":
        mix = (low * .65 + high * .045) * swell[:, None]
        # Small water trickles; no recognizable Earth bird calls.
        for _ in range(38):
            tt = np.arange(round(rng.uniform(.06, .20) * RATE)) / RATE
            drop = np.sin(TAU * (rng.uniform(650, 1250) * tt + 50 * tt ** 2)) * np.exp(-tt * 34)
            add(mix, smooth_edges(drop, .003, .015), rng.uniform(0, seconds), .028, rng.uniform(-.7, .7))
        rms = .011
    elif name == "rain":
        mix = (.26 * low + .28 * high) * swell[:, None]
        for _ in range(round(seconds * 24)):
            tt = np.arange(round(rng.uniform(.018, .09) * RATE)) / RATE
            drop = band_noise(len(tt), rng, 650, 6500) * np.exp(-tt * rng.uniform(55, 120))
            add(mix, smooth_edges(drop, .002, .006), rng.uniform(0, seconds), rng.uniform(.025, .11), rng.uniform(-.85, .85))
        rms = .020
    elif name == "room_air":
        mix = low * swell[:, None]
        for _ in range(26):
            tt = np.arange(round(.15 * RATE)) / RATE
            drop = np.sin(TAU * rng.uniform(800, 1200) * tt) * np.exp(-tt * 42)
            add(mix, smooth_edges(drop, .008, .02), rng.uniform(0, seconds), .028, -.35)
        rms = .007
    elif name == "workshop_air":
        mix = .7 * low * swell[:, None]
        for i in range(13):
            add(mix, percussion(.35, rng, rng.uniform(140, 260)),
                (i + .4) * seconds / 13, .11 if i % 4 else .19, rng.uniform(-.55, .55))
        rms = .010
    else:
        mix = (.7 * low + .03 * high) * swell[:, None]
        # Cloth, movement, and vessels; no fabricated spoken voices.
        for _ in range(45):
            tt = np.arange(round(.28 * RATE)) / RATE
            movement = band_noise(len(tt), rng, 160, 1600) * np.sin(np.pi * tt / .28) ** 2
            add(mix, movement, rng.uniform(0, seconds), .055, rng.uniform(-.8, .8))
        rms = .012
    save(name + ".wav", room(mix, rng, .08), rng, rms, peak=.22)


def effect(name, seed):
    rng = np.random.default_rng(seed)
    if name in ("flute_first", "flute_practice"):
        tentative = name == "flute_first"
        seconds = 8 if tentative else 12
        mix = np.zeros((seconds * RATE, 2))
        notes = ((.4, 72, .65), (2.0, 74, .43), (3.8, 76, .9), (5.3, 72, .8)) if tentative else (
            (.4, 72, 1.05), (1.6, 74, 1.05), (2.8, 76, 1.9), (4.9, 67, 1.0),
            (6.1, 72, 1.1), (7.4, 69, .7), (8.3, 67, .7), (9.2, 72, 1.5))
        for start, midi, length in notes:
            add(mix, flute(midi, length, rng, tentative), start, .6, .08, circular=False)
        mix = room(mix, rng, .12, circular=False)
        rms = .075
    elif name == "tree_creak":
        seconds = 3.4
        tt = np.arange(round(seconds * RATE)) / RATE
        phase = TAU * np.cumsum(74 + 7 * np.sin(TAU * .35 * tt)) / RATE
        voice = sum(np.sin(k * phase) / k ** 1.3 for k in range(1, 7))
        voice *= np.sin(np.pi * tt / seconds) ** 2 * (.65 + .35 * np.sin(TAU * 14 * tt) ** 2)
        voice += .12 * band_noise(len(tt), rng, 70, 1200) * np.sin(np.pi * tt / seconds) ** 2
        mix = np.column_stack((voice, voice * .82))
        rms = .032
    elif name == "water_splash":
        seconds = 2.2
        tt = np.arange(round(seconds * RATE)) / RATE
        voice = band_noise(len(tt), rng, 120, 4500) * (1 - np.exp(-tt * 30)) * np.exp(-tt * 3.5)
        mix = np.column_stack((voice, np.roll(voice, 240)))
        for _ in range(15):
            dt = np.arange(round(.14 * RATE)) / RATE
            drop = np.sin(TAU * rng.uniform(550, 1400) * dt) * np.exp(-dt * 32)
            add(mix, smooth_edges(drop, .005, .02), rng.uniform(.25, 1.4), .05, rng.uniform(-.7, .7), circular=False)
        rms = .047
    else:
        voice = percussion(.65, rng, 170)
        mix = np.column_stack((voice, voice * .92))
        rms = .042
    save(name + ".wav", mix, rng, rms, peak=.30, loop=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assets", nargs="*", help="Optional stems to rebuild; otherwise all assets.")
    parser.add_argument("--encode-existing", action="store_true", help="Encode cached WAV masters without resynthesizing.")
    args = parser.parse_args()
    ambience = [("garden_air", 32, 1103), ("rain", 32, 1109), ("room_air", 32, 1117),
                ("workshop_air", 32, 1123), ("plaza_air", 32, 1129)]
    effects = [("wood", 1151), ("flute_first", 1153), ("flute_practice", 1163),
               ("tree_creak", 1171), ("water_splash", 1181)]
    known = {cue.name for cue in CUES} | {row[0] for row in ambience + effects}
    requested = set(args.assets) or known
    unknown = requested - known
    if unknown:
        parser.error("Unknown asset(s): " + ", ".join(sorted(unknown)))
    if args.encode_existing:
        loops = {cue.name for cue in CUES} | {row[0] for row in ambience}
        for name in sorted(requested & loops):
            encode_master(MASTER_OUT / (name + ".wav"))
        return
    for cue in CUES:
        if cue.name in requested:
            score(cue)
    for name, seconds, seed in ambience:
        if name in requested:
            environment(name, seconds, seed)
    for name, seed in effects:
        if name in requested:
            effect(name, seed)


if __name__ == "__main__":
    main()
