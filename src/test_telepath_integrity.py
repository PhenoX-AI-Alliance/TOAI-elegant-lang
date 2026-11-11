import os
import sys
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_exist(self):
        self.assertTrue(os.path.exists(self.base_dir), f"Base directory does not exist: {self.base_dir}")
        self.assertTrue(os.path.exists(self.src_dir), f"Source directory does not exist: {self.src_dir}")

    def test_files_syntax_and_existence(self):
        # Check for any python files in src and ensure they parse correctly
        if os.path.exists(self.src_dir):
            for filename in os.listdir(self.src_dir):
                if filename.endswith(".py"):
                    filepath = os.path.join(self.src_dir, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    try:
                        compile(content, filepath, 'exec')
                    except SyntaxError as e:
                        self.fail(f"Syntax error in {filepath}: {e}")

if __name__ == '__main__':
    unittest.main()
