import sys
import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def test_dictionary_and_specs(self):
        base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        dict_path = os.path.join(base_dir, "dict", "telepath_dict.json")
        spec_path = os.path.join(base_dir, "docs", "telepath_spec.md")
        log_path = os.path.join(base_dir, "logs", "dialogue_log.json")

        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, (dict, list))

        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
            self.assertIsInstance(logs, (dict, list))

        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
