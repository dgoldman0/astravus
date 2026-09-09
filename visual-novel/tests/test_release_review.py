"""A release receipt must not stay green after its inputs or evidence change."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("release_review", Path(__file__).parents[1] / "scripts/release_review.py")
review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review)


class ReviewEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "visual-novel"
        self.root.mkdir()
        self.addCleanup(patch.stopall)
        patch.object(review, "PROJECT", self.root).start()
        (self.root / "input.txt").write_text("selected source")
        (self.root / "review.md").write_text("Actual inspection notes")
        self.matrix = {"input_groups": {"sources": ["input*.txt"]}}
        self.row = {"id": "visual", "method": "manual", "input_groups": ["sources"],
                    "acceptance": ["Face and scene quality match references"]}
        self.receipt = {"input_sha256": review.digest(review.snapshot(self.matrix, self.row)),
                        "method": "manual", "outcome": "pass", "notes": "Inspected image and comparison",
                        "evidence": review.evidence_hashes(["review.md"])}

    def state(self):
        return review.check_status(self.matrix, self.row, {"visual": self.receipt})[0]

    def test_current_explicit_manual_review_passes(self):
        self.assertEqual(self.state(), "PASS")

    def test_changed_source_invalidates_review(self):
        (self.root / "input.txt").write_text("redrawn face")
        self.assertEqual(self.state(), "STALE")

    def test_new_source_matching_scope_invalidates_review(self):
        (self.root / "input-new.txt").write_text("new selected scene")
        self.assertEqual(self.state(), "STALE")

    def test_changed_acceptance_invalidates_review(self):
        self.row["acceptance"].append("Eyes must remain deep green")
        self.assertEqual(self.state(), "STALE")

    def test_altered_evidence_invalidates_review(self):
        (self.root / "review.md").write_text("Different review of different art")
        self.assertEqual(self.state(), "STALE")

    def test_missing_evidence_invalidates_review(self):
        (self.root / "review.md").unlink()
        self.assertEqual(self.state(), "STALE")

    def test_development_evidence_and_comparison_remain_hash_bound(self):
        path = self.root.parent / "development/visual-novel/reviews/art.md"
        path.parent.mkdir(parents=True)
        path.write_text("Inspected source and native frame")
        name = "../development/visual-novel/reviews/art.md"
        self.receipt["evidence"] = review.evidence_hashes([name])
        self.receipt["comparison_reference"] = "file:" + name
        self.receipt["comparison_signature"] = review.comparison_signature("file:" + name)
        self.assertEqual(self.state(), "PASS")
        path.write_text("Different review")
        self.assertEqual(self.state(), "STALE")

    def test_review_paths_cannot_escape_allowed_workspaces(self):
        outside = self.root.parent / "unrelated.md"
        outside.write_text("Unrelated file")
        (self.root / "escape.md").symlink_to(outside)
        for name in ("../unrelated.md", "escape.md"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                review.evidence_hashes([name])
            with self.subTest(name=name), self.assertRaises(ValueError):
                review.comparison_signature("file:" + name)

    def test_hash_without_review_never_passes(self):
        self.assertEqual(review.check_status(self.matrix, self.row, {})[0], "PENDING")
        self.receipt["evidence"] = {}
        self.assertEqual(self.state(), "PENDING")

    def test_image_quality_needs_chosen_comparison(self):
        self.row["quality_dimensions"] = ["composition", "lighting", "anatomy"]
        self.receipt["input_sha256"] = review.digest(review.snapshot(self.matrix, self.row))
        self.assertEqual(self.state(), "PENDING")
        self.receipt["comparison_reference"] = "file:review.md"
        self.receipt["comparison_signature"] = review.comparison_signature("file:review.md")
        self.assertEqual(self.state(), "PASS")

    def test_changed_comparison_invalidates_quality_review(self):
        (self.root / "reference.png").write_bytes(b"approved reference pixels")
        self.receipt["comparison_reference"] = "file:reference.png"
        self.receipt["comparison_signature"] = review.comparison_signature("file:reference.png")
        self.assertEqual(self.state(), "PASS")
        (self.root / "reference.png").write_bytes(b"different facial proportions")
        self.assertEqual(self.state(), "STALE")

    def test_comparison_cannot_be_an_unresolved_label(self):
        with self.assertRaises(ValueError):
            review.comparison_signature("some previous picture")

    def test_explicit_author_rejection_stays_failed(self):
        self.receipt["outcome"] = "fail"
        self.receipt["notes"] = "Author rejected loss of detail and expression."
        self.assertEqual(self.state(), "FAIL")

    def test_automated_check_needs_successful_command(self):
        self.row["method"] = "automated"
        self.receipt["method"] = "automated"
        self.receipt["input_sha256"] = review.digest(review.snapshot(self.matrix, self.row))
        self.assertEqual(self.state(), "FAIL")
        self.receipt["returncode"] = 0
        self.assertEqual(self.state(), "PASS")

    def test_temporary_build_cannot_supply_candidate_evidence(self):
        self.row["candidate_builds"] = ["web"]
        (self.root / "build").mkdir()
        artifact = self.root / "build/web.zip"
        artifact.write_bytes(b"compiled runtime")
        stamp = self.root / "build/release-builds.json"
        record = {"kind": "review", "files": {"build/web.zip": review.file_digest(artifact)}}
        stamp.write_text(json.dumps({"builds": {"web": record}}))
        self.assertFalse(review.candidate_builds_ready(self.row))
        record["kind"] = "candidate"
        stamp.write_text(json.dumps({"builds": {"web": record}}))
        self.assertTrue(review.candidate_builds_ready(self.row))
        artifact.write_bytes(b"stale replacement")
        self.assertFalse(review.candidate_builds_ready(self.row))


if __name__ == "__main__":
    unittest.main()
