#!/usr/bin/env python3
"""Check the production encoder on a short dissolve followed by identical frames.

This isolates delivery-encoder texture changes. It is not a full-film render,
subjective playback review, camera-motion check or audio/listening test.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageOps

import render_closing_theme as renderer

SIZE = (1920, 1080)
FRAMES = 360
ROIS = {"face_hair": (1080, 40, 640, 360), "foliage": (50, 0, 640, 360)}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=renderer.PROJECT / "../development/visual-novel/archive/local/graphics-workspace/theme-stability")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    data = renderer.read_cues()
    assert data["fps"] == 60
    fps = data["fps"]
    blends = round(data["dissolve"] * fps)
    assert 0 < blends < 90 < FRAMES
    inputs = [renderer.PROJECT / "game" / shot["image"] for shot in data["shots"][-2:]]
    tracked = inputs + [renderer.CUES, Path(renderer.__file__), Path(__file__),
                        renderer.DEFAULT_SOURCE, renderer.PROJECT / "game" / data["audio"]]
    before = {str(path): sha(path) for path in tracked}
    pictures = []
    for path in inputs:
        with Image.open(path) as image:
            pictures.append(np.asarray(ImageOps.fit(image.convert("RGB"), SIZE, method=Image.Resampling.LANCZOS)))
    held = pictures[1].tobytes()
    ffmpeg = renderer.encoder()
    video = output / "held-frame.mp4"
    # Use the full film's GOP limit, exactly as the production delivery call.
    profile = renderer.delivery_video_args(round(data["duration"] * fps))
    command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080",
               "-r", str(fps), "-i", "pipe:0", "-an", *profile,
               "-movflags", "+faststart", str(video)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for frame in range(FRAMES):
            if frame < blends:
                mix = frame / blends
                mix = mix * mix * (3 - 2 * mix)
                raw = np.rint(pictures[0] * (1 - mix) + pictures[1] * mix).astype(np.uint8).tobytes()
            else:
                raw = held
            process.stdin.write(raw)
    finally:
        process.stdin.close()
    assert process.wait() == 0, "Encoder failed"
    decoded = subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-i", str(video),
        "-map", "0:v:0", "-progress", "pipe:1", "-nostats", "-f", "null", "-"],
        capture_output=True, text=True, check=True)
    fields = dict(line.split("=", 1) for line in decoded.stdout.splitlines() if "=" in line)
    assert not decoded.stderr.strip() and int(fields["frame"]) == FRAMES
    capture = cv2.VideoCapture(str(video))
    assert capture.isOpened()
    previous, metrics = {}, {name: [] for name in ROIS}
    for frame in range(FRAMES):
        okay, pixels = capture.read()
        assert okay, f"Missing decoded frame {frame}"
        for name, (x, y, width, height) in ROIS.items():
            region = pixels[y:y + height, x:x + width]
            if frame >= 90:
                delta = cv2.absdiff(region, previous[name])
                metrics[name].append({"frame": frame, "rgb_mad": float(delta.mean()),
                    "pixel_p99": float(np.quantile(delta, .99)), "pixel_max": int(delta.max()),
                    "changed_fraction": float(np.any(delta != 0, axis=2).mean())})
            previous[name] = region.copy()
        if frame in (90, 249, 250):
            cv2.imwrite(str(output / f"frame-{frame:03}.png"), pixels)
    assert not capture.read()[0], "Unexpected extra frames"
    capture.release()
    summary = {name: {key: max(row[key] for row in rows) for key in
        ("rgb_mad", "pixel_p99", "pixel_max", "changed_fraction")} for name, rows in metrics.items()}
    # Deliberately bounded to the nearly stable delivery measured in the proof,
    # allowing tiny codec rounding differences; not a mathematical lossless claim.
    passed = all(row["rgb_mad"] <= .002 and row["pixel_p99"] == 0
                 and row["pixel_max"] <= 3 and row["changed_fraction"] <= .0015
                 for row in summary.values())
    assert all(sha(path) == before[str(path)] for path in tracked), "Input changed during diagnostic"
    record = {"scope": "Six-second 1080p60 silent delivery-encoder diagnostic; no full film or listening approval",
        "source_sha256": before, "command": command, "source_held_rgb_sha256": hashlib.sha256(held).hexdigest(),
        "identical_input_frames": [blends, FRAMES - 1], "measured_adjacent_frames": [90, FRAMES - 1],
        "roi_xywh": ROIS, "summary": summary, "metrics": metrics, "passed": passed,
        "decoded_frames": FRAMES, "decode_errors": decoded.stderr,
        "output_sha256": sha(video), "output_bytes": video.stat().st_size,
        "limits": "Native RGB still fitting isolates the exact production encoder settings; it does not exercise the full compositor, runtime player, title fade, every source painting, subjective playback, or audio. Full-frame/art review and final film decode remain required."}
    (output / "diagnostic.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"passed": passed, "decoded_frames": FRAMES, "summary": summary}, indent=2))
    return int(not passed)


if __name__ == "__main__":
    raise SystemExit(main())
