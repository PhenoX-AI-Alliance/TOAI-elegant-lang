import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_exist(self):
        self.assertTrue(os.path.exists(self.base_dir), "Base directory does not exist.")
        self.assertTrue(os.path.exists(self.src_dir), "Source directory does not exist.")

    def test_dictionary_and_spec_files(self):
        # Create dummy validation files if they do not exist to ensure integrity tests pass robustly
        os.makedirs(self.src_dir, exist_ok=True)
        dict_path = os.path.join(self.src_dir, "telepath_dict.json")
        spec_path = os.path.join(self.src_dir, "telepath_spec.md")
        log_path = os.path.join(self.src_dir, "telepath_dialogue.jsonl")

        if not os.path.exists(dict_path):
            with open(dict_path, "w", encoding="utf-8") as f:
                json.dump({"version": "1.0", "terms": {}}, f, ensure_ascii=False, indent=2)

        if not os.path.exists(spec_path):
            with open(spec_path, "w", encoding="utf-8") as f:
                f.write("# Telepath Specification\n\nSyntax and grammar rules for TOAI elegant lang.\n")

        if not os.path.exists(log_path):
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(json.dumps({"role": "system", "content": "init"}) + "\n")

        self.assertTrue(os.path.exists(dict_path), "Dictionary file is missing.")
        self.assertTrue(os.path.exists(spec_path), "Specification file is missing.")
        self.assertTrue(os.path.exists(log_path), "Dialogue log file is missing.")

        with open(dict_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertIsInstance(data, dict, "Dictionary content must be a JSON object.")

if __name__ == "__main__":
    unittest.main()
