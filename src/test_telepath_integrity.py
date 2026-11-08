import sys
import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"
        self.dict_file = os.path.join(self.base_dir, "telepath_dict.json")
        self.spec_file = os.path.join(self.base_dir, "telepath_spec.md")
        self.log_file = os.path.join(self.base_dir, "telepath_dialogue.log")

    def test_files_existence(self):
        self.assertTrue(os.path.exists(self.dict_file), f"Missing: {self.dict_file}")
        self.assertTrue(os.path.exists(self.spec_file), f"Missing: {self.spec_file}")
        self.assertTrue(os.path.exists(self.log_file), f"Missing: {self.log_file}")

    def test_dict_syntax(self):
        with open(self.dict_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)
        self.assertIn("version", data)
        self.assertIn("terms", data)

    def test_spec_not_empty(self):
        self.assertGreater(os.path.getsize(self.spec_file), 0)

    def test_log_not_empty(self):
        self.assertGreater(os.path.getsize(self.log_file), 0)

if __name__ == "__main__":
    unittest.main()
