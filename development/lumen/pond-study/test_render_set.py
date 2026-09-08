"""Regression checks for the mixed-revision preview failure."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from check_render_set import HERE,verify_artifacts


class RenderSetTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='pond-set-test-')
        self.here=Path(self.temp.name)
        self.manifest=json.loads((HERE/'render-manifest.json').read_text())
        build=self.manifest['build_id']
        shutil.copytree(HERE/'builds'/build,self.here/'builds'/build)
        for name in ('render-manifest.json','render-manifest.js'):
            shutil.copyfile(HERE/name,self.here/name)
        (self.here/'pond-study.blend').symlink_to(self.manifest['blend']['path'])
        (self.here/'renders').symlink_to(Path('builds')/build/'renders')

    def tearDown(self):self.temp.cleanup()

    def test_complete_matching_set(self):
        self.assertEqual(verify_artifacts(self.here)['build_id'],self.manifest['build_id'])

    def test_replacing_overview_with_another_view_fails(self):
        views=self.manifest['views']
        shutil.copyfile(self.here/views['pond']['path'],self.here/views['overview']['path'])
        with self.assertRaisesRegex(ValueError,'overview file hash differs'):
            verify_artifacts(self.here)

    def test_missing_view_fails(self):
        (self.here/self.manifest['views']['overview']['path']).unlink()
        with self.assertRaises(FileNotFoundError):verify_artifacts(self.here)


if __name__=='__main__':unittest.main()
