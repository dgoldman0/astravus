"""Release retention must not remove usable exports after a failed build."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile


SPEC = importlib.util.spec_from_file_location("project", Path(__file__).parents[1] / "scripts/project.py")
project = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(project)


class ExportRetentionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "game").mkdir()
        (self.root / "docs").mkdir()
        (self.root / "docs/release-matrix.json").write_text(json.dumps({"release_version": "0.1-alpha"}))
        (self.root / "game/options.rpy").write_text(
            'define config.version = "0.1-alpha"\n'
            'define build.name = "astravus-book-one"\n'
        )
        self.dist = self.root / "dist"
        self.dist.mkdir()
        self.addCleanup(patch.stopall)
        patch.object(project, "PROJECT", self.root).start()
        self.old = self.archive("astravus-book-one-0.2.6-pc.zip")

    def archive(self, name, payload=b"release payload"):
        path = self.dist / name
        with zipfile.ZipFile(path, "w", zipfile.ZIP_STORED) as archive:
            archive.writestr("runtime", payload)
        return path

    def current_exports(self):
        return [self.archive(f"astravus-book-one-0.1-alpha-{platform}.zip")
                for platform in ("pc", "mac")]

    def test_reset_removes_only_recognized_superseded_exports(self):
        current = self.current_exports()
        legacy = self.archive("astravus-chapter-one-0.1.3-mac.zip")
        unrelated = self.archive("holiday-photos.zip")
        unrecognized = self.archive("astravus-book-one-review-pc.zip")
        saves = self.dist / "saves"
        saves.mkdir()
        save = saves / "1-1.save"
        save.write_bytes(b"player progress")
        project.prune_desktop_exports()
        self.assertFalse(self.old.exists())
        self.assertFalse(legacy.exists())
        self.assertTrue(all(path.exists() for path in current))
        self.assertTrue(unrelated.exists())
        self.assertTrue(unrecognized.exists())
        self.assertEqual(save.read_bytes(), b"player progress")

    def test_missing_current_export_preserves_previous_release(self):
        self.archive("astravus-book-one-0.1-alpha-pc.zip")
        with self.assertRaises(FileNotFoundError):
            project.prune_desktop_exports()
        self.assertTrue(self.old.exists())

    def test_corrupt_current_export_preserves_previous_release(self):
        current = self.current_exports()
        current[1].write_bytes(current[1].read_bytes().replace(b"release payload", b"damaged payload"))
        with self.assertRaisesRegex(SystemExit, "Corrupt export"):
            project.prune_desktop_exports()
        self.assertTrue(self.old.exists())

    def test_empty_current_export_preserves_previous_release(self):
        current = self.current_exports()
        with zipfile.ZipFile(current[1], "w"):
            pass
        with self.assertRaisesRegex(SystemExit, "Empty export"):
            project.prune_desktop_exports()
        self.assertTrue(self.old.exists())

    def test_normal_build_stops_before_packaging_when_matrix_is_not_approved(self):
        def command_result(command, **kwargs):
            if any(str(part).endswith("release_review.py") for part in command):
                raise subprocess.CalledProcessError(1, command)
        with patch.object(project.sys, "argv", ["project.py", "build"]), \
                patch.object(project.subprocess, "run", side_effect=command_result), \
                patch.object(project, "engine") as engine:
            with self.assertRaises(subprocess.CalledProcessError):
                project.main()
            engine.assert_not_called()

    def test_explicit_review_build_is_recorded_as_review_only(self):
        with patch.object(project.sys, "argv", ["project.py", "build", "--review-build"]), \
                patch.object(project.subprocess, "run") as run, \
                patch.object(project, "engine"), patch.object(project, "prune_desktop_exports"), \
                patch.object(project, "record_build") as record:
            project.main()
            run.assert_not_called()
            record.assert_called_once_with("desktop", True)

    def test_build_provenance_keeps_distinct_artifact_hashes_and_review_kind(self):
        self.current_exports()
        project.record_build("desktop", True)
        path = self.root / "build/release-builds.json"
        saved = json.loads(path.read_text())
        self.assertEqual(saved["builds"]["desktop"]["kind"], "review")
        self.assertEqual(len(saved["builds"]["desktop"]["files"]), 2)
        (self.root / "build/web.zip").write_bytes(b"web build")
        project.record_build("web", False)
        saved = json.loads(path.read_text())
        self.assertEqual(saved["builds"]["desktop"]["kind"], "review")
        self.assertEqual(saved["builds"]["web"]["kind"], "candidate")

    def test_wrong_version_blocks_desktop_and_web_before_any_packaging(self):
        options = self.root / "game/options.rpy"
        options.write_text(options.read_text().replace('"0.1-alpha"', '"0.1.1"'))
        for command in ("build", "web"):
            for review in ([], ["--review-build"]):
                with self.subTest(command=command, review=bool(review)), \
                        patch.object(project.sys, "argv", ["project.py", command, *review]), \
                        patch.object(project.subprocess, "run") as run, \
                        patch.object(project, "engine") as engine:
                    with self.assertRaisesRegex(SystemExit, "locked to '0.1-alpha'"):
                        project.main()
                    run.assert_not_called()
                    engine.assert_not_called()
        self.assertTrue(self.old.exists())

    def test_provenance_cannot_record_a_version_changed_during_build(self):
        self.current_exports()
        options = self.root / "game/options.rpy"
        options.write_text(options.read_text().replace('"0.1-alpha"', '"0.2.0"'))
        with self.assertRaisesRegex(SystemExit, "locked to '0.1-alpha'"):
            project.record_build("desktop", True)
        self.assertFalse((self.root / "build/release-builds.json").exists())


if __name__ == "__main__":
    unittest.main()
