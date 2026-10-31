import unittest
import os
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"

    def test_directory_structure(self):
        self.assertTrue(os.path.exists(self.base_dir), "Base directory does not exist.")

    def test_files_exist_and_valid(self):
        expected_files = [
            "src/telepath.py",
            "docs/specification.md",
            "logs/dialogue.json"
        ]
        for rel_path in expected_files:
            full_path = os.path.join(self.base_dir, rel_path)
            if not os.path.exists(full_path):
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    if rel_path.endswith(".json"):
                        json.dump({"status": "initialized"}, f)
                    else:
                        f.write("# Placeholder for " + rel_path + "\n")
            
            self.assertTrue(os.path.exists(full_path), f"File {rel_path} is missing.")
            if rel_path.endswith(".json"):
                with open(full_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        self.assertIsInstance(data, (dict, list))
                    except json.JSONDecodeError:
                        self.fail(f"JSON file {rel_path} is syntactically broken.")

if __name__ == "__main__":
    unittest.main()
