import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_exist(self):
        self.assertTrue(os.path.isdir(self.base_dir), "Base directory does not exist.")
        self.assertTrue(os.path.isdir(self.src_dir), "Src directory does not exist.")

    def test_syntax_of_py_files(self):
        for root, dirs, files in os.walk(self.src_dir):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    try:
                        compile(content, full_path, "exec")
                    except SyntaxError as e:
                        self.fail(f"Syntax error in {full_path}: {e}")

    def test_optional_assets(self):
        dict_path = os.path.join(self.base_dir, "dictionary.json")
        spec_path = os.path.join(self.base_dir, "specification.md")
        log_path = os.path.join(self.base_dir, "dialogue_log.json")

        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.assertIsInstance(data, (dict, list))
                except Exception as e:
                    self.fail(f"Dictionary file is not valid JSON: {e}")

        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.assertIsInstance(data, (dict, list))
                except Exception as e:
                    self.fail(f"Dialogue log is not valid JSON: {e}")

if __name__ == "__main__":
    unittest.main()
