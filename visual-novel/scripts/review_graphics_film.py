"""Inspect actual final delivery timestamps, final dissolves and held detail.

No render, runtime mutation, listening, or subjective playback is performed.
Outputs only a small JSON receipt and review strips under ignored test-results.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import wave

import cv2
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]


def project_relative(path):
    """Record sibling development outputs relative to the game project too."""
    return Path(os.path.relpath(path, ROOT)).as_posix()


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def call(args):
    return subprocess.run(args, capture_output=True, text=True, check=True)


def strip(path, frames, labels, width=None):
    tiles = []
    for frame in frames:
        im = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if width:
            im.thumbnail((width, width), Image.Resampling.LANCZOS)
        tiles.append(im)
    canvas = Image.new("RGB", (sum(i.width for i in tiles), max(i.height for i in tiles)+28), "#111111")
    draw = ImageDraw.Draw(canvas)
    x = 0
    for im, label in zip(tiles, labels):
        canvas.paste(im, (x, 28))
        draw.text((x+5, 7), label, fill="white")
        x += im.width
    canvas.save(path)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--movie", type=Path, default=ROOT / "build/closing-theme.mp4")
    p.add_argument("--output", type=Path, default=ROOT / "test-results/graphics-film")
    args = p.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    renderer_path = ROOT / "scripts/render_closing_theme.py"
    loader = importlib.util.spec_from_file_location("renderer", renderer_path)
    renderer = importlib.util.module_from_spec(loader)
    loader.loader.exec_module(renderer)
    ff = renderer.encoder()
    data = json.loads((ROOT / "game/closing_theme.json").read_text())
    fps, blend = data["fps"], round(data["dissolve"] * data["fps"])
    total = round(data["duration"] * fps)
    inputs = [ROOT / "game/closing_theme.json", renderer_path, Path(__file__)]
    runtime_audio = ROOT / "game" / data["audio"]
    inputs.append(runtime_audio)
    inputs += [ROOT / "game" / s["image"] for s in data["shots"]]
    input_hashes = {str(f.relative_to(ROOT)): sha(f) for f in inputs}
    movie_hash = sha(args.movie)
    render_snapshot_path = ROOT / "../development/visual-novel/archive/local/graphics-workspace/film-render-inputs.json"
    render_snapshot = json.loads(render_snapshot_path.read_text())
    assert render_snapshot["output"]["sha256"] == movie_hash
    assert all(sha(ROOT / p) == h for p, h in render_snapshot["inputs"].items())
    source = renderer.DEFAULT_SOURCE
    with wave.open(str(source)) as wav:
        source_audio = {"file": source.name, "sha256": sha(source), "sample_rate": wav.getframerate(),
                        "channels": wav.getnchannels(), "sample_frames": wav.getnframes(),
                        "duration_seconds": wav.getnframes()/wav.getframerate()}
    metadata = call([ff, "-hide_banner", "-i", str(args.movie), "-map", "0:v:0", "-map", "0:a:0", "-t", "0", "-f", "null", "-"])
    (out / "container-metadata.txt").write_text(metadata.stderr)
    assert "1920x1080" in metadata.stderr and "60 fps" in metadata.stderr
    assert "48000 Hz, stereo" in metadata.stderr and "aac (LC)" in metadata.stderr

    packet_text = call([ff, "-hide_banner", "-loglevel", "error", "-i", str(args.movie),
                        "-map", "0:v:0", "-c", "copy", "-f", "framehash", "-"]).stdout
    timebase = Fraction(re.search(r"#tb 0:\s*(\d+/\d+)", packet_text).group(1))
    packets = [[int(v.strip()) for v in line.split(",")[:5]]
               for line in packet_text.splitlines() if line and not line.startswith("#")]
    pts = [r[2] for r in packets]
    dts = [r[1] for r in packets]
    assert len(packets) == total and len(set(pts)) == total
    assert all(Fraction(b-a)*timebase == Fraction(1, fps) for a, b in zip(pts, pts[1:]))
    assert dts == pts, "Production profile uses no B-frame timestamp reordering"
    timestamp_result = {"packet_count": len(packets), "timebase": str(timebase),
        "all_pts_and_dts_equal": True, "strictly_monotonic_uniform_pts": True,
        "interval_seconds": str(Fraction(1, fps)), "first_pts_seconds": float(pts[0]*timebase),
        "last_pts_seconds": float(pts[-1]*timebase),
        "presentation_end_seconds": float((pts[-1]+packets[-1][3])*timebase),
        "packet_audit_sha256": hashlib.sha256(packet_text.encode()).hexdigest()}
    audio_text = call([ff, "-hide_banner", "-loglevel", "error", "-i", str(args.movie),
                       "-map", "0:a:0", "-c", "copy", "-f", "framehash", "-"]).stdout
    audio_tb = Fraction(re.search(r"#tb 0:\s*(\d+/\d+)", audio_text).group(1))
    audio_rows = [[int(v.strip()) for v in line.split(",")[:5]]
                  for line in audio_text.splitlines() if line and not line.startswith("#")]
    assert all(b[2] > a[2] for a, b in zip(audio_rows, audio_rows[1:]))
    audio_end = float((audio_rows[-1][2]+audio_rows[-1][3])*audio_tb)
    assert audio_end == source_audio["duration_seconds"]
    audio_result = {"codec": "AAC LC", "sample_rate": 48000, "channels": 2,
        "bitrate_demux_report_kbps": 257, "packet_count": len(audio_rows), "timebase": str(audio_tb),
        "first_packet_pts_seconds": float(audio_rows[0][2]*audio_tb), "presentation_end_seconds": audio_end,
        "packet_audit_sha256": hashlib.sha256(audio_text.encode()).hexdigest(),
        "note": "Negative first packet is AAC encoder priming; actual track presentation ends at the supplied WAV duration. No listening or new signal-master comparison is claimed."}

    cap = cv2.VideoCapture(str(args.movie))
    assert cap.isOpened()
    info = {"width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": cap.get(cv2.CAP_PROP_FPS), "reported_frames": int(cap.get(cv2.CAP_PROP_FRAME_COUNT))}
    assert tuple(info.values()) == (1920, 1080, 60.0, total)
    starts = [round(s["at"]*fps) for s in data["shots"]]
    transitions = []
    crops = [
        {"face_hair": [250, 200, 890, 560], "foliage": [1460, 110, 1880, 430]},
        {"face_hair": [480, 130, 1120, 490], "foliage": [1300, 0, 1880, 360]},
        {"face_hair": [950, 70, 1510, 430], "foliage": [40, 240, 680, 600]},
    ]
    holds = []
    for j, i in enumerate(range(len(starts)-3, len(starts))):
        shot = data["shots"][i]
        assert shot["zoom"] == [1.0, 1.0]
        assert shot.get("focus_to", shot["focus"]) == shot["focus"]
        transitions.append({"shot": i+1, "label": shot["label"], "start": starts[i],
                            "end": starts[i]+blend, "samples": {}, "thumbs": [], "adjacent_rgb_mae": []})
        end = starts[i+1]-1 if i+1 < len(starts) else min(round(data["title_at"]*fps)-1, round((data["duration"]-data["fade_out"])*fps)-1)
        holds.append({"shot": i+1, "label": shot["label"], "start": starts[i]+blend+1, "end": end,
                      "crop_boxes": crops[j], "observations": {k: [] for k in crops[j]}, "worst_pairs": {}})
    start, end = transitions[0]["start"]-1, holds[-1]["end"]
    assert cap.set(cv2.CAP_PROP_POS_FRAMES, start)
    previous = None
    selected_offsets = set(range(0, blend+1, blend//6))
    for n in range(start, end+1):
        ok, frame = cap.read()
        assert ok, n
        for tr in transitions:
            if tr["start"] <= n <= tr["end"]:
                tr["thumbs"].append(cv2.resize(frame, (480, 270), interpolation=cv2.INTER_AREA))
                if n-tr["start"] in selected_offsets:
                    tr["samples"][n] = frame.copy()
                tr["adjacent_rgb_mae"].append(float(cv2.absdiff(frame, previous).mean()))
        for hold in holds:
            if hold["start"] < n <= hold["end"]:
                for name, (x0, y0, x1, y1) in hold["crop_boxes"].items():
                    a, b = previous[y0:y1, x0:x1], frame[y0:y1, x0:x1]
                    delta = cv2.absdiff(a, b)
                    row = {"frame": n, "rgb_mae": float(delta.mean()), "maximum_channel_delta": int(delta.max()),
                           "changed_pixel_fraction": float(np.any(delta, axis=2).mean())}
                    hold["observations"][name].append(row)
                    worst = hold["worst_pairs"].get(name)
                    if worst is None or row["rgb_mae"] > worst[0]:
                        hold["worst_pairs"][name] = (row["rgb_mae"], n, a.copy(), b.copy())
        previous = frame
        if n % 300 == 0:
            print("Measured ending frame", n, "of", end, flush=True)
    cap.release()
    transition_reports = []
    for tr in transitions:
        thumbs = np.asarray(tr["thumbs"], dtype=np.float32)
        a, diff = thumbs[0], thumbs[-1]-thumbs[0]
        denominator = float(np.sum(diff*diff, dtype=np.float64))
        mix = np.sum((thumbs-a)*diff, axis=(1, 2, 3), dtype=np.float64)/denominator
        expected = np.linspace(0, 1, blend+1)
        expected = expected*expected*(3-2*expected)
        residuals = np.mean(np.abs((thumbs-a)-mix[:, None, None, None]*diff), axis=(1, 2, 3))
        keys = sorted(tr["samples"])
        path = out / f"transition-{tr['shot']:02}.png"
        strip(path, [tr["samples"][n] for n in keys], [f"{n/fps:.3f}s" for n in keys], width=384)
        # Native-size central facial/foliage detail, with no image resampling.
        box = holds[tr["shot"]-(len(starts)-2)]["crop_boxes"]["face_hair"]
        x0, y0, x1, y1 = box
        selected = [keys[0], keys[len(keys)//2], keys[-1]]
        detail_path = out / f"transition-{tr['shot']:02}-native.png"
        strip(detail_path, [tr["samples"][n][y0:y1, x0:x1] for n in selected], [f"{n/fps:.3f}s" for n in selected])
        transition_reports.append({"shot": tr["shot"], "label": tr["label"], "start_frame": tr["start"],
            "end_frame": tr["end"], "start_seconds": tr["start"]/fps, "sampled_frames": len(thumbs),
            "maximum_abs_opacity_error": float(np.max(np.abs(mix-expected))),
            "minimum_opacity_step": float(np.diff(mix).min()), "maximum_opacity_step": float(np.diff(mix).max()),
            "maximum_residual_rgb_mae_at480x270": float(residuals.max()),
            "maximum_full_frame_adjacent_rgb_mae": max(tr["adjacent_rgb_mae"]),
            "native_frame_samples": keys, "strip": project_relative(path), "native_detail": project_relative(detail_path),
            "opacity_samples": mix.tolist()})
    hold_reports = []
    for hold in holds:
        statistics = {}
        for name, observations in hold["observations"].items():
            mae = np.asarray([r["rgb_mae"] for r in observations])
            statistics[name] = {"pairs": len(mae), "mean_rgb_mae": float(mae.mean()),
                "maximum_rgb_mae": float(mae.max()), "p99_rgb_mae": float(np.quantile(mae, .99)),
                "maximum_channel_delta": max(r["maximum_channel_delta"] for r in observations),
                "maximum_changed_pixel_fraction": max(r["changed_pixel_fraction"] for r in observations)}
            settled = [r for r in observations if r["frame"] >= hold["start"]+round(.5*fps)]
            statistics[name]["after_first_half_second"] = {
                "pairs": len(settled), "maximum_rgb_mae": max(r["rgb_mae"] for r in settled),
                "maximum_channel_delta": max(r["maximum_channel_delta"] for r in settled),
                "maximum_changed_pixel_fraction": max(r["changed_pixel_fraction"] for r in settled)}
            _, n, a, b = hold["worst_pairs"][name]
            path = out / f"hold-{hold['shot']:02}-{name}-native.png"
            strip(path, [a, b], [f"{(n-1)/fps:.3f}s", f"{n/fps:.3f}s"])
            statistics[name]["worst_adjacent_pair_strip"] = project_relative(path)
        hold_reports.append({k: v for k, v in hold.items() if k not in ("worst_pairs", "observations")}
                            | {"statistics": statistics, "observations": hold["observations"]})
    assert sha(args.movie) == movie_hash
    assert sha(source) == source_audio["sha256"]
    assert all(sha(ROOT / p) == h for p, h in input_hashes.items())
    report = {"created_at_utc": datetime.now(timezone.utc).isoformat(), "movie": {
        "file": project_relative(args.movie), "sha256": movie_hash, "bytes": args.movie.stat().st_size, **info},
        "inputs": input_hashes, "inputs_unchanged_during_check": True,
        "render_snapshot": project_relative(render_snapshot_path), "render_snapshot_sha256": sha(render_snapshot_path),
        "render_snapshot_matches_movie_and_inputs": True, "source_audio": source_audio, "audio": audio_result,
        "runtime_audio": {"file": str(runtime_audio.relative_to(ROOT)), "sha256": input_hashes[str(runtime_audio.relative_to(ROOT))],
                          "role": "Separate runtime Vorbis asset; standalone MP4 encodes the supplied WAV instead."},
        "delivery_profile": renderer.delivery_video_args(total), "ffmpeg": ff, "ffprobe_available": bool(shutil.which("ffprobe")),
        "metadata_method": "Bundled FFmpeg demux metadata plus stored packet framehash and OpenCV video decode",
        "timestamps": timestamp_result, "decoded_frame_range": [start, end],
        "transitions": transition_reports, "held_shots": hold_reports,
        "method_limit": "Native timestamps and decoded frames, not subjective real-time viewing or auditory listening. Full renderer stream decode is recorded separately. Opacity fitting uses 480x270 whole-frame copies; held-detail differences use native pixels. No title/dissolve/fade frames enter held-detail statistics.",
        "visual_review": "Pending inspection of generated strips; metrics alone are not artistic approval."}
    (out / "verification.json").write_text(json.dumps(report, indent=2)+"\n")
    print("Receipt:", out / "verification.json", flush=True)


if __name__ == "__main__":
    main()
