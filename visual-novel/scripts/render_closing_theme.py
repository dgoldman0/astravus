#!/usr/bin/env python3
"""Render the editable closing-theme cue sheet as a standalone MP4 preview.

Uses the supplied WAV without gain/EQ changes. Runtime uses the same cue sheet
and an Ogg encode, so the game does not need a second copy of the whole video.
Install imageio-ffmpeg==0.6.0 into .cache/video-tools, or set ASTRAVUS_FFMPEG.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import wave

from PIL import Image, ImageDraw, ImageFont

PROJECT = Path(__file__).resolve().parents[1]
CUES = PROJECT / "game/closing_theme.json"
DEFAULT_SOURCE = PROJECT.parents[1] / "Curiosity and Discovery.wav"


def encoder():
    if os.environ.get("ASTRAVUS_FFMPEG"):
        return os.environ["ASTRAVUS_FFMPEG"]
    sys.path.insert(0, str(PROJECT / ".cache/video-tools"))
    try:
        import imageio_ffmpeg
    except ImportError:
        raise SystemExit("Install imageio-ffmpeg==0.6.0 into .cache/video-tools, or set ASTRAVUS_FFMPEG.")
    return imageio_ffmpeg.get_ffmpeg_exe()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(ffmpeg, *args):
    subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", *map(str, args)], check=True)


def read_cues():
    data = json.loads(CUES.read_text())
    shots = data["shots"]
    starts = [s["at"] for s in shots]
    assert starts[0] == 0 and starts == sorted(set(starts))
    assert 0 < data["dissolve"] < min(b - a for a, b in zip(starts, starts[1:] + [data["duration"]]))
    for shot in shots:
        image = PROJECT / "game" / shot["image"]
        assert image.resolve().is_relative_to(PROJECT / "game/images") and image.is_file(), image
        assert all(1 <= z <= 1.12 for z in shot["zoom"])
        assert all(0 <= v <= 1 for v in shot["focus"])
        assert all(0 <= v <= 1 for v in shot.get("focus_to", shot["focus"]))
    return data


def encode_audio(ffmpeg, source, data):
    target = PROJECT / "game" / data["audio"]
    with wave.open(str(source)) as wav:
        duration = wav.getnframes() / wav.getframerate()
        assert abs(duration - data["duration"]) < .02, (duration, data["duration"])
        assert wav.getframerate() == 48000 and wav.getnchannels() == 2
        source_info = {"file": source.name, "sha256": digest(source), "sample_rate": wav.getframerate(),
                       "channels": wav.getnchannels(), "bits": wav.getsampwidth() * 8,
                       "frames": wav.getnframes(), "duration_seconds": duration}
    provenance = PROJECT / "docs/closing-theme-audio.json"
    if target.is_file() and provenance.is_file():
        previous = json.loads(provenance.read_text())
        output = previous.get("output", {})
        if (previous.get("source") == source_info and output.get("sha256") == digest(target)
                and output.get("codec") == "Vorbis" and output.get("quality") == 6):
            print("Using the unchanged runtime audio encode.", flush=True)
            return
    run(ffmpeg, "-i", source, "-map", "0:a:0", "-c:a", "libvorbis", "-q:a", "6", target)
    record = {
        "source": source_info,
        "source_kind": "Original WAV supplied by the user at the workspace root; distinct from the CC0 sample library.",
        "output": {"file": target.relative_to(PROJECT).as_posix(), "sha256": digest(target),
                   "codec": "Vorbis", "quality": 6},
        "processing": "Encoding only; no gain, EQ, compression, edits or fades applied to the supplied song.",
        "renderer": "scripts/render_closing_theme.py",
        "ffmpeg": subprocess.check_output([ffmpeg, "-version"], text=True).splitlines()[0],
    }
    provenance.write_text(json.dumps(record, indent=2) + "\n")
    print(f"Encoded {target.relative_to(PROJECT)}", flush=True)


def title_overlay(path, width, height, data):
    # A typographic overlay only. FFmpeg reads all scene artwork unchanged.
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    scale = width / 1920
    for text, font, size, y, color in (
        ("ASTRAVUS", "Story-Serif.ttf", 68, 465, "#f4e7cb"),
        ("S E E D S   O F   Y O U T H", "Lato-Regular.ttf", 25, 560, "#e2cba2"),
    ):
        face = ImageFont.truetype(str(PROJECT / "game/fonts" / font), round(size * scale))
        draw.text((width * data.get("title_x", .5), y * scale), text, font=face, anchor="mt", fill=color,
                  stroke_width=max(1, round(scale)), stroke_fill=(0, 0, 0, 150))
    overlay.save(path)


def camera_filter(shot, width, height, frames):
    """Sample a floating-point camera transform, avoiding zoompan's rounded crop."""
    z0, z1 = shot["zoom"]
    fx0, fy0 = shot["focus"]
    fx1, fy1 = shot.get("focus_to", shot["focus"])
    progress = f"(on/{frames-1})"
    ease = f"({progress}*{progress}*(3-2*{progress}))"
    zoom = f"({z0}+({z1}-{z0})*{ease})"
    fx = f"({fx0}+({fx1}-{fx0})*{ease})"
    fy = f"({fy0}+({fy1}-{fy0})*{ease})"
    left, top = f"(W-W*{zoom})*{fx}", f"(H-H*{zoom})*{fy}"
    right, bottom = f"({left})+W*{zoom}", f"({top})+H*{zoom}"
    # Transform all color planes at full resolution, before delivery subsampling.
    # Perspective's cubic sampler preserves fractional positions at every frame.
    return (f"perspective=x0='{left}':y0='{top}':x1='{right}':y1='{top}':"
            f"x2='{left}':y2='{bottom}':x3='{right}':y3='{bottom}':"
            "sense=destination:eval=frame:interpolation=cubic")


def render(ffmpeg, source, output, data, width):
    height = width * 9 // 16
    assert height % 2 == 0, "Choose a 16:9 width with an even height (1280 or 1920)."
    fps, dissolve, total = data["fps"], data["dissolve"], data["duration"]
    output.parent.mkdir(parents=True, exist_ok=True)
    # Temporary clips disappear after the render; only the current preview remains.
    with tempfile.TemporaryDirectory(prefix="closing-theme-", dir=PROJECT / ".cache") as scratch:
        scratch = Path(scratch)
        clips = []
        for index, shot in enumerate(data["shots"]):
            end = data["shots"][index + 1]["at"] + dissolve if index + 1 < len(data["shots"]) else total
            frames = round((end - shot["at"]) * fps)
            # Size the still once, cache it, then sample each camera frame.
            base = (f"scale={width}:{height}:force_original_aspect_ratio=increase:flags=lanczos,"
                    f"crop={width}:{height},format=yuv444p")
            loop = f"loop=loop=-1:size=1:start=0,setpts=N/({fps}*TB)"
            camera = camera_filter(shot, width, height, frames)
            held = (shot["zoom"][0] == shot["zoom"][1]
                    and shot.get("focus_to", shot["focus"]) == shot["focus"])
            # A held composition only needs sampling once, before it is looped.
            filters = f"{base},{camera},{loop}" if held else f"{base},{loop},{camera}"
            filters += ",setsar=1,format=yuv420p"
            clip = scratch / f"shot-{index:02}.mp4"
            print(f"Shot {index+1:02}/{len(data['shots'])}: {shot['label']}", flush=True)
            run(ffmpeg, "-filter_threads", "4", "-framerate", fps, "-i", PROJECT / "game" / shot["image"],
                "-vf", filters, "-frames:v", frames, "-an", "-c:v", "libx264", "-preset", "fast",
                "-crf", "18", "-threads", "4", clip)
            clips.append(clip)

        overlay = scratch / "title.png"
        title_overlay(overlay, width, height, data)
        inputs = []
        graph = []
        for index, clip in enumerate(clips):
            inputs += ["-threads", "1", "-i", clip]
            graph.append(f"[{index}:v]setpts=PTS-STARTPTS,fps={fps},settb=AVTB[v{index}]")
        last = "v0"
        for index in range(1, len(clips)):
            name = f"x{index}"
            graph.append(f"[{last}][v{index}]xfade=transition=fade:duration={dissolve}:"
                         f"offset={data['shots'][index]['at']}[{name}]")
            last = name
        audio_index = len(clips)
        title_index = audio_index + 1
        inputs += ["-i", source, "-loop", "1", "-framerate", str(fps), "-i", overlay]
        graph.append(f"[{title_index}:v]format=rgba,fade=t=in:st={data['title_at']}:"
                     f"d={data['title_fade']}:alpha=1[title]")
        graph.append(f"[{last}][title]overlay=shortest=1,"
                     f"fade=t=in:d={data['fade_in']},"
                     f"fade=t=out:st={total-data['fade_out']}:d={data['fade_out']},"
                     f"format=yuv420p[film]")
        filters = scratch / "filter.txt"
        filters.write_text(";\n".join(graph))
        print("Joining shots and attaching the supplied song…", flush=True)
        completed = scratch / "completed.mp4"
        run(ffmpeg, "-filter_complex_threads", "1", *inputs, "-filter_complex_script", filters,
            "-map", "[film]", "-map", f"{audio_index}:a:0", "-t", total,
            "-r", fps, "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-threads", "4",
            "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", completed)
        print("Checking the complete video and audio streams…", flush=True)
        check = subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-i", str(completed),
                                "-map", "0:v:0", "-map", "0:a:0", "-progress", "pipe:1", "-nostats",
                                "-f", "null", "-"], capture_output=True, text=True, check=True)
        fields = dict(line.split("=", 1) for line in check.stdout.splitlines() if "=" in line)
        assert int(fields["frame"]) == round(total * fps), fields
        assert not check.stderr.strip(), check.stderr
        completed.replace(output)
    print(f"Preview: {output} ({output.stat().st_size/1024**2:.1f} MiB)", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=PROJECT / "build/closing-theme.mp4")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--audio-only", action="store_true")
    args = parser.parse_args()
    ffmpeg, data = encoder(), read_cues()
    encode_audio(ffmpeg, args.source, data)
    if not args.audio_only:
        render(ffmpeg, args.source, args.output, data, args.width)


if __name__ == "__main__":
    main()
