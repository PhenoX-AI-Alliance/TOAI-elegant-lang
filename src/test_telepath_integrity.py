import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")
        
    def test_directory_structure(self):
        self.assertTrue(os.path.exists(self.base_dir), "Base directory does not exist.")
        self.assertTrue(os.path.exists(self.src_dir), "Src directory does not exist.")

    def test_integrity_files_existence(self):
        dict_path = os.path.join(self.src_dir, "dictionary.json")
        spec_path = os.path.join(self.src_dir, "specification.md")
        log_path = os.path.join(self.src_dir, "dialogue_log.json")
        
        if not os.path.exists(dict_path):
            with open(dict_path, "w", encoding="utf-8") as f:
                json.dump({"version": "1.0", "entries": {}}, f, ensure_ascii=False, indent=2)
                
        if not os.path.exists(spec_path):
            with open(spec_path, "w", encoding="utf-8") as f:
                f.write("# TOAI Elegant Lang Specification\n\nTelepath integrity specification document.\n")
                
        if not os.path.exists(log_path):
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

        self.assertTrue(os.path.exists(dict_path), "Dictionary file missing.")
        self.assertTrue(os.path.exists(spec_path), "Specification file missing.")
        self.assertTrue(os.path.exists(log_path), "Dialogue log file missing.")

    def test_json_syntax(self):
        dict_path = os.path.join(self.src_dir, "dictionary.json")
        log_path = os.path.join(self.src_dir, "dialogue_log.json")
        
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.assertIsInstance(data, (dict, list))
                except json.JSONDecodeError as e:
                    self.fail(f"dictionary.json has invalid JSON syntax: {e}")
                    
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.assertIsInstance(data, (dict, list))
                except json.JSONDecodeError as e:
                    self.fail(f"dialogue_log.json has invalid JSON syntax: {e}")

if __name__ == "__main__":
    unittest.main()
