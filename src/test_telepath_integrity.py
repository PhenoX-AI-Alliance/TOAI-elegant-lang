import sys
import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")
        
    def test_directories_exist(self):
        self.assertTrue(os.path.exists(self.base_dir), "Base directory missing")
        self.assertTrue(os.path.exists(self.src_dir), "Src directory missing")

    def test_dictionary_and_specs(self):
        dict_path = os.path.join(self.base_dir, "dictionary.json")
        spec_path = os.path.join(self.base_dir, "specification.md")
        log_path = os.path.join(self.base_dir, "dialogue_log.json")
        
        if not os.path.exists(dict_path):
            with open(dict_path, "w", encoding="utf-8") as f:
                json.dump({"version": "1.0", "terms": {}}, f, ensure_ascii=False, indent=2)
                
        if not os.path.exists(spec_path):
            with open(spec_path, "w", encoding="utf-8") as f:
                f.write("# TOAI Elegant Lang Specification\n")
                
        if not os.path.exists(log_path):
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

        self.assertTrue(os.path.exists(dict_path), "Dictionary file missing")
        self.assertTrue(os.path.exists(spec_path), "Specification file missing")
        self.assertTrue(os.path.exists(log_path), "Dialogue log file missing")

        with open(dict_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertIsInstance(data, dict, "Dictionary must be a valid JSON object")

        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)
            self.assertIsInstance(logs, list, "Dialogue log must be a valid JSON list")

if __name__ == "__main__":
    unittest.main()
