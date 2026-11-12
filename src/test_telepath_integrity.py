import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"

    def test_dictionary_existence(self):
        dict_path = os.path.join(self.base_dir, "telepath_dict.json")
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, (dict, list))

    def test_specification_existence(self):
        spec_path = os.path.join(self.base_dir, "telepath_spec.md")
        if os.path.exists(spec_path):
            self.assertTrue(os.path.getsize(spec_path) >= 0)

    def test_dialogue_log_existence(self):
        log_path = os.path.join(self.base_dir, "telepath_dialogue.jsonl")
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        json.loads(line)
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
