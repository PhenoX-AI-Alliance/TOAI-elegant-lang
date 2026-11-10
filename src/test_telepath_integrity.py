import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")
        
    def test_directory_exists(self):
        self.assertTrue(os.path.exists(self.src_dir), f"Source directory does not exist: {self.src_dir}")

    def test_syntax_of_python_files(self):
        for root, dirs, files in os.walk(self.src_dir):
            for file in files:
                if file.endswith(".py") and file != "test_telepath_integrity.py":
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    try:
                        compile(content, file_path, "exec")
                    except SyntaxError as e:
                        self.fail(f"Syntax error in {file_path}: {e}")

    def test_required_assets(self):
        dict_path = os.path.join(self.base_dir, "dictionary.json")
        spec_path = os.path.join(self.base_dir, "specification.md")
        log_path = os.path.join(self.base_dir, "dialogue_log.json")
        
        for path in [dict_path, spec_path, log_path]:
            if os.path.exists(path):
                if path.endswith(".json"):
                    with open(path, "r", encoding="utf-8") as f:
                        try:
                            json.load(f)
                        except json.JSONDecodeError as e:
                            self.fail(f"Invalid JSON format in {path}: {e}")
            else:
                pass

if __name__ == "__main__":
    unittest.main()
