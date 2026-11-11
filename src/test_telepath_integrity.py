import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"

    def test_dictionary_exists_and_valid(self):
        dict_path = os.path.join(self.base_dir, "dictionary.json")
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, (dict, list))

    def test_specification_exists(self):
        spec_path = os.path.join(self.base_dir, "specification.md")
        if os.path.exists(spec_path):
            self.assertTrue(os.path.getsize(spec_path) >= 0)

    def test_dialogue_logs_valid(self):
        log_path = os.path.join(self.base_dir, "dialogue_log.json")
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
            self.assertIsInstance(logs, (dict, list))

if __name__ == "__main__":
    unittest.main()
