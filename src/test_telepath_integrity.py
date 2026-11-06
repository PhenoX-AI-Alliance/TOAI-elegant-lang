import unittest
import os
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")
        self.logs_dir = os.path.join(self.base_dir, "logs")
        self.specs_dir = os.path.join(self.base_dir, "specs")
        self.dicts_dir = os.path.join(self.base_dir, "dicts")

    def test_file_existence(self):
        log_file = os.path.join(self.logs_dir, "interaction.log")
        spec_file = os.path.join(self.specs_dir, "telepath_spec.json")
        dict_file = os.path.join(self.dicts_dir, "telepath_dict.json")

        self.assertTrue(os.path.exists(log_file), f"File missing: {log_file}")
        self.assertTrue(os.path.exists(spec_file), f"File missing: {spec_file}")
        self.assertTrue(os.path.exists(dict_file), f"File missing: {dict_file}")

    def test_json_validity(self):
        spec_file = os.path.join(self.specs_dir, "telepath_spec.json")
        dict_file = os.path.join(self.dicts_dir, "telepath_dict.json")

        with open(spec_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertIsInstance(data, dict)

        with open(dict_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertIsInstance(data, dict)

    def test_log_validity(self):
        log_file = os.path.join(self.logs_dir, "interaction.log")
        with open(log_file, "r", encoding="utf-8") as f:
            line = f.readline()
            data = json.loads(line)
            self.assertIsInstance(data, dict)

if __name__ == "__main__":
    unittest.main()
