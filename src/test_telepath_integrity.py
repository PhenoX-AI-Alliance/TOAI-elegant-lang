import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"

    def test_directories_and_files_existence(self):
        self.assertTrue(os.path.exists(self.base_dir), f"Base directory does not exist: {self.base_dir}")

    def test_dictionary_files(self):
        dict_path = os.path.join(self.base_dir, "dictionary.json")
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, (dict, list), "Dictionary file content must be valid JSON object or list.")

    def test_specifications(self):
        spec_path = os.path.join(self.base_dir, "specification.md")
        if os.path.exists(spec_path):
            with open(spec_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertGreater(len(content), 0, "Specification file should not be empty.")

    def test_dialogue_logs(self):
        log_path = os.path.join(self.base_dir, "dialogue_log.json")
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
            self.assertIsInstance(logs, (dict, list), "Dialogue logs must be valid JSON.")

if __name__ == "__main__":
    unittest.main()
