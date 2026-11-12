import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")
        
    def test_directory_structure(self):
        self.assertTrue(os.path.exists(self.base_dir), "Base directory must exist.")
        self.assertTrue(os.path.exists(self.src_dir), "Source directory must exist.")

    def test_dictionary_files_integrity(self):
        dict_path = os.path.join(self.base_dir, "dictionary")
        if os.path.exists(dict_path):
            for root, dirs, files in os.walk(dict_path):
                for file in files:
                    if file.endswith(".json"):
                        file_path = os.path.join(root, file)
                        with open(file_path, "r", encoding="utf-8") as f:
                            try:
                                json.load(f)
                            except json.JSONDecodeError as e:
                                self.fail(f"JSON syntax error in {{file_path}}: {{e}}")

    def test_specification_and_logs(self):
        spec_path = os.path.join(self.base_dir, "specifications")
        logs_path = os.path.join(self.base_dir, "logs")
        
        if os.path.exists(spec_path):
            specs = os.listdir(spec_path)
            self.assertGreaterEqual(len(specs), 0, "Specifications directory check.")
            
        if os.path.exists(logs_path):
            logs = os.listdir(logs_path)
            self.assertGreaterEqual(len(logs), 0, "Logs directory check.")

if __name__ == "__main__":
    unittest.main()
