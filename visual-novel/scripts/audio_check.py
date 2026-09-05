#!/usr/bin/env python3
"""Decode runtime Ogg/WAV and check measurable audio properties.

These checks catch clipping, DC, empty/broken assets, mono rendering mistakes,
missing cues, anomalous loop seams, and relative playback loudness. They do not
certify musical quality or replace listening in the game. Requires NumPy,
SciPy, and FFmpeg (the closing-theme renderer's cached copy is supported).
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import numpy as np
from scipy.signal import resample_poly, welch
from make_audio import MASTER_OUT, VORBIS_COMPRESSION, sf

PROJECT = Path(__file__).resolve().parents[1]
MUSIC = {"first_light", "home_theme", "discovery_theme", "wonder_theme", "festival_theme",
         "rain_refuge", "grief_theme", "remembrance_theme"}
AMBIENCE = {"garden_air", "rain", "room_air", "workshop_air", "plaza_air"}
EFFECTS = {"wood", "flute_attempt", "flute_first", "flute_practice", "tree_creak", "water_splash"}
SONGS = {"curiosity_and_discovery"}


def playback_uses():
    """Read the actual script gains instead of duplicating mix values here."""
    options = (PROJECT / "game/options.rpy").read_text()
    defaults = {
        channel: float(re.search(r"define config.default_" + setting + r"_volume\s*=\s*([.\d]+)", options).group(1))
        for channel, setting in (("music", "music"), ("sound", "sfx"), ("ambience", "sfx"))
    }
    uses = {}
    for path in sorted((PROJECT / "game").glob("*.rpy")):
        scene = None
        for number, line in enumerate(path.read_text().splitlines(), 1):
            entered = re.search(r'enter_scene\("([^"]+)"\)', line)
            if entered:
                scene = entered.group(1)
            cue = re.match(r'\s*play (music|sound|ambience) "(audio/[^"\n]+)"(.*)', line)
            if not cue:
                continue
            channel, filename, clauses = cue.groups()
            gain = re.search(r"\bvolume\s+([.\d]+)", clauses)
            relative = float(gain.group(1)) if gain else 1.0
            uses.setdefault(Path(filename).stem, []).append({
                "source": f"{path.relative_to(PROJECT)}:{number}", "scene": scene,
                "channel": channel, "relative_amplitude": relative,
                "default_mixer_amplitude": defaults[channel],
            })
    theme = json.loads((PROJECT / "game/closing_theme.json").read_text())
    uses.setdefault(Path(theme["audio"]).stem, []).append({
        "source": "game/closing_theme.json", "scene": "closing_theme", "channel": "closing_theme",
        "relative_amplitude": 10 ** (theme["runtime_gain_db"] / 20),
        "default_mixer_amplitude": defaults["music"],
    })
    return uses


def loudness(path, ffmpeg):
    result = subprocess.run([
        str(ffmpeg), "-hide_banner", "-nostats", "-i", str(path),
        "-af", "ebur128=peak=true:framelog=verbose", "-f", "null", "-",
    ], check=True, capture_output=True, text=True)
    summary = result.stderr.rsplit("Summary:", 1)[-1]
    return {
        "integrated_lufs": float(re.search(r"I:\s+(-?[\d.]+) LUFS", summary).group(1)),
        "loudness_range_lu": float(re.search(r"LRA:\s+(-?[\d.]+) LU", summary).group(1)),
        "true_peak_dbtp": float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", summary).group(1)),
    }


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
    expected_rate = 24000 if path.stem in ("flute_first", "flute_attempt") else 48000
    if rate != expected_rate or channels != 2:
        errors.append(f"Expected {expected_rate} Hz stereo")
    if path.stem == "flute_first":
        preserved = json.loads((PROJECT / "docs/audio-sources.json").read_text())["preserved_first_flute_sha256"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != preserved:
            errors.append("The deliberately rough first flute performance was changed")
    peak = np.max(np.abs(signal))
    rms = np.sqrt(np.mean(signal ** 2))
    dc = np.max(np.abs(signal.mean(axis=0)))
    # The supplied song has its own mastering. Its game balance is controlled
    # at playback, while the unchanged standalone song keeps its headroom.
    supplied_song = path.stem in SONGS
    ceiling = 10 ** (-1 / 20) if supplied_song else .45
    dc_ceiling = .001 if supplied_song else 3e-5
    if peak > ceiling:
        errors.append(f"Decoded peak exceeds {db(ceiling):.2f} dBFS ceiling")
    if np.any(np.abs(signal) >= 1):
        errors.append("Clipped decoded sample")
    if dc > dc_ceiling:
        errors.append(f"DC offset exceeds {db(dc_ceiling):.1f} dBFS")
    if rms < .001:
        errors.append("Unexpectedly silent asset")
    if np.array_equal(signal[:, 0], signal[:, 1]):
        errors.append("Identical left/right channels")
    seconds = frames / rate
    if path.stem == "flute_attempt" and not .9 <= seconds <= 2:
        errors.append("The first broken breath must be a short single attempt")
    if path.stem in MUSIC and not 45 <= seconds <= 90:
        errors.append("Music duration outside 45–90 seconds")
    if supplied_song:
        metadata = json.loads((PROJECT / "docs/closing-theme-audio.json").read_text())
        if hashlib.sha256(path.read_bytes()).hexdigest() != metadata["output"]["sha256"]:
            errors.append("Supplied song encoding differs from its recorded provenance")
        if frames != metadata["source"]["frames"]:
            errors.append("Supplied song does not retain its complete source duration")
    oversampled = resample_poly(signal, 4, 1, axis=0)
    true_peak = np.max(np.abs(oversampled))
    if true_peak > ceiling:
        errors.append("Reconstructed peak exceeds available headroom")
    del oversampled
    derivatives = np.abs(np.diff(signal, axis=0))
    typical_step = np.quantile(derivatives, .99, axis=0)
    seam = np.abs(signal[0] - signal[-1])
    loop = path.stem in MUSIC | AMBIENCE
    if loop and np.any(seam > np.maximum(5e-4, typical_step * 4)):
        errors.append("Loop boundary is anomalous relative to ordinary sample steps")
    window = min(frames, round(rate * .5))
    windows = signal[:len(signal) // window * window].reshape(-1, window, channels)
    rms_windows = np.sqrt(np.mean(windows ** 2, axis=(1, 2)))
    frequency, density = welch(signal.mean(axis=1), fs=rate, nperseg=8192)
    total = np.sum(density)
    bands = {}
    for name, low, high in (("20–180 Hz", 20, 180), ("180–2000 Hz", 180, 2000),
                            ("2000–6000 Hz", 2000, 6000), ("6000–12000 Hz", 6000, 12000),
                            ("12000–24000 Hz", 12000, 24001)):
        bands[name] = round(float(100 * np.sum(density[(frequency >= low) & (frequency < high)]) / total), 2)
    master_comparison = None
    master_path = MASTER_OUT / (path.stem + ".wav")
    if supplied_song:
        master_path = PROJECT.parents[1] / metadata["source"]["file"]
        if master_path.exists() and hashlib.sha256(master_path.read_bytes()).hexdigest() != metadata["source"]["sha256"]:
            errors.append("Supplied source WAV differs from its recorded provenance")
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


def balance_checks(rows):
    """Compare related cues; room tone and dramatic silence are not targets."""
    by_name = {Path(row["file"]).stem: row for row in rows if row["playback_uses"]}
    checks = []

    def level(name):
        return by_name[name]["playback_uses"][0]["lufs_before_user_mixer"]

    if SONGS | {"home_theme"} <= by_name.keys():
        difference = abs(level("curiosity_and_discovery") - level("home_theme"))
        checks.append({"check": "Closing song versus the preceding home theme", "difference_lu": round(difference, 2), "limit_lu": 1.5, "pass": difference <= 1.5})
    if {"flute_attempt", "flute_first", "flute_practice"} <= by_name.keys():
        difference = abs(level("flute_first") - level("flute_practice"))
        checks.append({"check": "Hesitant phrase versus later practice", "difference_lu": round(difference, 2), "limit_lu": 1.5, "pass": difference <= 1.5})
        difference = level("flute_first") - level("flute_attempt")
        checks.append({"check": "Single broken breath remains quieter than a phrase", "difference_lu": round(difference, 2), "minimum_lu": 1, "pass": difference >= 1})
    ordinary_music = MUSIC - {"grief_theme", "rain_refuge"}
    if ordinary_music <= by_name.keys():
        levels = [level(name) for name in ordinary_music]
        spread = max(levels) - min(levels)
        checks.append({"check": "Ordinary score cue spread; quieter grief/rain cues retain their dynamics", "spread_lu": round(spread, 2), "limit_lu": 3, "pass": spread <= 3})
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=PROJECT / "test-results" / "audio-report.json")
    cached_ffmpeg = PROJECT / ".cache/video-tools/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
    parser.add_argument("--ffmpeg", type=Path, default=cached_ffmpeg if cached_ffmpeg.exists() else shutil.which("ffmpeg"))
    args = parser.parse_args()
    if not args.ffmpeg:
        parser.error("FFmpeg is required; pass --ffmpeg or install the closing-theme renderer's tools")
    rows = []
    missing = []
    uses = playback_uses()
    for name in sorted(MUSIC | AMBIENCE | EFFECTS | SONGS):
        path = PROJECT / "game" / "audio" / (name + (".ogg" if name in MUSIC | AMBIENCE | SONGS else ".wav"))
        if not path.exists():
            missing.append(str(path.relative_to(PROJECT)))
            continue
        row = analyze(path)
        row["loudness"] = loudness(path, args.ffmpeg)
        row["playback_uses"] = uses.get(name, [])
        if not row["playback_uses"]:
            row["errors"].append("Delivered cue has no audited playback use")
        for use in row["playback_uses"]:
            relative_db = db(use["relative_amplitude"])
            use["relative_gain_db"] = round(relative_db, 3)
            use["lufs_before_user_mixer"] = round(row["loudness"]["integrated_lufs"] + relative_db, 2)
            use["estimated_default_lufs"] = round(row["loudness"]["integrated_lufs"] + relative_db + db(use["default_mixer_amplitude"]), 2)
        rows.append(row)
        state = "PASS" if not row["errors"] else "FAIL"
        print(f"{state} {name:24} {row['duration_seconds']:6.2f}s  peak {row['peak_dbfs']:6.2f} dBFS  loudness {row['loudness']['integrated_lufs']:5.1f} LUFS", flush=True)
        for error in row["errors"]:
            print(f"     {error}")
    checks = balance_checks(rows)
    for check in checks:
        print(("PASS " if check["pass"] else "FAIL ") + check["check"])
    report = {"method": "Decoded runtime audio, 4x reconstruction, periodic seam comparison, Welch spectrum and FFmpeg EBU R128. Playback estimates apply script gains and default mixers to file loudness; no human listening or live capture claim.",
              "encoder": {"soundfile": sf.__version__, "libsndfile": sf.__libsndfile_version__,
                          "vorbis_compression_level": VORBIS_COMPRESSION, "sample_rate": 48000,
                          "preserved_first_flute_sample_rate": 24000},
              "renderers": ["scripts/make_audio.py", "scripts/render_closing_theme.py"],
              "loudness_meter": str(args.ffmpeg), "balance_checks": checks,
              "missing": missing, "assets": rows}
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Report: {args.json}")
    return 1 if missing or any(row["errors"] for row in rows) or any(not check["pass"] for check in checks) else 0


if __name__ == "__main__":
    sys.exit(main())
