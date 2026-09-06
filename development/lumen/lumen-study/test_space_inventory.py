"""Exercise omissions and source drift that would invalidate the spatial audit.

Run: python3 -m unittest discover -s development/lumen/lumen-study -p 'test_*.py'
These tests verify the register's warning behavior, not completeness of canon.
"""
import copy
import json
import unittest
from unittest.mock import patch

import space_inventory as inventory


class InventoryCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(inventory.DATA.read_text())

    def errors_with_text_change(self, path, change):
        original = inventory.read

        def read(root, name):
            content = original(root, name)
            return change(content) if name == path else content

        with patch.object(inventory, "read", side_effect=read):
            return inventory.check(self.data)

    def test_current_evidence_and_generated_reference_agree(self):
        self.assertEqual(inventory.check(self.data), [])
        self.assertEqual(inventory.render(self.data), inventory.PAGE.read_text())

    def test_omitted_workshop_breaks_scene_and_image_coverage(self):
        data = copy.deepcopy(self.data)
        data["spaces"] = [s for s in data["spaces"] if s["id"] != "arin_workshop"]
        errors = inventory.check(data)
        self.assertTrue(any("Scene " in e and "missing space arin_workshop" in e for e in errors))
        self.assertTrue(any("Image refers to missing space arin_workshop" in e for e in errors))

    def test_omitted_scene_is_detected_from_runtime_registry(self):
        data = copy.deepcopy(self.data)
        data["scenes"].pop()
        self.assertIn("Scene coverage/order/titles differ from BOOK_SCENES", inventory.check(data))

    def test_source_change_requires_reading_even_when_anchors_survive(self):
        errors = self.errors_with_text_change(
            "visual-novel/game/family_book_one.rpy", lambda text: text + "\n# new spatial information\n")
        self.assertTrue(any("Re-read changed source" in e for e in errors))
        self.assertFalse(any("Missing anchor" in e for e in errors))

    def test_new_narrative_image_is_reported_as_unmapped(self):
        errors = self.errors_with_text_change(
            "visual-novel/game/script.rpy", lambda text: text + "\n    scene bg new_place\n")
        self.assertIn("Unmapped narrative images: bg new_place", errors)

    def test_new_closing_theme_location_is_reported(self):
        def add_shot(text):
            data = json.loads(text)
            data["shots"].append({"image": "images/new-place.png"})
            return json.dumps(data)

        errors = self.errors_with_text_change("visual-novel/game/closing_theme.json", add_shot)
        self.assertIn("Unmapped closing-theme images: visual-novel/game/images/new-place.png", errors)

    def test_reassigned_workshop_image_is_detected(self):
        data = copy.deepcopy(self.data)
        workshop = next(a for a in data["assets"] if "bg workshop" in a["aliases"])
        workshop["aliases"] = ["bg different_workshop"]
        self.assertIn("Image definitions changed or include an unregistered background/CG", inventory.check(data))

    def test_later_book_change_does_not_claim_book_one_is_stale(self):
        errors = self.errors_with_text_change("revision/latest.md", lambda text: text + "\nLater-book addition.\n")
        self.assertEqual(errors, [])

    def test_household_query_retains_work_and_private_uses(self):
        ids = {s["id"] for s in inventory.select(self.data, group="Household")}
        self.assertTrue({"arin_workshop", "selene_music", "dorian_library", "sage_room", "adult_retreats", "kitchen"} <= ids)
        self.assertEqual(inventory.select(self.data, id="nonexistent_room"), [])


if __name__ == "__main__":
    unittest.main()
