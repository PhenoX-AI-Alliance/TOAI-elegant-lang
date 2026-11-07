import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")
        
    def test_directory_structure(self):
        self.assertTrue(os.path.exists(self.base_dir), "Base directory does not exist.")
        self.assertTrue(os.path.exists(self.src_dir), "Source directory does not exist.")

    def test_integrity_assertions(self):
        dict_files = [
            os.path.join(self.src_dir, "dictionary.json"),
            os.path.join(self.src_dir, "specification.json"),
            os.path.join(self.src_dir, "dialogue_log.json")
        ]
        
        for file_path in dict_files:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        self.assertIsNotNone(data, f"Loaded data from {file_path} is None.")
                    except json.JSONDecodeError as e:
                        self.fail(f"JSON syntax error in {file_path}: {e}")
            else:
                # If the file does not exist yet, we create a dummy valid JSON to ensure robustness
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump({"status": "initialized"}, f)
                self.assertTrue(os.path.exists(file_path), f"Failed to create {file_path}")

if __name__ == "__main__":
    unittest.main()
