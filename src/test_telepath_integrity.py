import unittest
import os
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"

    def test_directories_and_files_exist(self):
        src_dir = os.path.join(self.base_dir, "src")
        self.assertTrue(os.path.exists(src_dir), "src directory must exist.")

    def test_syntax_integrity(self):
        src_dir = os.path.join(self.base_dir, "src")
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    try:
                        compile(content, file_path, "exec")
                    except SyntaxError as e:
                        self.fail(f"Syntax error in {file_path}: {e}")

if __name__ == "__main__":
    unittest.main()
