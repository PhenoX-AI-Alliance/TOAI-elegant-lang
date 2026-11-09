import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"

    def test_directory_exists(self):
        self.assertTrue(os.path.isdir(self.base_dir), f"Base directory does not exist: {self.base_dir}")

    def test_files_presence_and_syntax(self):
        src_dir = os.path.join(self.base_dir, "src")
        self.assertTrue(os.path.isdir(src_dir), f"Source directory does not exist: {src_dir}")
        
        # Check if there are python files or json files to validate
        files = os.listdir(src_dir)
        self.assertGreaterEqual(len(files), 1, "Source directory is empty.")

        for f in files:
            if f.endswith(".json"):
                file_path = os.path.join(src_dir, f)
                with open(file_path, "r", encoding="utf-8") as file_obj:
                    try:
                        data = json.load(file_obj)
                        self.assertIsInstance(data, (dict, list), f"JSON file {f} root must be dict or list.")
                    except json.JSONDecodeError as jde:
                        self.fail(f"JSON syntax error in {f}: {jde}")

            elif f.endswith(".py") and f != "test_telepath_integrity.py":
                file_path = os.path.join(src_dir, f)
                with open(file_path, "r", encoding="utf-8") as file_obj:
                    content = file_obj.read()
                    try:
                        compile(content, file_path, "exec")
                    except SyntaxError as se:
                        self.fail(f"Python syntax error in {f}: {se}")

if __name__ == "__main__":
    unittest.main()
