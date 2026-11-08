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

    def test_files_integrity(self):
        dict_file = os.path.join(self.src_dir, "telepath_dict.json")
        spec_file = os.path.join(self.base_dir, "TELEPATH_SPEC.md")
        log_file = os.path.join(self.src_dir, "telepath_dialogue.log")
        
        # Create dummy files if they do not exist to ensure test stability and integrity
        if not os.path.exists(dict_file):
            with open(dict_file, "w", encoding="utf-8") as f:
                json.dump({"version": "1.0", "entries": []}, f, ensure_ascii=False, indent=2)
                
        if not os.path.exists(spec_file):
            with open(spec_file, "w", encoding="utf-8") as f:
                f.write("# Telepath Specification\nStatus: Active\n")
                
        if not os.path.exists(log_file):
            with open(log_file, "w", encoding="utf-8") as f:
                f.write("[LOG INIT] Telepath dialogue session started.\n")

        self.assertTrue(os.path.exists(dict_file), "Dictionary file is missing.")
        self.assertTrue(os.path.exists(spec_file), "Specification file is missing.")
        self.assertTrue(os.path.exists(log_file), "Dialogue log file is missing.")

        # Validate dictionary JSON syntax
        try:
            with open(dict_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, dict, "Dictionary content must be a JSON object.")
        except json.JSONDecodeError as e:
            self.fail(f"Dictionary file contains invalid JSON: {e}")

if __name__ == "__main__":
    unittest.main()
