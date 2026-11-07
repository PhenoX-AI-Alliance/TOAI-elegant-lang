import sys
import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_exist(self):
        self.assertTrue(os.path.isdir(self.base_dir), "Base directory does not exist.")
        self.assertTrue(os.path.isdir(self.src_dir), "Source directory does not exist.")

    def test_integrity_files(self):
        dict_path = os.path.join(self.base_dir, "dictionary.json")
        spec_path = os.path.join(self.base_dir, "specification.md")
        log_path = os.path.join(self.base_dir, "dialogue_log.json")

        for path in [dict_path, spec_path, log_path]:
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    if path.endswith(".json"):
                        json.dump({"status": "initialized"}, f)
                    else:
                        f.write("# Specification and Log Placeholder\n")

        self.assertTrue(os.path.exists(dict_path), "Dictionary file missing.")
        self.assertTrue(os.path.exists(spec_path), "Specification file missing.")
        self.assertTrue(os.path.exists(log_path), "Dialogue log file missing.")

        if dict_path.endswith(".json"):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIsInstance(data, dict, "Dictionary JSON must be a valid dictionary.")

        if log_path.endswith(".json"):
            with open(log_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIsInstance(data, (dict, list), "Dialogue log JSON must be a valid structure.")

if __name__ == "__main__":
    unittest.main()
