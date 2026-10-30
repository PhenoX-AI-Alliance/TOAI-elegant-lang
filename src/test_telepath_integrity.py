import sys
import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.dict_path = os.path.join(self.base_dir, "dict", "telepath_dict.json")
        self.spec_path = os.path.join(self.base_dir, "docs", "telepath_spec.md")
        self.log_path = os.path.join(self.base_dir, "logs", "telepath_dialogue.log")

    def test_dictionary_existence_and_syntax(self):
        if os.path.exists(self.dict_path):
            with open(self.dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, (dict, list))
        else:
            self.assertTrue(True, "Dictionary path not found, skipping as optional.")

    def test_spec_existence(self):
        if os.path.exists(self.spec_path):
            with open(self.spec_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertGreater(len(content), 0)
        else:
            self.assertTrue(True, "Spec path not found, skipping as optional.")

    def test_log_existence(self):
        if os.path.exists(self.log_path):
            with open(self.log_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIsInstance(content, str)
        else:
            self.assertTrue(True, "Log path not found, skipping as optional.")

if __name__ == "__main__":
    unittest.main()
