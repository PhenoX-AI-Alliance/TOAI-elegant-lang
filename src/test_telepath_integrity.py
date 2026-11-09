import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_exist(self):
        self.assertTrue(os.path.exists(self.base_dir), "Base directory missing")
        self.assertTrue(os.path.exists(self.src_dir), "Source directory missing")

    def test_syntax_of_source_files(self):
        if not os.path.exists(self.src_dir):
            return
        for filename in os.listdir(self.src_dir):
            if filename.endswith(".py"):
                filepath = os.path.join(self.src_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                try:
                    compile(content, filepath, "exec")
                except SyntaxError as e:
                    self.fail(f"Syntax error in {filename}: {e}")

if __name__ == "__main__":
    unittest.main()
