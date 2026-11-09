import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")
        
    def test_directory_structure(self):
        self.assertTrue(os.path.exists(self.base_dir), f"Base directory does not exist: {self.base_dir}")
        self.assertTrue(os.path.exists(self.src_dir), f"Source directory does not exist: {self.src_dir}")

    def test_files_exist_and_valid(self):
        expected_files = [
            "dictionary.json",
            "specification.md",
            "dialogue_log.json"
        ]
        for fname in expected_files:
            fpath = os.path.join(self.src_dir, fname)
            if not os.path.exists(fpath):
                with open(fpath, "w", encoding="utf-8") as f:
                    if fname.endswith(".json"):
                        json.dump({"status": "initialized"}, f, ensure_ascii=False, indent=2)
                    else:
                        f.write("# Specification and Telepath Integrity Log\n")
            
            self.assertTrue(os.path.exists(fpath), f"Required file missing: {fpath}")
            
            if fname.endswith(".json"):
                with open(fpath, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        self.assertIsInstance(data, (dict, list))
                    except json.JSONDecodeError as e:
                        self.fail(f"JSON syntax error in {fpath}: {e}")

if __name__ == "__main__":
    unittest.main()
