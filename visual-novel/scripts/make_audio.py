#!/usr/bin/env python3
"""Render the original Book I score with CC0 instruments and field recordings.

The deliberately hesitant flute cues use 24 kHz synthesis.
Other assets use 48 kHz rendering. See docs/AUDIO_DIRECTION.md for provenance.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import sys
import wave
import numpy as np
from scipy.ndimage import gaussian_filter1d, minimum_filter1d
from scipy.signal import butter, sosfilt

RATE = 48000
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
from sample_audio import SampleBank, check_sources, fetch_sources, field_ambience, field_effect, studio_room

BANK = SampleBank()


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
    temporary = target.with_suffix(".tmp.ogg")
    # libsndfile's Vorbis writer can crash on a single large 48 kHz write.
    # Bounded blocks also keep codec memory predictable. Publish only on success.
    with sf.SoundFile(temporary, "w", samplerate=rate, channels=2,
                      format="OGG", subtype="VORBIS",
                      compression_level=VORBIS_COMPRESSION) as output:
        for start in range(0, len(data), 8192):
            output.write(data[start:start + 8192])
    canonicalize_ogg(temporary)
    temporary.replace(target)
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
    if voice.ndim == 1:
        stereo = voice[:, None] * np.array([np.cos(angle), np.sin(angle)]) * gain
    else:
        # Preserve the original recording's stereo field while positioning it.
        stereo = voice * np.array([np.cos(angle), np.sin(angle)]) * gain
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
    legacy_flute = name in ("flute_first.wav", "flute_attempt.wav")
    signal = circular_filter(signal, high=6500 if legacy_flute else 18000, low=35)
    signal -= signal.mean(axis=0)
    if legacy_flute:
        signal *= min(rms / max(np.sqrt(np.mean(signal ** 2)), 1e-9),
                      peak / max(np.max(np.abs(signal)), 1e-9))
    else:
        signal *= rms / max(np.sqrt(np.mean(signal ** 2)), 1e-9)
        # A few recorded attacks should not force the whole cue to be inaudible.
        # Linked stereo gain, short lookahead, and smooth recovery tame peaks;
        # cap reduction at 6 dB to retain the acoustic instruments' dynamics.
        envelope = np.max(np.abs(signal), axis=1)
        gain = np.clip(peak / np.maximum(envelope, peak), .5, 1)
        gain = minimum_filter1d(gain, size=round(.035 * RATE) | 1)
        gain = gaussian_filter1d(gain, sigma=.004 * RATE)
        signal *= gain[:, None]
        signal *= min(1, peak / max(np.max(np.abs(signal)), 1e-9))
        signal -= signal.mean(axis=0)
    if not loop:
        signal = smooth_edges(signal, .01, .12)
    target = (MASTER_OUT if loop else OUT) / name
    target.parent.mkdir(parents=True, exist_ok=True)
    if loop:
        # Keep high-resolution masters; delivery remains compact Ogg Vorbis.
        sf.write(target, signal, RATE, subtype="PCM_24")
        encode_master(target)
        return
    # Triangular dither prevents correlated low-level quantization distortion.
    dither = (rng.uniform(-.5, .5, signal.shape) + rng.uniform(-.5, .5, signal.shape)) / 32768
    pcm = np.rint((signal + dither) * 32767).astype("<i2")
    OUT.mkdir(parents=True, exist_ok=True)
    with wave.open(str(target), "wb") as output:
        output.setnchannels(2)
        output.setsampwidth(2)
        output.setframerate(RATE)
        output.writeframes(pcm.tobytes())
    print(f"{name:25} {len(signal) / RATE:6.2f}s  stereo PCM", flush=True)


# The full authored score has its own notation and arranger. Keep this entry
# point for existing build instructions and environmental/effect generation.
from score_catalog import SCORES
CUES = tuple(SCORES.values())


def score(cue):
    from compose_score import render
    render(cue)


def environment(name, seconds, seed):
    rng = np.random.default_rng(seed)
    mix = field_ambience(name, seconds)
    levels = {"garden_air": .011, "rain": .027, "room_air": .007,
              "workshop_air": .010, "plaza_air": .008}
    save(name + ".wav", mix, rng, levels[name], peak=.22)


def effect(name, seed):
    rng = np.random.default_rng(seed)
    if name == "flute_attempt":
        mix = np.zeros((round(1.6 * RATE), 2))
        # One breath briefly catches a C, then thins into air and gives out.
        voice = flute(72, .75, rng, tentative=True)
        t = np.arange(len(voice)) / RATE
        voice *= .08 + .92 * np.exp(-((t - .20) / .13) ** 2)
        voice += .18 * smooth_edges(band_noise(len(t), rng, 700, 4200), .05, .22)
        add(mix, voice, .15, .6, .08, circular=False)
        save(name + ".wav", room(mix, rng, .10, circular=False), rng, .055, peak=.25, loop=False)
        return
    if name not in ("flute_first", "flute_practice"):
        save(name + ".wav", field_effect(name), rng,
             {"wood": .042, "tree_creak": .032, "water_splash": .047}[name], peak=.30, loop=False)
        return
    if name in ("flute_first", "flute_practice"):
        tentative = name == "flute_first"
        seconds = 8 if tentative else 12
        mix = np.zeros((seconds * RATE, 2))
        notes = ((.4, 72, .65), (2.0, 74, .43), (3.8, 76, .9), (5.3, 72, .8)) if tentative else (
            (.4, 72, 1.05), (1.6, 74, 1.05), (2.8, 76, 1.9), (4.9, 67, 1.0),
            (6.1, 72, 1.1), (7.4, 69, .7), (8.3, 67, .7), (9.2, 72, 1.5))
        for start, midi, length in notes:
            voice = flute(midi, length, rng, True) if tentative else BANK.note("flute", midi, length, .65)
            add(mix, voice, start, .6, .08, circular=False)
        mix = room(mix, rng, .12, circular=False) if tentative else studio_room(mix, .10, circular=False)
        rms = .075
    save(name + ".wav", mix, rng, rms, peak=.30, loop=False)


def main():
    global RATE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assets", nargs="*", help="Optional stems to rebuild; otherwise all assets.")
    parser.add_argument("--encode-existing", action="store_true", help="Encode cached WAV masters without resynthesizing.")
    parser.add_argument("--fetch-sources", action="store_true", help="Download and verify pinned CC0 source recordings, then exit.")
    args = parser.parse_args()
    if args.fetch_sources:
        fetch_sources()
        return
    ambience = [("garden_air", 32, 1103), ("rain", 32, 1109), ("room_air", 32, 1117),
                ("workshop_air", 32, 1123), ("plaza_air", 32, 1129)]
    effects = [("wood", 1151), ("flute_attempt", 1187), ("flute_first", 1153), ("flute_practice", 1163),
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
    if requested - {"flute_first", "flute_attempt"}:
        check_sources()
    for cue in CUES:
        if cue.name in requested:
            score(cue)
    for name, seconds, seed in ambience:
        if name in requested:
            environment(name, seconds, seed)
    for name, seed in effects:
        if name in requested:
            RATE = 24000 if name in ("flute_first", "flute_attempt") else 48000
            try:
                effect(name, seed)
            finally:
                RATE = 48000


if __name__ == "__main__":
    main()
