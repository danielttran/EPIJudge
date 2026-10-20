"""Exercise startup on real clean directories without touching saved evidence."""
import tempfile
import unittest
from pathlib import Path

from verify_blind75_http import create_run_directory


class RunDirectoryTests(unittest.TestCase):
    def test_clean_checkout_creates_its_artifact_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertFalse((root / '.epi-runs').exists())
            run = create_run_directory(root)
            self.assertTrue(run.is_dir())
            self.assertEqual(root / '.epi-runs', run.parent)
            self.assertTrue(run.name.startswith('blind75-http-'))

    def test_repeated_runs_preserve_existing_evidence_and_use_unique_profiles(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifacts = root / '.epi-runs'
            artifacts.mkdir()
            evidence = artifacts / 'saved-evidence.json'
            evidence.write_bytes(b'{"preserve":true}\n')
            first = create_run_directory(root)
            second = create_run_directory(root)
            self.assertNotEqual(first, second)
            self.assertTrue(first.is_dir() and second.is_dir())
            self.assertEqual(b'{"preserve":true}\n', evidence.read_bytes())

    def test_absent_parent_directories_are_created(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'new' / 'checkout'
            run = create_run_directory(root)
            self.assertTrue(run.is_dir())
            self.assertEqual(root / '.epi-runs', run.parent)

    def test_conflicting_file_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            existing = root / '.epi-runs'
            existing.write_bytes(b'keep this file')
            with self.assertRaises(FileExistsError):
                create_run_directory(root)
            self.assertEqual(b'keep this file', existing.read_bytes())


if __name__ == '__main__':
    unittest.main()
