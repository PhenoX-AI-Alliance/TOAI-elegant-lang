import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.spec_path = os.path.join(self.base_dir, "docs", "spec.json")
        self.dict_path = os.path.join(self.base_dir, "data", "telepath_dict.json")
        self.log_path = os.path.join(self.base_dir, "data", "dialogue_log.json")

    def test_files_exist(self):
        self.assertTrue(os.path.exists(self.spec_path), f"Spec file missing: {self.spec_path}")
        self.assertTrue(os.path.exists(self.dict_path), f"Dict file missing: {self.dict_path}")
        self.assertTrue(os.path.exists(self.log_path), f"Log file missing: {self.log_path}")

    def test_json_syntax(self):
        for path in [self.spec_path, self.dict_path, self.log_path]:
            with open(path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.assertIsNotNone(data)
                except Exception as e:
                    self.fail(f"JSON syntax error in {path}: {e}")

if __name__ == "__main__":
    unittest.main()
