#!/usr/bin/env python3
"""Render the authored chamber score from pinned CC0 recordings, offline.

Only instrumental score assets are written. Diegetic flute performances,
environmental recordings and the supplied closing song are outside this renderer.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from functools import lru_cache
import gc
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess

import numpy as np
from scipy.ndimage import gaussian_filter1d, minimum_filter1d

from make_audio import BANK, MASTER_OUT, OUT, RATE, add, circular_filter, encode_master, percussion, sf
from sample_audio import check_sources, edges, studio_room
from score_catalog import SCORES, compile_score

PROJECT = OUT.parents[1]
FFMPEG = PROJECT / ".cache/video-tools/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
PAN = {"piano": -.10, "harp": -.24, "flute": .16, "viola": .26, "cello": -.18, "pulse": 0}


@lru_cache(maxsize=96)
def voice(instrument, midi, frames):
    seconds = frames / RATE
    if instrument in ("viola", "cello") and seconds < 1.8:
        # Short bowed gestures must not enter the long sustain-loop splice:
        # preserve the recorded bow attack, then release within the exact length.
        data = BANK.pitched(instrument, midi)[:frames]
        if len(data) != frames:
            raise ValueError(f"Short string source is too short: {instrument}/{midi}")
        return edges(data, .035, min(.22, seconds * .22)) * .70
    return BANK.note(instrument, midi, seconds, .70)


def measure(path, ffmpeg=FFMPEG):
    result = subprocess.run([str(ffmpeg), "-hide_banner", "-nostats", "-i", str(path),
                             "-af", "ebur128=peak=true:framelog=verbose", "-f", "null", "-"],
                            capture_output=True, text=True, check=True)
    found = re.findall(r"I:\s*(-?[0-9.]+) LUFS", result.stderr)
    if not found:
        raise RuntimeError(f"No integrated loudness measurement for {path}")
    return float(found[-1])


def constrain_peaks(data, peak=.39):
    # Linked stereo, periodic lookahead/recovery: no stereo-image pumping and
    # no first/last gain-state seam. The short bow/soft piano attacks survive.
    envelope = np.max(np.abs(data), axis=1)
    gain = np.minimum(1.0, peak / np.maximum(envelope, 1e-12))
    gain = minimum_filter1d(gain, size=round(.025 * RATE) | 1, mode="wrap")
    gain = gaussian_filter1d(gain, sigma=.0025 * RATE, mode="wrap")
    data *= gain[:, None]
    return float(-20 * np.log10(max(gain.min(), 1e-9)))


def write_midi(spec, notes, path):
    """Small editable MIDI score for review, not a second runtime asset."""
    def vlq(value):
        data = [value & 127]
        while value >> 7:
            value >>= 7
            data.insert(0, 128 | (value & 127))
        return bytes(data)

    def track(events):
        body, last = bytearray(), 0
        for tick, priority, event in sorted(events):
            body.extend(vlq(tick - last)); body.extend(event); last = tick
        end = round(spec.beats * 480)
        body.extend(vlq(max(0, end - last)) + b"\xff\x2f\x00")
        return b"MTrk" + struct.pack(">I", len(body)) + body

    tempo = round(60_000_000 / spec.bpm)
    numerator, denominator = map(int, spec.time_signature.split("/"))
    tracks = [track([(0, 0, b"\xff\x51\x03" + tempo.to_bytes(3, "big")),
                     (0, 1, bytes((255, 88, 4, numerator, int(np.log2(denominator)), 24, 8)))])]
    programs = {"piano": 0, "harp": 46, "flute": 73, "viola": 41, "cello": 42, "pulse": 115}
    for channel, instrument in enumerate(PAN):
        events = [(0, 0, bytes((0xC0 | channel, programs[instrument])))]
        for note in notes:
            if note.instrument != instrument:
                continue
            onset = round(note.beat * 480)
            ending = min(round((note.beat + note.length) * 480), round(spec.beats * 480))
            events.append((onset, 2, bytes((0x90 | channel, note.midi, max(1, min(110, round(note.gain * 300)))))))
            events.append((ending, 1, bytes((0x80 | channel, note.midi, 0))))
        tracks.append(track(events))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"MThd" + struct.pack(">IHHH", 6, 1, len(tracks), 480) + b"".join(tracks))


def render(spec, ffmpeg=FFMPEG):
    seed = int.from_bytes(hashlib.sha256(spec.name.encode()).digest()[:4], "big")
    rng = np.random.default_rng(seed)
    beat = 60 / spec.bpm
    notes = compile_score(spec)
    mix = np.zeros((round(spec.duration_seconds * RATE), 2))
    print(f"Composing {spec.name}: {len(notes)} notes, {len(spec.sections)} sections, {spec.duration_seconds:.1f}s", flush=True)
    for note in notes:
        frames = max(2, round(note.length * beat * RATE))
        data = percussion(min(.36, frames / RATE), rng, 116 if note.midi == 45 else 170) if note.instrument == "pulse" else voice(note.instrument, note.midi, frames)
        # Fixed player positions; slight timing/velocity phrasing is deterministic
        # and much smaller than the notated offbeats. Downbeat bass stays anchored.
        timing = 0 if note.role == "bass" else rng.uniform(-.008, .008)
        gain = note.gain * rng.uniform(.955, 1.045)
        add(mix, data, note.beat * beat + timing, gain, PAN[note.instrument])
    voice.cache_clear()
    BANK.pitched.cache_clear()
    wet = .10 if spec.balance_group == "grief" else .15 if spec.name in ("wonder_theme", "festival_lanterns") else .115
    mix = circular_filter(studio_room(mix, wet), high=18000, low=35)
    mix -= mix.mean(axis=0)
    MASTER_OUT.mkdir(parents=True, exist_ok=True)
    temporary = MASTER_OUT / ("." + spec.name + "-meter.wav")
    master = MASTER_OUT / (spec.name + ".wav")
    reductions = []
    try:
        # Meter actual K-weighted programme loudness. Two quiet cues needn't
        # share the same RMS as a busy dance to sound appropriately balanced.
        sf.write(temporary, mix, RATE, subtype="FLOAT")
        initial = measure(temporary, ffmpeg)
        mix *= 10 ** ((spec.target_lufs - initial) / 20)
        for _ in range(2):
            reductions.append(constrain_peaks(mix))
            mix -= mix.mean(axis=0)
            sf.write(temporary, mix, RATE, subtype="PCM_24")
            measured = measure(temporary, ffmpeg)
            correction = spec.target_lufs - measured
            if abs(correction) <= .2:
                break
            mix *= 10 ** (correction / 20)
        reductions.append(constrain_peaks(mix))
        mix -= mix.mean(axis=0)
        sf.write(master, mix, RATE, subtype="PCM_24")
    finally:
        temporary.unlink(missing_ok=True)
    del mix
    gc.collect()
    encode_master(master)
    delivered = measure(OUT / (spec.name + ".ogg"), ffmpeg)
    if abs(delivered - spec.target_lufs) > 1.0:
        raise RuntimeError(f"{spec.name}: {delivered} LUFS versus intended {spec.target_lufs}")
    record = dict(name=spec.name, duration_seconds=spec.duration_seconds,
                  target_lufs=spec.target_lufs, measured_lufs=delivered,
                  maximum_limiter_reduction_db=round(max(reductions), 3),
                  notes=len(notes), sha256=hashlib.sha256((OUT / (spec.name + ".ogg")).read_bytes()).hexdigest())
    evidence = PROJECT / ".cache/score-render" / (spec.name + ".json")
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(json.dumps(record, indent=2) + "\n")
    write_midi(spec, notes, PROJECT / ".cache/score-midi" / (spec.name + ".mid"))
    print(f"  {delivered:.1f} LUFS; peak control {max(reductions):.1f} dB", flush=True)
    return record


def catalog():
    rows = []
    for score in SCORES.values():
        notes = compile_score(score)
        row = {key: value for key, value in asdict(score).items() if key != "sections"}
        row.update(duration_seconds=round(score.duration_seconds, 3),
                   file="game/audio/" + score.name + ".ogg", notes=len(notes),
                   instruments=sorted({note.instrument for note in notes}),
                   sections=[dict(name=s.name, bars=len(s.bars), lead=s.lead, texture=s.texture)
                             for s in score.sections])
        rows.append(row)
    return dict(method="Authored phrases and instrumental arrangements; musical intent is subject to contextual listening.",
                core_compositions=sum(s.parent is None for s in SCORES.values()),
                variations=sum(s.parent is not None for s in SCORES.values()),
                total_minutes=round(sum(s.duration_seconds for s in SCORES.values()) / 60, 2), cues=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cues", nargs="*", help="Cue stems; default renders the complete instrumental score.")
    parser.add_argument("--ffmpeg", type=Path, default=FFMPEG)
    parser.add_argument("--catalog-only", action="store_true")
    args = parser.parse_args()
    unknown = set(args.cues) - SCORES.keys()
    if unknown:
        parser.error("Unknown cue(s): " + ", ".join(sorted(unknown)))
    (PROJECT / "docs/score-catalog.json").write_text(json.dumps(catalog(), indent=2) + "\n")
    if args.catalog_only:
        return
    check_sources()
    for name in args.cues or SCORES:
        render(SCORES[name], args.ffmpeg)


if __name__ == "__main__":
    main()
