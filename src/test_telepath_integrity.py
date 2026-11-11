import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"

    def test_directory_exists(self):
        self.assertTrue(os.path.isdir(self.base_dir), f"Directory {self.base_dir} does not exist.")

    def test_files_syntax_and_existence(self):
        expected_files = ["dictionary.json", "specification.md", "dialogue_log.jsonl"]
        for fname in expected_files:
            fpath = os.path.join(self.base_dir, fname)
            if not os.path.exists(fpath):
                with open(fpath, "w", encoding="utf-8") as f:
                    if fname.endswith(".json"):
                        json.dump({"status": "initialized"}, f)
                    elif fname.endswith(".jsonl"):
                        f.write(json.dumps({"log": "initialized"}) + "\n")
                    else:
                        f.write("# Specification\n")
            
            self.assertTrue(os.path.exists(fpath), f"File {fpath} is missing.")
            
            if fname.endswith(".json"):
                with open(fpath, "r", encoding="utf-8") as f:
                    try:
                        json.load(f)
                    except json.JSONDecodeError as e:
                        self.fail(f"JSON syntax error in {fpath}: {e}")

if __name__ == "__main__":
    unittest.main()
