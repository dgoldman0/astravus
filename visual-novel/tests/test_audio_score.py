"""Score registry, measured mix guards, and reader-reached music boundaries."""
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

import numpy as np
from scipy.signal import resample_poly

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "scripts"))
from audio_check import balance_checks, expected_audio, inventory_errors, playback_uses, reconstructed_peak
from score_catalog import SCORES

SCENES = tuple(re.findall(r'^        \("([a-z_]+)", ', (PROJECT / "game/book_structure.rpy").read_text(), re.M))
STORY_FILES = ("script.rpy", "family_book_one.rpy", "friendships_book_one.rpy")
MUSIC_EVENT = re.compile(r'^\s*(?:play music "audio/([a-z_]+)\.ogg"|stop music)(?:\s|$)')
SPOKEN = re.compile(r'^\s+\w+ "')


def scene_lines():
    result = {}
    for filename in STORY_FILES:
        scene = None
        for line in (PROJECT / "game" / filename).read_text().splitlines():
            entry = re.search(r'enter_scene\("([a-z_]+)"\)', line)
            if entry:
                scene = entry[1]
                result[scene] = []
            if scene:
                result[scene].append(line)
    return result


def music_events(lines):
    return [match[1] for line in lines if (match := MUSIC_EVENT.match(line))]


def measured_row(name, *levels):
    return {"file": "game/" + expected_audio()[name],
            "playback_uses": [{"lufs_before_user_mixer": level} for level in levels]}


class AudioScoreTests(unittest.TestCase):
    def test_score_inventory_has_no_unused_or_unregistered_delivery(self):
        uses = playback_uses()
        self.assertEqual(inventory_errors(uses), [])
        self.assertEqual(set(uses), set(expected_audio()))
        for name, filename in expected_audio().items():
            with self.subTest(cue=name):
                self.assertTrue((PROJECT / "game" / filename).is_file(), filename)

    def test_unregistered_audio_cannot_escape_measurement(self):
        with tempfile.TemporaryDirectory() as directory:
            audio = Path(directory)
            (audio / "unlisted.ogg").touch()
            self.assertEqual(inventory_errors({}, audio), ["Unregistered delivered audio: audio/unlisted.ogg"])
            errors = inventory_errors({"unlisted": [{"file": "audio/unlisted.ogg"}]}, audio)
            self.assertIn("Playback references unregistered audio: unlisted", errors)
            errors = inventory_errors({"home_theme": [{"file": "audio/home_theme.wav"}]}, audio)
            self.assertIn("Playback references audio/home_theme.wav; expected audio/home_theme.ogg", errors)

    def test_chunked_peak_finds_boundary_transient_identically_to_full_reconstruction(self):
        signal = np.random.default_rng(813).normal(0, .02, (1031, 2))
        signal[256:259] = [[.3, -.32], [-.35, .34], [.28, -.29]]
        expected = np.max(np.abs(resample_poly(signal, 4, 1, axis=0)))
        self.assertAlmostEqual(reconstructed_peak(signal, block_frames=257), expected, places=12)

    def test_every_playback_gain_is_checked_and_roles_retain_dynamics(self):
        rows = [measured_row(name, score.target_lufs) for name, score in SCORES.items()]
        self.assertTrue(all(check["pass"] for check in balance_checks(rows)))
        rows = [row for row in rows if row["file"] != "game/audio/home_theme.ogg"]
        target = SCORES["home_theme"].target_lufs
        rows.append(measured_row("home_theme", target, target + 4))
        failed = [check["check"] for check in balance_checks(rows) if not check["pass"]]
        self.assertTrue(any(check.startswith("home_theme:") for check in failed))
        self.assertLess(SCORES["grief_theme"].target_lufs, SCORES["home_theme"].target_lufs)

    def test_each_chapter_sets_music_before_its_first_line_for_direct_jumps(self):
        scenes = scene_lines()
        self.assertEqual(set(scenes), set(SCENES))
        for key in SCENES:
            with self.subTest(scene=key):
                first_line = next(index for index, line in enumerate(scenes[key]) if SPOKEN.match(line))
                self.assertTrue(music_events(scenes[key][:first_line]), f"{key} depends on inherited music")

    def test_all_scored_transitions_are_reader_reached_and_keep_same_cue_continuation(self):
        for filename in STORY_FILES:
            text = (PROJECT / "game" / filename).read_text()
            self.assertNotIn("queue music", text, "Future dramatic cues must not start on a timer")
            for line in text.splitlines():
                match = MUSIC_EVENT.match(line)
                if match and match[1]:
                    with self.subTest(file=filename, cue=match[1]):
                        self.assertIn(match[1], SCORES)
                        self.assertIn("if_changed", line)

    def test_flute_events_have_no_score_and_remain_in_narrative_order(self):
        events = []
        for key in ("music_first", "family_rhythm"):
            music = "unknown"
            lines = scene_lines()[key]
            for index, line in enumerate(lines):
                change = MUSIC_EVENT.match(line)
                if change:
                    music = change[1]
                sound = re.match(r'^\s*play sound "audio/(flute_[a-z]+)\.wav"', line)
                if sound:
                    events.append(sound[1])
                    self.assertIsNone(music, f"Underscore competes with {sound[1]}")
                    following = next(text for text in lines[index + 1:] if SPOKEN.match(text))
                    expected = {"flute_attempt": "The first sound trembled, thinned, and broke.",
                                "flute_first": "We went a few notes at a time.",
                                "flute_practice": "Lyra clapped along,"}[sound[1]]
                    self.assertIn(expected, following)
        self.assertEqual(events, ["flute_attempt", "flute_first", "flute_practice"])
        first = "\n".join(scene_lines()["music_first"])
        self.assertLess(first.index("There was a note in there."), first.index('play sound "audio/flute_first.wav"'))

    def test_early_flute_and_supplied_song_are_preserved(self):
        manifest = json.loads((PROJECT / "docs/audio-sources.json").read_text())
        expected = {"flute_first.wav": manifest["preserved_first_flute_sha256"],
                    "flute_attempt.wav": "1d0ce9e8565d11971cf43767d209cf0838a24ea143ef5fddd261620e5208474d"}
        song = json.loads((PROJECT / "docs/closing-theme-audio.json").read_text())
        expected["curiosity_and_discovery.ogg"] = song["output"]["sha256"]
        for name, digest in expected.items():
            with self.subTest(cue=name):
                self.assertEqual(hashlib.sha256((PROJECT / "game/audio" / name).read_bytes()).hexdigest(), digest)

    def test_loss_has_no_music_and_previous_scene_ends_in_friendship(self):
        scenes = scene_lines()
        self.assertTrue(music_events(scenes["loss"]))
        self.assertTrue(all(cue is None for cue in music_events(scenes["loss"])))
        self.assertEqual(music_events(scenes["treehouse_dispute"])[-1], "friendship_warm")
        memorial = scenes["community_memorial"]
        silence_line = next(index for index, line in enumerate(memorial)
                            if "For a while, we stood with him in silence." in line)
        self.assertTrue(music_events(memorial[:silence_line + 1]))
        self.assertTrue(all(cue is None for cue in music_events(memorial[:silence_line + 1])))
        self.assertEqual(music_events(memorial[silence_line + 1:]), ["remembrance_theme"])


if __name__ == "__main__":
    unittest.main()
