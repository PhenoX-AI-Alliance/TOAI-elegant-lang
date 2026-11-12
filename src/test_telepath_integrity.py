import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"

    def test_directories_exist(self):
        src_dir = os.path.join(self.base_dir, "src")
        self.assertTrue(os.path.isdir(src_dir), f"Directory missing: {src_dir}")

    def test_sample_files_or_spec(self):
        src_dir = os.path.join(self.base_dir, "src")
        files = os.listdir(src_dir)
        self.assertGreaterEqual(len(files), 1, "Source directory is empty.")

    def test_syntax_integrity(self):
        src_dir = os.path.join(self.base_dir, "src")
        for filename in os.listdir(src_dir):
            if filename.endswith(".py"):
                filepath = os.path.join(src_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                try:
                    compile(content, filepath, "exec")
                except SyntaxError as e:
                    self.fail(f"Syntax error in {filepath}: {e}")

if __name__ == "__main__":
    unittest.main()
