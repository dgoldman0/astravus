"""Boundary tests for the glossary's actual reading-local selector."""
import json
from pathlib import Path
import re
import sys
import unittest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "game"))
sys.path.insert(0, str(PROJECT / "scripts"))
from glossary_rules import revealed_glossary
from check_glossary import validate_glossary

ENTRIES = json.loads((PROJECT / "game/glossary.json").read_text())["entries"]
SCENES = tuple(re.findall(r'^        \("([a-z_]+)", ', (PROJECT / "game/book_structure.rpy").read_text(), re.M))
BY_ID = {entry["id"]: entry for entry in ENTRIES}


def knowledge(scene="first_memory", visited=(), history=()):
    return revealed_glossary(ENTRIES, SCENES, scene, visited, history)


class GlossaryTests(unittest.TestCase):
    def test_source_and_exact_script_cues(self):
        self.assertEqual(validate_glossary(), {"entries": 9, "reveal_stages": 11, "status": "pass"})

    def test_fresh_beginning_has_no_titles(self):
        self.assertEqual(knowledge(visited=["first_memory"]), {})

    def test_each_cue_unlocks_only_when_displayed(self):
        for entry in ENTRIES:
            for level, stage in enumerate(entry["stages"]):
                with self.subTest(term=entry["id"], level=level):
                    before = knowledge(stage["scene"], [stage["scene"]])
                    self.assertNotIn(entry["id"], before)
                    after = knowledge(stage["scene"], [stage["scene"]], [stage["cue"]])
                    self.assertEqual(after[entry["id"]]["level"], level)
                    self.assertEqual(after[entry["id"]]["description"], stage["description"])

    def test_rollback_removes_revelation_and_restores_earlier_definition(self):
        initial, reveal = BY_ID["lumen"]["stages"]
        prefix = SCENES[:SCENES.index("tree_echoes")]
        self.assertEqual(knowledge("tree_echoes", prefix, [reveal["cue"]])["lumen"]["level"], 1)
        rolled = knowledge("tree_echoes", prefix)
        self.assertEqual(rolled["lumen"]["description"], initial["description"])
        self.assertNotIn("living", rolled["lumen"]["description"])

    def test_jump_into_loss_does_not_reveal_destination_terms(self):
        prefix = SCENES[:SCENES.index("loss")]
        start = knowledge("loss", prefix)
        self.assertNotIn("astraviin", start)
        self.assertNotIn("transcendence", start)
        self.assertEqual(start["lumen"]["level"], 1)

    def test_backwards_jump_and_early_save_remove_later_knowledge(self):
        late = knowledge("annual_remembrance", SCENES[:-1])
        self.assertEqual(set(late), set(BY_ID))
        early = knowledge("music_first", SCENES[:4])
        self.assertEqual(set(early), {"first_breath", "sanctuary", "lumen", "familiar", "constellation"})
        self.assertEqual(early["lumen"]["level"], 0)
        self.assertEqual(knowledge(), {})

    def test_shortened_old_save_history_recovers_completed_scenes(self):
        result = knowledge("pond_scare", SCENES[:9])
        self.assertEqual(result["lumen"]["level"], 1)
        self.assertEqual(result["tree_of_echoes"]["level"], 1)
        self.assertNotIn("transcendence", result)

    def test_future_history_cannot_override_current_scene(self):
        future = [stage["cue"] for entry in ENTRIES for stage in entry["stages"] if stage["scene"] != "first_memory"]
        self.assertEqual(knowledge(history=future), {})

    def test_early_definitions_do_not_explain_future_mechanics(self):
        for key in ("first_breath", "sanctuary", "familiar", "constellation", "lumen"):
            text = BY_ID[key]["stages"][0]["description"].lower()
            for future in ("transcenden", "core", "living ship", "astraviin", "joren", "death", "longevity"):
                self.assertNotIn(future, text)
        self.assertIn("romantic partnership among adults", BY_ID["constellation"]["stages"][0]["description"])


if __name__ == "__main__":
    unittest.main()
