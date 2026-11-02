import sys
import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_dictionary_existence(self):
        dict_path = os.path.join(self.src_dir, "dictionary.json")
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, (dict, list))

    def test_specification_existence(self):
        spec_path = os.path.join(self.base_dir, "SPECIFICATION.md")
        if os.path.exists(spec_path):
            self.assertTrue(os.path.getsize(spec_path) >= 0)

    def test_dialogue_log_integrity(self):
        log_path = os.path.join(self.src_dir, "dialogue_log.json")
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
            self.assertIsInstance(logs, list)

if __name__ == "__main__":
    unittest.main()
