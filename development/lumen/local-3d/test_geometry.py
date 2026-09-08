"""Blender regression checks: blender --background --python test_geometry.py."""

from pathlib import Path
import sys
import unittest

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_geometry import validate


class GeometryValidationTests(unittest.TestCase):
    def setUp(self):
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=False)
        self.floor = self.box("Floor", (0, 0, -0.1), (8, 4, 0.2), "walk_surface")
        self.spec = {"routes": [{"id": "walk", "title": "Cross the room",
                                 "points": [[-2, 0, 0], [2, 0, 0]], "radius": 0.35, "height": 1.8}]}

    def box(self, name, location, dimensions, tag):
        bpy.ops.mesh.primitive_cube_add(size=1, location=location)
        obj = bpy.context.object
        obj.name, obj.dimensions = name, dimensions
        obj[tag] = True
        return obj

    def check(self, spec=None):
        return validate(bpy.context.scene, spec or self.spec)["checks"][0]

    def test_moved_hidden_obstruction_changes_route_result(self):
        obstacle = self.box("Moved bench", (0, 3, 0.8), (1.2, 0.8, 1.6), "collision")
        obstacle.hide_render = True
        self.assertEqual(self.check()["status"], "pass")
        obstacle.location.y = 0
        check = self.check()
        self.assertEqual(check["status"], "fail")
        self.assertEqual(check["metrics"]["collision_failure"]["object"], "Moved bench")
        self.assertIsNone(check["metrics"]["support_failure"])

    def test_removing_floor_support_fails(self):
        self.assertEqual(self.check()["status"], "pass")
        bpy.data.objects.remove(self.floor, do_unlink=True)
        check = self.check()
        self.assertEqual(check["status"], "fail")
        self.assertIsNotNone(check["metrics"]["support_failure"])

    def test_real_geometry_blocks_sightline(self):
        spec = {"sightlines": [{"id": "look", "title": "View through the room",
                                "from": [-2, 0, 1], "to": [2, 0, 1]}]}
        self.assertEqual(self.check(spec)["status"], "pass")
        self.box("Intervening wall", (0, 0, 1.5), (0.3, 3, 3), "collision")
        check = self.check(spec)
        self.assertEqual(check["status"], "fail")
        self.assertEqual(check["metrics"]["obstruction"]["object"], "Intervening wall")


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(GeometryValidationTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
