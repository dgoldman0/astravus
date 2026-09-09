"""Exercise the shipped fadeout branch and fail safely on SDK drift."""
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import project


class WebAudioPatchTests(unittest.TestCase):
    def test_unrecognized_sdk_leaves_archive_untouched(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "game.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(project.WEB_AUDIO_MEMBER, b"unknown engine source")
            before = path.read_bytes()
            with self.assertRaisesRegex(SystemExit, "Unexpected Ren'Py web audio source"):
                project.patch_web_audio(path)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(list(Path(directory).iterdir()), [path])

    def test_patch_preserves_other_archive_members_and_metadata(self):
        source = b"engine preamble\n" + project.WEB_AUDIO_FADEOUT_START + b"body\n};\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "game.zip"
            member = zipfile.ZipInfo("game/audio/rain.ogg", (2026, 1, 2, 3, 4, 6))
            member.external_attr = 0o100644 << 16
            member.compress_type = zipfile.ZIP_DEFLATED
            with zipfile.ZipFile(path, "w") as archive:
                archive.comment = b"retained archive metadata"
                archive.writestr(member, b"unchanged audio bytes")
                archive.writestr(project.WEB_AUDIO_MEMBER, source)
            with patch.object(project, "WEB_AUDIO_SOURCE_SHA256", hashlib.sha256(source).hexdigest()):
                project.patch_web_audio(path)
            with zipfile.ZipFile(path) as archive:
                self.assertIsNone(archive.testzip())
                self.assertEqual(archive.comment, b"retained archive metadata")
                self.assertEqual(archive.read(member.filename), b"unchanged audio bytes")
                after = archive.getinfo(member.filename)
                self.assertEqual((after.date_time, after.external_attr, after.compress_type),
                                 (member.date_time, member.external_attr, member.compress_type))
                self.assertEqual(archive.read(project.WEB_AUDIO_MEMBER),
                                 source.replace(project.WEB_AUDIO_FADEOUT_START,
                                                project.WEB_AUDIO_FADEOUT_START + project.WEB_AUDIO_PENDING_STOP))

    def test_failed_archive_rewrite_preserves_original(self):
        source = project.WEB_AUDIO_FADEOUT_START + b"};"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "game.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(project.WEB_AUDIO_MEMBER, source)
                archive.writestr("game/story.rpy", b"story")
            before = path.read_bytes()
            with patch.object(project, "WEB_AUDIO_SOURCE_SHA256", hashlib.sha256(source).hexdigest()), \
                    patch.object(project.shutil, "copyfileobj", side_effect=OSError("simulated write failure")):
                with self.assertRaisesRegex(OSError, "simulated write failure"):
                    project.patch_web_audio(path)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(list(Path(directory).iterdir()), [path])

    def test_actual_pinned_fadeout_clears_pending_audio_and_preserves_running_fades(self):
        sdk_source = project.SDK / project.WEB_AUDIO_MEMBER
        if not sdk_source.is_file() or not shutil.which("node"):
            self.skipTest("Pinned SDK and Node are required for the engine behavior check")
        original = sdk_source.read_bytes()
        patched = project.patched_web_audio(original).decode("utf-8-sig")
        def function(text, name):
            start = text.index(f"renpyAudio.{name} =")
            return text[start:text.index("\n};", start) + 3]
        javascript = r"""
const assert = require('node:assert/strict');
let state, stops, ramps, starts, videoStops, timers;
const context = { currentTime: 20 };
const get_channel = () => state;
const renpyAudio = {};
const start_playing = () => { starts += 1; };
const stop_playing = c => { c.playing = c.queued; c.queued = null; stops += 1; };
const video_stop = c => { c.playing = c.queued; c.queued = null; videoStops += 1; };
const linearRampToValue = (...args) => ramps.push(args.slice(1));
const setTimeout = (...args) => timers.push(args.slice(1));
function setup({started = null, video = false, duration = 30} = {}) {
    stops = starts = videoStops = 0; ramps = []; timers = [];
    const source = { stop: t => timers.push(t) };
    state = { video, playing: {started, source, buffer: {duration}},
              queued: {tight: true, fadeout: null}, fade_volume: {gain: {value: .8}} };
}
"""
        javascript += function(patched, "stop") + "\n" + function(patched, "fadeout")
        javascript += r"""
setup(); renpyAudio.fadeout(8, 2);
assert.equal(state.playing, null); assert.equal(state.queued, null);
assert.equal(stops, 1); assert.equal(starts, 0); assert.equal(ramps.length, 0);
setup(); state.playing = null; renpyAudio.fadeout(8, 2);
assert.equal(state.playing, null); assert.equal(state.queued, null);
setup({started: 10}); renpyAudio.fadeout(8, 2);
assert.deepEqual(ramps, [[.8, 0, 2]]); assert.deepEqual(timers, [22]);
assert.equal(stops, 0); assert.equal(state.queued, null);
setup({started: 10, duration: 11}); renpyAudio.fadeout(8, 3);
assert.deepEqual(ramps, [[.8, 0, 3]]); assert.deepEqual(timers, [23]);
assert.equal(state.queued.fadeout, 2); assert.equal(stops, 0);
setup({started: 10, video: true}); renpyAudio.fadeout(8, 2);
assert.deepEqual(timers, [[2000, 8]]); assert.equal(stops, 0);
setup({video: true}); renpyAudio.fadeout(8, 2);
assert.notEqual(state.playing, null); assert.equal(starts, 1); assert.equal(stops, 0);
"""
        # Establish that the original branch exhibits the same pending-loop bug.
        javascript += function(original.decode("utf-8-sig"), "fadeout")
        javascript += "\nsetup(); renpyAudio.fadeout(8, 2); assert.notEqual(state.playing, null); assert.equal(starts, 1);\n"
        result = subprocess.run(["node", "-e", javascript], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
