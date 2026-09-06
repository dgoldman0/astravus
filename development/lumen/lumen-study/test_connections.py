"""Check omissions and route mistakes in the proposed local arrangement."""
import copy
import json
import unittest

import build_connections as connections
import space_inventory as inventory


class ConnectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proposal = json.loads(connections.DATA.read_text())
        cls.sources = json.loads(inventory.DATA.read_text())

    def test_current_proposal_and_generated_pages_agree(self):
        self.assertEqual(connections.validate(self.proposal, self.sources), [])
        for path, content in connections.outputs(self.proposal, self.sources).items():
            self.assertEqual(path.read_text(), content, path.name)

    def test_omitted_workshop_disposition_is_named(self):
        proposal = copy.deepcopy(self.proposal)
        proposal["allocations"] = [a for a in proposal["allocations"] if a["space_id"] != "arin_workshop"]
        self.assertTrue(any("arin_workshop" in e and "disposition" in e for e in connections.validate(proposal, self.sources)))

    def test_private_provision_cannot_drop_an_adult(self):
        proposal = copy.deepcopy(self.proposal)
        proposal["private_provision"] = [p for p in proposal["private_provision"] if p["resident"] != "Maia"]
        self.assertTrue(any("eight residents" in e for e in connections.validate(proposal, self.sources)))

    def test_workshop_route_cannot_use_sages_room_as_a_corridor(self):
        proposal = copy.deepcopy(self.proposal)
        walk = next(w for w in proposal["walkthroughs"] if w["scene_id"] == "workshop_first")
        walk["path"] = ["central_room", "home_halls", "sage_room", "home_halls", "arin_workshop"]
        errors = connections.validate(proposal, self.sources)
        self.assertTrue(any("crosses a private room" in e for e in errors))
        self.assertFalse(any("Undeclared route" in e for e in errors))

    def test_missing_garden_link_invalidates_carried_project_route(self):
        proposal = copy.deepcopy(self.proposal)
        proposal["edges"] = [e for e in proposal["edges"] if {e["a"], e["b"]} != {"maia_garden", "pond_bank"}]
        self.assertTrue(any("Undeclared route in waterwheel" in e for e in connections.validate(proposal, self.sources)))

    def test_shared_woodland_route_cannot_depend_on_private_refuge(self):
        proposal = copy.deepcopy(self.proposal)
        proposal["edges"] = [e for e in proposal["edges"] if {e["a"], e["b"]} != {"community_routes", "local_landscape"}]
        self.assertTrue(any("bypassing household/private refuge" in e for e in connections.validate(proposal, self.sources)))


if __name__ == "__main__":
    unittest.main()
