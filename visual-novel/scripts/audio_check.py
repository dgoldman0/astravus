#!/usr/bin/env python3
"""Decode runtime Ogg/WAV and check measurable audio properties.

These checks catch clipping, DC, empty/broken assets, mono rendering mistakes,
missing cues, and anomalous loop seams. They do not certify musical quality or
replace listening in the game. Requires NumPy and SciPy.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from scipy.signal import resample_poly, welch
from make_audio import MASTER_OUT, VORBIS_COMPRESSION, sf

PROJECT = Path(__file__).resolve().parents[1]
MUSIC = {"first_light", "home_theme", "discovery_theme", "wonder_theme", "festival_theme",
         "rain_refuge", "grief_theme", "remembrance_theme"}
AMBIENCE = {"garden_air", "rain", "room_air", "workshop_air", "plaza_air"}
EFFECTS = {"wood", "flute_first", "flute_practice", "tree_creak", "water_splash"}


def db(value):
    return float(20 * np.log10(max(float(value), 1e-12)))


def analyze(path):
    info = sf.info(path)
    signal, rate = sf.read(path, dtype="float64", always_2d=True)
    channels, frames = signal.shape[1], len(signal)
    errors = []
    expected_subtype = "VORBIS" if path.suffix == ".ogg" else "PCM_16"
    if info.subtype != expected_subtype:
        errors.append(f"Expected {expected_subtype}, got {info.subtype}")
    if rate != 24000 or channels != 2:
        errors.append("Expected 24 kHz stereo")
    peak = np.max(np.abs(signal))
    rms = np.sqrt(np.mean(signal ** 2))
    dc = np.max(np.abs(signal.mean(axis=0)))
    if peak > .45:
        errors.append("Decoded peak exceeds -6.94 dBFS ceiling")
    if np.any(np.abs(signal) >= 1):
        errors.append("Clipped decoded sample")
    if dc > 3e-5:
        errors.append("DC offset exceeds -90 dBFS")
    if rms < .001:
        errors.append("Unexpectedly silent asset")
    if np.array_equal(signal[:, 0], signal[:, 1]):
        errors.append("Identical left/right channels")
    seconds = frames / rate
    if path.stem in MUSIC and not 45 <= seconds <= 90:
        errors.append("Music duration outside 45–90 seconds")
    oversampled = resample_poly(signal, 4, 1, axis=0)
    true_peak = np.max(np.abs(oversampled))
    if true_peak > .45:
        errors.append("Reconstructed peak exceeds available headroom")
    del oversampled
    derivatives = np.abs(np.diff(signal, axis=0))
    typical_step = np.quantile(derivatives, .99, axis=0)
    seam = np.abs(signal[0] - signal[-1])
    loop = path.stem in MUSIC | AMBIENCE
    if loop and np.any(seam > np.maximum(5e-4, typical_step * 4)):
        errors.append("Loop boundary is anomalous relative to ordinary sample steps")
    window = round(rate * .5)
    windows = signal[:len(signal) // window * window].reshape(-1, window, channels)
    rms_windows = np.sqrt(np.mean(windows ** 2, axis=(1, 2)))
    frequency, density = welch(signal.mean(axis=1), fs=rate, nperseg=8192)
    total = np.sum(density)
    bands = {}
    for name, low, high in (("20–180 Hz", 20, 180), ("180–2000 Hz", 180, 2000),
                            ("2000–6000 Hz", 2000, 6000), ("6000–12000 Hz", 6000, 12001)):
        bands[name] = round(float(100 * np.sum(density[(frequency >= low) & (frequency < high)]) / total), 2)
    master_comparison = None
    master_path = MASTER_OUT / (path.stem + ".wav")
    if path.suffix == ".ogg" and master_path.exists():
        reference, reference_rate = sf.read(master_path, dtype="float64", always_2d=True)
        if reference_rate != rate or reference.shape != signal.shape:
            errors.append("Decoded duration/channels differ from the WAV master")
        else:
            reference_rms = np.sqrt(np.mean(reference ** 2))
            residual = np.sqrt(np.mean((reference - signal) ** 2))
            master_comparison = {
                "sha256": hashlib.sha256(master_path.read_bytes()).hexdigest(),
                "frame_count_matches": True,
                "rms_change_db": round(db(rms / reference_rms), 3),
                "signal_to_error_db": round(db(reference_rms / max(residual, 1e-12)), 2),
            }
            if abs(master_comparison["rms_change_db"]) > .5:
                errors.append("Codec altered average level by more than 0.5 dB")
    return {
        "file": str(path.relative_to(PROJECT)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "duration_seconds": round(seconds, 3), "sample_rate": rate,
        "channels": channels, "format": info.format, "subtype": info.subtype,
        "bits_per_sample": 16 if info.subtype == "PCM_16" else None,
        "bytes": path.stat().st_size, "loop": loop,
        "peak_dbfs": round(db(peak), 2), "true_peak_4x_dbfs": round(db(true_peak), 2),
        "rms_dbfs": round(db(rms), 2), "dc_dbfs": round(db(dc), 2),
        "crest_factor_db": round(db(peak / rms), 2),
        "stereo_correlation": round(float(np.corrcoef(signal.T)[0, 1]), 4),
        "half_second_rms_range_dbfs": [round(db(rms_windows.min()), 2), round(db(rms_windows.max()), 2)],
        "loop_step_dbfs": round(db(seam.max()), 2) if loop else None,
        "loop_step_vs_p99": round(float(np.max(seam / np.maximum(typical_step, 1e-9))), 3) if loop else None,
        "spectral_centroid_hz": round(float(np.sum(frequency * density) / total), 1),
        "spectral_energy_percent": bands,
        "master_comparison": master_comparison,
        "errors": errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=PROJECT / "test-results" / "audio-report.json")
    args = parser.parse_args()
    rows = []
    missing = []
    for name in sorted(MUSIC | AMBIENCE | EFFECTS):
        path = PROJECT / "game" / "audio" / (name + (".ogg" if name in MUSIC | AMBIENCE else ".wav"))
        if not path.exists():
            missing.append(str(path.relative_to(PROJECT)))
            continue
        row = analyze(path)
        rows.append(row)
        state = "PASS" if not row["errors"] else "FAIL"
        print(f"{state} {name:22} {row['duration_seconds']:6.2f}s  peak {row['peak_dbfs']:6.2f}  RMS {row['rms_dbfs']:6.2f} dBFS")
        for error in row["errors"]:
            print(f"     {error}")
    report = {"method": "Decoded runtime audio, 4x reconstruction, periodic seam comparison, Welch spectrum; no subjective listening claim",
              "encoder": {"soundfile": sf.__version__, "libsndfile": sf.__libsndfile_version__,
                          "vorbis_compression_level": VORBIS_COMPRESSION, "sample_rate": 24000},
              "renderer": "scripts/make_audio.py", "missing": missing, "assets": rows}
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Report: {args.json}")
    return 1 if missing or any(row["errors"] for row in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
