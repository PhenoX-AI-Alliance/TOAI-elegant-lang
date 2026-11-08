import unittest
import os
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")
        
    def test_directories_exist(self):
        self.assertTrue(os.path.exists(self.base_dir), "Base directory does not exist.")
        self.assertTrue(os.path.exists(self.src_dir), "Source directory does not exist.")

    def test_integrity_files(self):
        dict_path = os.path.join(self.src_dir, "telepath_dict.json")
        spec_path = os.path.join(self.src_dir, "telepath_spec.md")
        log_path = os.path.join(self.src_dir, "telepath_dialogue.log")
        
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIsInstance(data, dict, "Dictionary file must contain a valid JSON object.")
                
        if os.path.exists(spec_path):
            with open(spec_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertGreater(len(content), 0, "Specification file is empty.")
                
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                self.assertIsInstance(lines, list, "Dialogue log must be readable as lines.")

if __name__ == "__main__":
    unittest.main()
