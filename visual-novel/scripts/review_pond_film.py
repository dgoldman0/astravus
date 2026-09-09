"""Check the pond-image film revision without repeating the unchanged ending audit.

Reads the previous graphics-film receipt, the replacement MP4 and the current
renderer snapshot. Exports only three decoded frames for manual visual review.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import re

import cv2

from review_graphics_film import ROOT, call, sha


def packet_audit(ffmpeg, movie, stream):
    text = call([ffmpeg, "-hide_banner", "-loglevel", "error", "-i", str(movie),
                 "-map", stream, "-c", "copy", "-f", "framehash", "-"]).stdout
    timebase = Fraction(re.search(r"#tb 0:\s*(\d+/\d+)", text).group(1))
    rows = [[int(v.strip()) for v in line.split(",")[:5]]
            for line in text.splitlines() if line and not line.startswith("#")]
    return rows, timebase, hashlib.sha256(text.encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--movie", type=Path, default=ROOT / "build/closing-theme.mp4")
    parser.add_argument("--previous", type=Path,
                        default=ROOT / "test-results/graphics-film/verification.json")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "test-results/graphics-film/pond-update")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    previous = json.loads(args.previous.read_text())
    snapshot_path = ROOT / "../development/visual-novel/archive/local/graphics-workspace/film-render-inputs.json"
    snapshot = json.loads(snapshot_path.read_text())
    movie_hash = sha(args.movie)
    assert snapshot["output"]["sha256"] == movie_hash
    assert movie_hash != previous["movie"]["sha256"], "Replacement film has not arrived"
    assert all(sha(ROOT / path) == digest for path, digest in snapshot["inputs"].items())
    changed = {path: {"previous": previous["inputs"].get(path), "current": digest}
               for path, digest in snapshot["inputs"].items()
               if previous["inputs"].get(path) != digest}
    image_path = "game/images/cg/book-one/garden-compromise.png"
    assert set(changed) == {image_path}, changed

    renderer_path = ROOT / "scripts/render_closing_theme.py"
    loader = importlib.util.spec_from_file_location("renderer", renderer_path)
    renderer = importlib.util.module_from_spec(loader)
    loader.loader.exec_module(renderer)
    ffmpeg = renderer.encoder()
    cue = json.loads((ROOT / "game/closing_theme.json").read_text())
    fps, count = cue["fps"], round(cue["duration"] * cue["fps"])
    assert sha(renderer.DEFAULT_SOURCE) == previous["source_audio"]["sha256"]
    runtime_audio = ROOT / previous["runtime_audio"]["file"]
    assert sha(runtime_audio) == previous["runtime_audio"]["sha256"]

    metadata = call([ffmpeg, "-hide_banner", "-i", str(args.movie), "-map", "0:v:0",
                     "-map", "0:a:0", "-t", "0", "-f", "null", "-"]).stderr
    assert all(value in metadata for value in ["1920x1080", "60 fps", "48000 Hz, stereo", "aac (LC)"])
    metadata_path = args.output / "container-metadata.txt"
    metadata_path.write_text(metadata)
    rows, timebase, video_audit_hash = packet_audit(ffmpeg, args.movie, "0:v:0")
    assert len(rows) == count and all(row[1] == row[2] for row in rows)
    assert rows[0][2] == 0
    assert all((b[2] - a[2]) * timebase == Fraction(1, fps) for a, b in zip(rows, rows[1:]))
    audio_rows, audio_tb, audio_hash = packet_audit(ffmpeg, args.movie, "0:a:0")
    assert audio_hash == previous["audio"]["packet_audit_sha256"], "Encoded song packets changed"

    index, shot = next((i, shot) for i, shot in enumerate(cue["shots"])
                       if "game/" + shot["image"] == image_path)
    start = round(shot["at"] * fps)
    blend = round(cue["dissolve"] * fps)
    settled_time = (shot["at"] + cue["dissolve"] + cue["shots"][index+1]["at"]) / 2
    positions = {"incoming-start": start, "incoming-midpoint": start + blend//2,
                 "settled-planting": round(settled_time * fps)}
    cap = cv2.VideoCapture(str(args.movie))
    assert cap.isOpened()
    assert (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            cap.get(cv2.CAP_PROP_FPS), int(cap.get(cv2.CAP_PROP_FRAME_COUNT))) == (1920, 1080, float(fps), count)
    decoded = []
    for label, frame_number in positions.items():
        assert cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ok, frame = cap.read()
        assert ok and int(cap.get(cv2.CAP_PROP_POS_FRAMES)) == frame_number + 1
        path = args.output / (label + ".png")
        assert cv2.imwrite(str(path), frame)
        decoded.append({"label": label, "frame": frame_number,
                        "seconds": frame_number/fps, "file": str(path.relative_to(ROOT)),
                        "sha256": sha(path)})
    cap.release()

    log_path = ROOT / snapshot["renderer_log"]
    log = log_path.read_text()
    assert "Checking the complete video and audio streams" in log and "Preview:" in log
    assert sha(args.movie) == movie_hash
    assert all(sha(ROOT / path) == digest for path, digest in snapshot["inputs"].items())
    report = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "movie": {"file": str(args.movie.relative_to(ROOT)), "sha256": movie_hash,
                  "bytes": args.movie.stat().st_size, "width": 1920, "height": 1080, "fps": fps},
        "previous_review": {"file": str(args.previous.relative_to(ROOT)), "sha256": sha(args.previous),
                            "movie_sha256": previous["movie"]["sha256"],
                            "scope": "Historical final-three-transition and held-detail audit; not rerun or relabelled as measurements of this replacement."},
        "changed_render_inputs": changed,
        "render_snapshot": {"file": str(snapshot_path.relative_to(ROOT)), "sha256": sha(snapshot_path)},
        "renderer_decode_evidence": {"file": str(log_path.relative_to(ROOT)), "sha256": sha(log_path),
                                     "method": "Production renderer logs complete stream check then Preview only after successful frame-count/decode verification and atomic replacement."},
        "script_sha256": sha(Path(__file__)),
        "timestamps": {"frames": len(rows), "interval_seconds": str(Fraction(1, fps)),
                       "all_pts_equal_dts": True, "strictly_monotonic_uniform": True,
                       "last_pts_seconds": float(rows[-1][2]*timebase),
                       "presentation_end_seconds": float((rows[-1][2]+rows[-1][3])*timebase),
                       "packet_audit_sha256": video_audit_hash},
        "audio": {"codec": "AAC LC", "sample_rate": 48000, "channels": 2,
                  "encoded_packet_hash_identical_to_previous": True,
                  "packet_audit_sha256": audio_hash,
                  "presentation_end_seconds": float((audio_rows[-1][2]+audio_rows[-1][3])*audio_tb),
                  "source_wav_sha256": previous["source_audio"]["sha256"],
                  "runtime_ogg_sha256": previous["runtime_audio"]["sha256"]},
        "decoded_frames": decoded,
        "inputs_unchanged_during_check": True,
        "visual_review": "Pending manual inspection of the three decoded frames.",
        "limits": "Bounded changed-shot and timestamp check, not a repeat ending-motion study, full-film visual review, subjective playback, listening or seeking-performance test. Complete video/audio decode is evidenced by the production render log."
    }
    receipt_path = args.output / "verification.json"
    receipt_path.write_text(json.dumps(report, indent=2) + "\n")
    print(receipt_path)


if __name__ == "__main__":
    main()
