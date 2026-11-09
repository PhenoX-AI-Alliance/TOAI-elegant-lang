import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"

    def test_directory_structure(self):
        self.assertTrue(os.path.exists(self.base_dir), "Base directory does not exist.")

    def test_files_existence_and_syntax(self):
        src_dir = os.path.join(self.base_dir, "src")
        self.assertTrue(os.path.isdir(src_dir), "src directory does not exist.")
        
        # Check potential dictionary, specification, or log files if they exist
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(".json"):
                    json_path = os.path.join(root, file)
                    with open(json_path, "r", encoding="utf-8") as f:
                        try:
                            json.load(f)
                        except json.JSONDecodeError as e:
                            self.fail(f"JSON file {json_path} is syntactically broken: {e}")
                elif file.endswith(".py"):
                    py_path = os.path.join(root, file)
                    with open(py_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        try:
                            compile(content, py_path, "exec")
                        except SyntaxError as e:
                            self.fail(f"Python file {py_path} has syntax error: {e}")

if __name__ == "__main__":
    unittest.main()
