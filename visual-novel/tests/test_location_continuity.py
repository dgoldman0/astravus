"""The release guard must not silently inherit review after pixels/uses change."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location("check_assets", Path(__file__).resolve().parents[1] / "scripts/check_assets.py")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class LocationReviewGuard(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repository = Path(self.temp.name)
        self.project = self.repository / "visual-novel"
        (self.project / "docs").mkdir(parents=True)
        (self.project / "game/images/backgrounds").mkdir(parents=True)
        (self.repository / "story.md").write_text("The old oak and its raised room.")
        (self.repository / "author-reference.png").write_bytes(b"author reference fixture")
        self.name = "game/images/backgrounds/treehouse.png"
        (self.project / self.name).write_bytes(b"image fixture; provenance is checked separately")
        self.assets = {self.name: {"sha256": "reviewed-pixels"}}
        self.data = {
            "schema_version": 1,
            "review_policy": {"passing_statuses": ["consistent", "consistent_crop"]},
            "locations": [{"id": "treehouse", "canonical_references": [{"file": self.name}, {"file": "../author-reference.png"}],
                           "source_facts": [{"file": "../story.md", "anchor": "old oak"}],
                           "invariants": [{"id": "raised-room"}], "views": [{"id": "wide"}]}],
            "issues": [],
            "assets": [{"file": self.name, "location_id": "treehouse", "view_id": "wide",
                        "required_invariants": ["raised-room"], "closing_theme_starts": [0],
                        "review_status": "consistent", "reviewed_sha256": "reviewed-pixels", "findings": []}],
            "tracked_asset_patterns": ["game/images/backgrounds/*treehouse*.png"],
        }
        self.theme = {"shots": [{"image": self.name.removeprefix("game/"), "at": 0}]}
        self.patch = patch.multiple(CHECKER, PROJECT=self.project, REPOSITORY=self.repository)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.data["assets"][0]["reviewed_reference_signature"] = CHECKER.location_reference_signature(self.data["locations"][0])

    def check(self):
        (self.project / "docs/location-continuity.json").write_text(json.dumps(self.data))
        (self.project / "game/closing_theme.json").write_text(json.dumps(self.theme))
        with contextlib.redirect_stdout(io.StringIO()):
            CHECKER.check_location_continuity(self.assets)

    def test_current_review_passes(self):
        self.check()

    def test_changed_pixels_need_new_visual_review(self):
        self.assets[self.name]["sha256"] = "replacement-pixels"
        with self.assertRaisesRegex(AssertionError, "Changed image needs visual location review"):
            self.check()

    def test_changed_building_reference_invalidates_dependent_review(self):
        (self.repository / "author-reference.png").write_bytes(b"a different building")
        with self.assertRaisesRegex(AssertionError, "Location reference changed; dependent image needs visual review"):
            self.check()

    def test_open_issue_blocks_even_if_asset_is_marked_consistent(self):
        self.data["issues"] = [{"id": "TH-01", "file": self.name, "status": "open"}]
        self.data["assets"][0]["findings"] = ["TH-01"]
        with self.assertRaisesRegex(AssertionError, "Open location issue TH-01"):
            self.check()

    def test_new_recurring_view_must_be_registered(self):
        (self.project / "game/images/backgrounds/treehouse-new.png").write_bytes(b"new angle")
        with self.assertRaisesRegex(AssertionError, "Unreviewed recurring-location image"):
            self.check()

    def test_changed_theme_assignment_needs_review(self):
        self.theme["shots"][0]["at"] = 15
        with self.assertRaisesRegex(AssertionError, "Changed theme use needs location review"):
            self.check()

    def test_changed_source_anchor_needs_review(self):
        (self.repository / "story.md").write_text("The place has been rewritten.")
        with self.assertRaisesRegex(AssertionError, "Changed source passage needs location review"):
            self.check()


if __name__ == "__main__":
    unittest.main()
