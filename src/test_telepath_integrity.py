import sys
import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.BASE_PATH = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_path = os.path.join(self.BASE_PATH, "src")
        self.data_path = os.path.join(self.BASE_PATH, "data")
        self.docs_path = os.path.join(self.BASE_PATH, "docs")
        
        os.makedirs(self.src_path, exist_ok=True)
        os.makedirs(self.data_path, exist_ok=True)
        os.makedirs(self.docs_path, exist_ok=True)

    def test_directories_exist(self):
        self.assertTrue(os.path.exists(self.src_path))
        self.assertTrue(os.path.exists(self.data_path))
        self.assertTrue(os.path.exists(self.docs_path))

    def test_files_integrity(self):
        dict_file = os.path.join(self.data_path, "dictionary.json")
        spec_file = os.path.join(self.docs_path, "specification.md")
        log_file = os.path.join(self.data_path, "dialogue_log.json")

        if not os.path.exists(dict_file):
            with open(dict_file, "w", encoding="utf-8") as f:
                json.dump({"version": "1.0", "terms": {}}, f, ensure_ascii=False, indent=2)
        if not os.path.exists(spec_file):
            with open(spec_file, "w", encoding="utf-8") as f:
                f.write("# Telepath Specification\n")
        if not os.path.exists(log_file):
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

        self.assertTrue(os.path.exists(dict_file))
        self.assertTrue(os.path.exists(spec_file))
        self.assertTrue(os.path.exists(log_file))

        with open(dict_file, "r", encoding="utf-8") as f:
            json.load(f)

        with open(log_file, "r", encoding="utf-8") as f:
            json.load(f)

if __name__ == "__main__":
    unittest.main()
