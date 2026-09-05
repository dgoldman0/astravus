"""Baked figure reviews cannot carry over after art/reference/contract changes."""
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


class CGCharacterReviewGuard(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repository = Path(self.temp.name)
        self.project = self.repository / "visual-novel"
        (self.project / "docs").mkdir(parents=True)
        (self.project / "game/images/cg").mkdir(parents=True)
        (self.project / "game/images/characters").mkdir(parents=True)
        self.cg = "game/images/cg/group.png"
        self.sprite = "game/images/characters/calista.png"
        (self.project / self.cg).write_bytes(b"CG fixture")
        (self.project / self.sprite).write_bytes(b"character reference")
        (self.repository / "Calista.md").write_text("Calista has deep blue eyes.")
        (self.project / "game/character_layout.json").write_text('{"calista_early": 675}')
        self.assets = {self.cg: {"sha256": "reviewed-CG"}, self.sprite: {"sha256": "sprite"}}
        self.data = {
            "schema_version": 1,
            "relative_height_production_contract": {"file": "game/character_layout.json"},
            "review_policy": {"passing_statuses": ["consistent", "consistent_crop"]},
            "characters": [{"id": "Calista", "wiki": "../Calista.md", "wiki_anchors": ["deep blue"],
                            "specs": ["Deep blue eyes."], "stage_references": {"early": [self.sprite]}}],
            "issues": [],
            "assets": [{"file": self.cg, "cast": [{"character": "Calista", "stage": "early"}],
                        "review_status": "consistent", "reviewed_sha256": "reviewed-CG", "findings": [],
                        "face_review": {"status": "accepted", "method": "Crops beside stage reference",
                                        "checks": ["facial_anatomy", "iris_pigment_and_light", "stage_identity", "reference_comparison"],
                                        "notes": "Natural blue iris pigment and the reference facial structure are retained."}}],
        }
        self.patch = patch.multiple(CHECKER, PROJECT=self.project, REPOSITORY=self.repository)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.data["assets"][0]["reviewed_reference_signature"] = CHECKER.cg_reference_signature(self.data, self.data["assets"][0])

    def check(self):
        (self.project / "docs/cg-character-review.json").write_text(json.dumps(self.data))
        with contextlib.redirect_stdout(io.StringIO()):
            CHECKER.check_cg_characters(self.assets)

    def test_current_review_passes(self):
        self.check()

    def test_repainted_CG_needs_new_review(self):
        self.assets[self.cg]["sha256"] = "new-CG"
        with self.assertRaisesRegex(AssertionError, "Changed CG needs character scale/identity review"):
            self.check()

    def test_changed_identity_reference_needs_new_review(self):
        (self.project / self.sprite).write_bytes(b"new character proportions")
        with self.assertRaisesRegex(AssertionError, "Changed character reference or stature contract"):
            self.check()

    def test_changed_shared_height_contract_needs_new_review(self):
        (self.project / "game/character_layout.json").write_text('{"calista_early": 800}')
        with self.assertRaisesRegex(AssertionError, "Changed character reference or stature contract"):
            self.check()

    def test_changed_additional_face_reference_needs_new_review(self):
        reference = "game/images/characters/other-pose.png"
        (self.project / reference).write_bytes(b"facial shading reference")
        self.assets[reference] = {"sha256": "face-reference"}
        item = self.data["assets"][0]
        item["face_review"]["reference_files"] = [reference]
        item["reviewed_reference_signature"] = CHECKER.cg_reference_signature(self.data, item)
        (self.project / reference).write_bytes(b"changed facial anatomy")
        with self.assertRaisesRegex(AssertionError, "Changed character reference or stature contract"):
            self.check()

    def test_open_scale_issue_blocks_consistent_flag(self):
        self.data["issues"] = [{"id": "CG-01", "file": self.cg, "status": "open"}]
        self.data["assets"][0]["findings"] = ["CG-01"]
        with self.assertRaisesRegex(AssertionError, "Open CG character issue CG-01"):
            self.check()

    def test_new_CG_must_be_reviewed(self):
        self.assets["game/images/cg/new-scene.png"] = {"sha256": "new-scene"}
        with self.assertRaisesRegex(AssertionError, "Unreviewed or missing CGs"):
            self.check()

    def test_stature_pass_does_not_substitute_for_face_review(self):
        del self.data["assets"][0]["face_review"]
        with self.assertRaisesRegex(AssertionError, "explicit face/iris review independent of stature"):
            self.check()

    def test_incomplete_face_checks_do_not_pass(self):
        self.data["assets"][0]["face_review"]["checks"].remove("iris_pigment_and_light")
        with self.assertRaisesRegex(AssertionError, "explicit face/iris review independent of stature"):
            self.check()

    def test_resolved_issue_requires_recorded_repair(self):
        self.data["issues"] = [{"id": "CG-01", "file": self.cg, "status": "resolved"}]
        self.data["assets"][0]["findings"] = ["CG-01"]
        with self.assertRaisesRegex(AssertionError, "Missing CG figure repair record"):
            self.check()


if __name__ == "__main__":
    unittest.main()
