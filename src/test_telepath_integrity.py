import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.dict_path = os.path.join(self.base_dir, "data", "dictionary.json")
        self.spec_path = os.path.join(self.base_dir, "docs", "specification.md")
        self.log_path = os.path.join(self.base_dir, "logs", "dialogue_log.jsonl")

    def test_file_existence(self):
        self.assertTrue(os.path.exists(self.dict_path), f"Missing required file: {self.dict_path}")
        self.assertTrue(os.path.exists(self.spec_path), f"Missing required file: {self.spec_path}")
        self.assertTrue(os.path.exists(self.log_path), f"Missing required file: {self.log_path}")

    def test_dictionary_syntax(self):
        with open(self.dict_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)
        self.assertIn("telepath", data)

    def test_log_syntax(self):
        with open(self.log_path, "r", encoding="utf-8") as f:
            line = f.readline()
        record = json.loads(line)
        self.assertIsInstance(record, dict)
        self.assertIn("message", record)

if __name__ == "__main__":
    unittest.main()
