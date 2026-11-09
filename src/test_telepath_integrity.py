import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_and_files_exist(self):
        self.assertTrue(os.path.exists(self.base_dir), "Base directory missing")
        self.assertTrue(os.path.exists(self.src_dir), "Src directory missing")

    def test_dictionary_and_spec_syntax(self):
        dict_path = os.path.join(self.base_dir, "dictionary.json")
        spec_path = os.path.join(self.base_dir, "specification.md")
        log_path = os.path.join(self.base_dir, "dialogue_log.json")

        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, (dict, list))

        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
            self.assertIsInstance(logs, (dict, list))

        if os.path.exists(spec_path):
            with open(spec_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertGreater(len(content), 0)

if __name__ == "__main__":
    unittest.main()
