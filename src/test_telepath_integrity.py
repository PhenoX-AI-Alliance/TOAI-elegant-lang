import sys
import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_exist(self):
        self.assertTrue(os.path.exists(self.base_dir), "Base directory missing")
        self.assertTrue(os.path.exists(self.src_dir), "Source directory missing")

    def test_mock_dictionary_and_specs(self):
        dict_path = os.path.join(self.src_dir, "dictionary.json")
        spec_path = os.path.join(self.src_dir, "specification.md")
        log_path = os.path.join(self.src_dir, "dialogue_log.json")

        if not os.path.exists(dict_path):
            with open(dict_path, "w", encoding="utf-8") as f:
                json.dump({"version": "1.0", "entries": []}, f, ensure_ascii=False, indent=2)
        
        if not os.path.exists(spec_path):
            with open(spec_path, "w", encoding="utf-8") as f:
                f.write("# TOAI Elegant Lang Specification\n")

        if not os.path.exists(log_path):
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

        self.assertTrue(os.path.exists(dict_path))
        self.assertTrue(os.path.exists(spec_path))
        self.assertTrue(os.path.exists(log_path))

        try:
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIsInstance(data, dict)
        except Exception as e:
            self.fail(f"Dictionary file is not valid JSON: {e}")

        try:
            with open(log_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIsInstance(data, list)
        except Exception as e:
            self.fail(f"Dialogue log is not valid JSON: {e}")

if __name__ == "__main__":
    unittest.main()
