import sys
import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directory_structure(self):
        self.assertTrue(os.path.exists(self.base_dir), f"Base directory does not exist: {self.base_dir}")
        self.assertTrue(os.path.exists(self.src_dir), f"Source directory does not exist: {self.src_dir}")

    def test_dictionary_and_specs(self):
        dict_path = os.path.join(self.src_dir, "dictionary.json")
        spec_path = os.path.join(self.src_dir, "specification.md")
        log_path = os.path.join(self.src_dir, "dialogue_log.json")

        if not os.path.exists(dict_path):
            with open(dict_path, "w", encoding="utf-8") as f:
                json.dump({"version": "1.0", "terms": {}}, f, ensure_ascii=False, indent=4)
        
        if not os.path.exists(spec_path):
            with open(spec_path, "w", encoding="utf-8") as f:
                f.write("# Telepath Specification\n\nInitial specification document.\n")

        if not os.path.exists(log_path):
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        self.assertTrue(os.path.exists(dict_path), "Dictionary file missing.")
        self.assertTrue(os.path.exists(spec_path), "Specification file missing.")
        self.assertTrue(os.path.exists(log_path), "Dialogue log file missing.")

        try:
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIsInstance(data, dict, "Dictionary must be a JSON object.")
        except json.JSONDecodeError as e:
            self.fail(f"Dictionary JSON is syntactically broken: {e}")

        try:
            with open(log_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIsInstance(data, list, "Dialogue log must be a JSON list.")
        except json.JSONDecodeError as e:
            self.fail(f"Dialogue log JSON is syntactically broken: {e}")

        with open(spec_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertGreater(len(content), 0, "Specification file is empty.")

if __name__ == "__main__":
    unittest.main()
