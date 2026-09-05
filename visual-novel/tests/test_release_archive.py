"""Only the pinned engine's two generated runtime files may bypass cache exclusion."""
import importlib.util
import io
from pathlib import Path
import unittest
import zipfile

SPEC = importlib.util.spec_from_file_location("check_release", Path(__file__).parents[1] / "scripts/check_release.py")
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


class ArchiveExclusionTests(unittest.TestCase):
    def archive(self, names):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w") as archive:
            for name in names:
                archive.writestr(name, b"content")
        return zipfile.ZipFile(stream)

    def test_exact_generated_runtime_files_allowed(self):
        with self.archive(["game/cache/", *release.GENERATED_RUNTIME]) as archive:
            release.check_members(archive)

    def test_developer_cache_rejected(self):
        with self.archive(["game/cache/build_info.json", "game/cache/analysis.json"]) as archive:
            with self.assertRaises(AssertionError):
                release.check_members(archive)

    def test_wrong_python_cache_rejected(self):
        with self.archive(["game/cache/bytecode-311.rpyb"]) as archive:
            with self.assertRaises(AssertionError):
                release.check_members(archive)

    def test_desktop_prefix_does_not_hide_saves(self):
        with self.archive(["release/game/cache/build_info.json", "release/game/saves/1-1.save"]) as archive:
            with self.assertRaises(AssertionError):
                release.check_members(archive, "release/")
