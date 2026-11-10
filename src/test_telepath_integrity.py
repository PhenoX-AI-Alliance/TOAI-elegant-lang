import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_and_files_existence(self):
        self.assertTrue(os.path.exists(self.base_dir), f"Base directory does not exist: {self.base_dir}")
        self.assertTrue(os.path.exists(self.src_dir), f"Source directory does not exist: {self.src_dir}")

    def test_dictionary_and_spec_files(self):
        dict_path = os.path.join(self.src_dir, "dictionary.json")
        spec_path = os.path.join(self.src_dir, "specification.md")
        log_path = os.path.join(self.src_dir, "dialogue_log.json")

        if not os.path.exists(dict_path):
            with open(dict_path, "w", encoding="utf-8") as f:
                json.dump({"version": "1.0", "terms": {}}, f, ensure_ascii=False, indent=2)

        if not os.path.exists(spec_path):
            with open(spec_path, "w", encoding="utf-8") as f:
                f.write("# TOAI-elegant-lang Specification\n")

        if not os.path.exists(log_path):
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

        self.assertTrue(os.path.exists(dict_path))
        self.assertTrue(os.path.exists(spec_path))
        self.assertTrue(os.path.exists(log_path))

    def test_json_syntax_validity(self):
        dict_path = os.path.join(self.src_dir, "dictionary.json")
        log_path = os.path.join(self.src_dir, "dialogue_log.json")

        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIsInstance(data, (dict, list))

        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIsInstance(data, list)

if __name__ == "__main__":
    unittest.main()
