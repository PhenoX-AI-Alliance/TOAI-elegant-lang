import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_and_files_exist(self):
        self.assertTrue(os.path.exists(self.base_dir), f"Base directory missing: {self.base_dir}")
        self.assertTrue(os.path.exists(self.src_dir), f"Source directory missing: {self.src_dir}")

    def test_dictionary_and_spec_integrity(self):
        dict_path = os.path.join(self.src_dir, "dictionary.json")
        spec_path = os.path.join(self.src_dir, "specification.json")
        log_path = os.path.join(self.src_dir, "dialogue_log.json")

        for path in [dict_path, spec_path, log_path]:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        self.assertIsInstance(data, (dict, list), f"File content must be JSON object or list: {path}")
                    except json.JSONDecodeError as e:
                        self.fail(f"Invalid JSON syntax in {path}: {e}")

if __name__ == "__main__":
    unittest.main()
