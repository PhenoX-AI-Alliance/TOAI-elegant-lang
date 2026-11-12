import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_exist(self):
        self.assertTrue(os.path.isdir(self.base_dir), f"Base directory does not exist: {self.base_dir}")
        self.assertTrue(os.path.isdir(self.src_dir), f"Source directory does not exist: {self.src_dir}")

    def test_dictionary_and_specs(self):
        dict_path = os.path.join(self.base_dir, "dictionary.json")
        spec_path = os.path.join(self.base_dir, "spec.md")
        logs_path = os.path.join(self.base_dir, "dialogue_logs.json")

        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIsInstance(data, (dict, list), "Dictionary file is not valid JSON object or list.")

        if os.path.exists(logs_path):
            with open(logs_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
                self.assertIsInstance(logs, (dict, list), "Dialogue logs file is not valid JSON object or list.")

        if os.path.exists(spec_path):
            with open(spec_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertGreater(len(content), 0, "Specification file is empty.")

if __name__ == "__main__":
    unittest.main()
