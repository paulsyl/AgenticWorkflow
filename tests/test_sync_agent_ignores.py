import os
import shutil
import tempfile
import unittest

from scripts.sync_agent_ignores import (
    BEGIN_SENTINEL,
    END_SENTINEL,
    TARGET_FILES,
    merge_sentinel_block,
    sync_ignores,
)

class TestSyncAgentIgnores(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_creates_master_ignore_and_target_files(self):
        sync_ignores(self.test_dir)
        master_path = os.path.join(self.test_dir, ".agentignore")
        self.assertTrue(os.path.exists(master_path))

        for target in TARGET_FILES:
            target_path = os.path.join(self.test_dir, target)
            self.assertTrue(os.path.exists(target_path), f"Target {target} should exist")
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(BEGIN_SENTINEL, content)
            self.assertIn(END_SENTINEL, content)
            self.assertIn("*.png", content)
            self.assertIn("node_modules/", content)

    def test_idempotency(self):
        sync_ignores(self.test_dir)
        target_path = os.path.join(self.test_dir, ".antigravityignore")
        with open(target_path, "r", encoding="utf-8") as f:
            first_content = f.read()

        sync_ignores(self.test_dir)
        with open(target_path, "r", encoding="utf-8") as f:
            second_content = f.read()

        self.assertEqual(first_content, second_content)

    def test_non_destructive_merge_preserves_custom_rules(self):
        target_path = os.path.join(self.test_dir, ".antigravityignore")
        initial_custom = "# Custom rule before block\ncustom_file.txt\n"
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(initial_custom)

        sync_ignores(self.test_dir)
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertTrue(content.startswith("# Custom rule before block"))
        self.assertIn(BEGIN_SENTINEL, content)
        self.assertIn("custom_file.txt", content)

    def test_nested_directory_creation(self):
        nested_target = os.path.join(self.test_dir, ".github", "copilot-ignore")
        self.assertFalse(os.path.exists(os.path.dirname(nested_target)))
        sync_ignores(self.test_dir)
        self.assertTrue(os.path.exists(nested_target))

if __name__ == "__main__":
    unittest.main()
