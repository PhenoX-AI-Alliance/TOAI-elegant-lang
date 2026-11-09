import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_exist(self):
        self.assertTrue(os.path.exists(self.base_dir), f"Base directory does not exist: {self.base_dir}")
        self.assertTrue(os.path.exists(self.src_dir), f"Source directory does not exist: {self.src_dir}")

    def test_syntax_of_python_files(self):
        if not os.path.exists(self.src_dir):
            self.skipTest("Source directory does not exist yet.")
        
        py_files = [f for f in os.listdir(self.src_dir) if f.endswith(".py")]
        for file_name in py_files:
            file_path = os.path.join(self.src_dir, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                compile(content, file_path, "exec")
            except SyntaxError as e:
                self.fail(f"Syntax error in {file_path}: {e}")

if __name__ == "__main__":
    unittest.main()
