import unittest
import os
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.dict_path = os.path.join(self.base_dir, "dict", "telepath_dict.json")
        self.spec_path = os.path.join(self.base_dir, "specs", "telepath_spec.md")
        self.log_path = os.path.join(self.base_dir, "logs", "dialogue_history.json")

    def test_files_exist(self):
        self.assertTrue(os.path.exists(self.dict_path), f"Missing dict at {self.dict_path}")
        self.assertTrue(os.path.exists(self.spec_path), f"Missing spec at {self.spec_path}")
        self.assertTrue(os.path.exists(self.log_path), f"Missing logs at {self.log_path}")

    def test_dict_syntax(self):
        with open(self.dict_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)

    def test_log_syntax(self):
        with open(self.log_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, list)

if __name__ == "__main__":
    unittest.main()
