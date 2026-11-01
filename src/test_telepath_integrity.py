import sys
import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"

    def test_directories_exist(self):
        src_dir = os.path.join(self.base_dir, "src")
        self.assertTrue(os.path.exists(src_dir), "Source directory must exist")

    def test_syntax_integrity(self):
        src_dir = os.path.join(self.base_dir, "src")
        if os.path.exists(src_dir):
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
