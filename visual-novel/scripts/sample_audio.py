"""Offline CC0 sample playback and field-recording preparation.

The game ships rendered audio only. Sources are pinned by SHA-256 in
docs/audio-sources.json; downloads and extracted material stay in .cache.
"""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.request
import zipfile

import numpy as np
from scipy.signal import butter, fftconvolve, resample_poly, sosfilt

PROJECT = Path(__file__).resolve().parents[1]
CACHE = PROJECT / ".cache/audio-sources"
MANIFEST = PROJECT / "docs/audio-sources.json"
sys.path.append(str(PROJECT / ".cache/audio-tools"))
import soundfile as sf

RATE = 48000


def source_rows():
    return json.loads(MANIFEST.read_text())["sources"]


def check_sources(extracted=True):
    for row in source_rows():
        path = CACHE / row["path"]
        if not path.is_file():
            raise SystemExit("CC0 sources missing. Run: python3 scripts/make_audio.py --fetch-sources")
        if row["license"] != "CC0-1.0" or hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            raise SystemExit(f"Audio source/license mismatch: {path}")
    if extracted:
        for row in json.loads(MANIFEST.read_text())["extracted_members"]:
            path = CACHE / row["path"]
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
                raise SystemExit("Extracted audio changed or missing. Run: python3 scripts/make_audio.py --fetch-sources")


def extract_sources():
    with zipfile.ZipFile(CACHE / "recordings/Rain OGG.zip") as archive:
        for name in ("1.ogg", "2.ogg", "3.ogg", "4.ogg"):
            destination = CACHE / "rain" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(archive.read(name))
    extractor = shutil.which("7z") or shutil.which("7zz")
    if not extractor:
        raise SystemExit("Extracting the CC0 water samples requires 7z or 7zz.")
    # Only the six known audio members are extracted, never arbitrary paths.
    for index in range(1, 7):
        member = f"ezwa-water_splash/water_splash-{index:02d}.flac"
        destination = CACHE / "splash" / member
        destination.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run([extractor, "x", "-so", str(CACHE / "recordings/ezwa-water_splash.7z"), member],
                                check=True, capture_output=True)
        destination.write_bytes(result.stdout)


def fetch_sources():
    for row in source_rows():
        path = CACHE / row["path"]
        if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]:
            continue
        print("Download:", row["id"], flush=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".part")
        with urllib.request.urlopen(row["url"], timeout=60) as response, temporary.open("wb") as out:
            shutil.copyfileobj(response, out)
        if hashlib.sha256(temporary.read_bytes()).hexdigest() != row["sha256"]:
            temporary.unlink()
            raise SystemExit(f"Changed upstream source: {row['id']}")
        temporary.replace(path)
    check_sources(extracted=False)
    extract_sources()
    check_sources()


@lru_cache(maxsize=90)
def read_source(path):
    data, rate = sf.read(CACHE / path, dtype="float64", always_2d=True)
    if rate != RATE:
        ratio = Fraction(RATE, rate)
        data = resample_poly(data, ratio.numerator, ratio.denominator, axis=0)
    if data.shape[1] == 1:
        data = np.repeat(data, 2, axis=1)
    data = data[:, :2]
    data -= data.mean(axis=0)
    return data


def edges(data, attack=.01, release=.1):
    result = data.copy()
    for seconds, front in ((attack, True), (release, False)):
        count = min(len(result), max(2, round(seconds * RATE)))
        ramp = np.sin(np.linspace(0, np.pi / 2, count)) ** 2
        if front:
            result[:count] *= ramp[:, None]
        else:
            result[-count:] *= ramp[::-1, None]
    return result


def level(data, rms):
    return data * (rms / max(np.sqrt(np.mean(data ** 2)), 1e-9))


def lowpass(data, frequency):
    return sosfilt(butter(2, frequency, fs=RATE, output="sos"), data, axis=0)


def loop_recording(data, frames, overlap=.75):
    """Overlap a recording's ends, then extend its periodic section as needed."""
    count = min(round(overlap * RATE), len(data) // 4)
    ramp = (0.5 - .5 * np.cos(np.linspace(0, np.pi, count)))[:, None]
    cross = data[-count:] * (1 - ramp) + data[:count] * ramp
    periodic = np.concatenate((cross, data[count:-count]))
    # Make the requested period itself seamless even when not an integer
    # multiple of the source length. No fade to silence at either boundary.
    extended = np.tile(periodic, (int(np.ceil((frames + count) / len(periodic))), 1))[:frames + count]
    cross = extended[frames:] * (1 - ramp) + extended[:count] * ramp
    return np.concatenate((cross, extended[count:frames]))


class SampleBank:
    def __init__(self):
        self.instruments = {}
        for row in source_rows():
            kind = row["kind"]
            if kind not in ("harp", "piano", "cello", "viola", "flute"):
                continue
            note = re.search(r"_([A-G])([#b]?)(\d)_", row["id"])
            if not note:
                raise ValueError(f"Unmapped sample pitch: {row['id']}")
            letter, accidental, octave = note.groups()
            midi = 12 * (int(octave) + 1) + dict(C=0, D=2, E=4, F=5, G=7, A=9, B=11)[letter]
            midi += {"": 0, "#": 1, "b": -1}[accidental]
            # VSCO's ensemble/woodwind names use C3=middle C; harp/piano C4.
            if kind in ("cello", "viola", "flute"):
                midi += 12
            self.instruments.setdefault(kind, []).append((midi, row["path"]))

    @lru_cache(maxsize=160)
    def pitched(self, instrument, midi):
        root, path = min(self.instruments[instrument], key=lambda item: abs(item[0] - midi))
        source = read_source(path)
        ratio = Fraction(2 ** ((root - midi) / 12)).limit_denominator(800)
        if root != midi:
            source = resample_poly(source, ratio.numerator, ratio.denominator, axis=0)
        # Match reference levels before applying performance velocity, retaining
        # each soft sample's recorded attack and decay.
        reference = source[:min(len(source), RATE * 3)]
        gain = min(.17 / max(np.sqrt(np.mean(reference ** 2)), 1e-6), 8)
        return source * gain

    def note(self, instrument, midi, seconds, velocity=.7):
        data = self.pitched(instrument, midi)
        count = round(seconds * RATE)
        if instrument in ("cello", "viola"):
            # The middle of a long recorded bow contains the sustained tone.
            # Keep its attack, and join the sustain with a gentle crossfade.
            attack = data[:min(round(1.5 * RATE), count)]
            sustain = data[round(1.2 * RATE):round(min(len(data) / RATE - 1.8, 5.2) * RATE)]
            cross = min(round(.3 * RATE), len(attack) // 2)
            tail = loop_recording(sustain, count - len(attack) + cross, .35)
            ramp = (.5 - .5 * np.cos(np.linspace(0, np.pi, cross)))[:, None]
            joint = attack[-cross:] * (1 - ramp) + tail[:cross] * ramp
            result = np.concatenate((attack[:-cross], joint, tail[cross:]))
            result = edges(result, .55, min(1.2, seconds * .22))
        else:
            result = np.zeros((count, 2))
            take = min(count, len(data))
            result[:take] = data[:take]
            result = edges(result, .004 if instrument in ("piano", "harp") else .065,
                           min(.4, seconds * .2))
        return result * velocity


@lru_cache(maxsize=4)
def room_impulse(seconds=1.3):
    """Dense, frequency-damped stereo decay; generated here, no external IR."""
    rng = np.random.default_rng(2147)
    time = np.arange(round(seconds * RATE)) / RATE
    impulse = rng.normal(size=(len(time), 2)) * np.exp(-time[:, None] * (6.9 / seconds))
    impulse = lowpass(impulse, 5200)
    impulse[:round(.022 * RATE)] = 0
    impulse /= np.sqrt(np.sum(impulse ** 2, axis=0))
    return impulse


def studio_room(data, wet=.13, circular=True):
    impulse = room_impulse()
    reflections = np.column_stack([fftconvolve(data[:, ch], impulse[:, ch]) for ch in range(2)])
    output = reflections[:len(data)].copy()
    if circular:
        output[:len(reflections) - len(data)] += reflections[len(data):]
    return data + wet * output


def field_ambience(name, seconds):
    frames = round(seconds * RATE)
    if name == "rain":
        rain = read_source("rain/3.ogg")
        return level(loop_recording(rain, frames, 1.2), .027)
    water = level(loop_recording(read_source("recordings/atmosbasement.mp3_.flac"), frames, .8), .009)
    # Soft original air stays beneath the recorded physical details.
    rng = np.random.default_rng({"garden_air": 1103, "room_air": 1117, "workshop_air": 1123, "plaza_air": 1129}[name])
    air = lowpass(rng.normal(size=(frames, 2)), 1300)
    air = level(loop_recording(air, frames), .0025)
    if name == "garden_air":
        return water + air
    if name == "room_air":
        return lowpass(water, 2600) * .48 + air * .65
    mix = air * .8 + lowpass(water, 1800) * .12
    # Real, quiet wooden contacts give workshop/gathering spaces irregular life.
    for start in rng.uniform(0, seconds, 9 if name == "workshop_air" else 5):
        sound = wood_contact()
        sound = level(sound, .009 if name == "workshop_air" else .004)
        index = round(start * RATE)
        indexes = (np.arange(len(sound)) + index) % frames
        mix[indexes] += sound * rng.uniform(.6, 1.0)
    return mix


def wood_contact():
    source = read_source("recordings/tree_creak.flac")
    # A brief contact from the opening; do not pitch it into a musical hit.
    return edges(source[round(.4 * RATE):round(1.15 * RATE)], .012, .16)


def field_effect(name):
    if name == "wood":
        data = wood_contact()
    elif name == "tree_creak":
        data = edges(read_source("recordings/tree_creak.flac"), .08, .6)
    else:
        data = edges(read_source("splash/ezwa-water_splash/water_splash-02.flac"), .006, .15)
    # A small pan/reverb makes mono foley spatial without fake source stereo.
    data = data * np.array([.95, .82])
    return studio_room(data, wet=.07, circular=False)
