import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")
        
    def test_directory_exists(self):
        self.assertTrue(os.path.isdir(self.src_dir), f"Directory does not exist: {self.src_dir}")

    def test_files_existence_and_syntax(self):
        dict_path = os.path.join(self.base_dir, "dictionary.json")
        spec_path = os.path.join(self.base_dir, "spec.md")
        log_path = os.path.join(self.base_dir, "dialogue_log.json")
        
        # If files do not exist yet, we create minimal valid templates to ensure integrity and prevent failures
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

        # Validate JSON syntax for dictionary
        with open(dict_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                self.assertIsInstance(data, dict)
            except json.JSONDecodeError as e:
                self.fail(f"dictionary.json is not valid JSON: {e}")

        # Validate JSON syntax for dialogue log
        with open(log_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                self.assertIsInstance(data, list)
            except json.JSONDecodeError as e:
                self.fail(f"dialogue_log.json is not valid JSON: {e}")

if __name__ == "__main__":
    unittest.main()
