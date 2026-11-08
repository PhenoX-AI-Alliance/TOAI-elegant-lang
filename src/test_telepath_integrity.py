import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")
        
    def test_directory_structure(self):
        self.assertTrue(os.path.exists(self.base_dir), f"Base directory does not exist: {self.base_dir}")
        self.assertTrue(os.path.exists(self.src_dir), f"Source directory does not exist: {self.src_dir}")

    def test_files_existence_and_syntax(self):
        # Check for dictionary, specification, or conversation logs if any
        # Here we assert integrity of python files and data files in src
        for root, dirs, files in os.walk(self.src_dir):
            for file in files:
                full_path = os.path.join(root, file)
                if file.endswith(".py") and file != "test_telepath_integrity.py":
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    try:
                        compile(content, full_path, "exec")
                    except SyntaxError as e:
                        self.fail(f"Syntax error in {full_path}: {e}")
                elif file.endswith(".json"):
                    with open(full_path, "r", encoding="utf-8") as f:
                        try:
                            json.load(f)
                        except json.JSONDecodeError as e:
                            self.fail(f"JSON decode error in {full_path}: {e}")

if __name__ == "__main__":
    unittest.main()
