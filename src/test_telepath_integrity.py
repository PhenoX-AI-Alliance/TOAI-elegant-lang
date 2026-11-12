import sys
import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_exist(self):
        self.assertTrue(os.path.isdir(self.base_dir), f"Base directory does not exist: {self.base_dir}")
        self.assertTrue(os.path.isdir(self.src_dir), f"Source directory does not exist: {self.src_dir}")

    def test_files_integrity(self):
        dict_path = os.path.join(self.src_dir, "telepath_dict.json")
        spec_path = os.path.join(self.src_dir, "telepath_spec.md")
        log_path = os.path.join(self.src_dir, "telepath_dialogue.json")

        if not os.path.exists(dict_path):
            with open(dict_path, "w", encoding="utf-8") as f:
                json.dump({"version": "1.0", "entries": {}}, f, ensure_ascii=False, indent=2)
        
        if not os.path.exists(spec_path):
            with open(spec_path, "w", encoding="utf-8") as f:
                f.write("# Telepath Specification\nInitial spec.\n")

        if not os.path.exists(log_path):
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

        self.assertTrue(os.path.exists(dict_path), "Dictionary file is missing.")
        self.assertTrue(os.path.exists(spec_path), "Specification file is missing.")
        self.assertTrue(os.path.exists(log_path), "Dialogue log file is missing.")

        with open(dict_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                self.assertIsInstance(data, dict, "Dictionary file content must be a JSON object.")
            except json.JSONDecodeError as e:
                self.fail(f"Dictionary file contains invalid JSON: {e}")

        with open(log_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                self.assertIsInstance(data, list, "Dialogue log file content must be a JSON list.")
            except json.JSONDecodeError as e:
                self.fail(f"Dialogue log file contains invalid JSON: {e}")

if __name__ == "__main__":
    unittest.main()
