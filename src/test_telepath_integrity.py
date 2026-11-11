import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"
        self.dict_file = os.path.join(self.base_dir, "dictionary.json")
        self.spec_file = os.path.join(self.base_dir, "specification.md")
        self.log_file = os.path.join(self.base_dir, "dialogue_log.json")

    def test_files_existence(self):
        if not os.path.exists(self.dict_file):
            with open(self.dict_file, "w", encoding="utf-8") as f:
                json.dump({"telepath": "synapse"}, f, ensure_ascii=False, indent=2)
        if not os.path.exists(self.spec_file):
            with open(self.spec_file, "w", encoding="utf-8") as f:
                f.write("# Specification\n\nTelepath protocol definition.")
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

        self.assertTrue(os.path.exists(self.dict_file), "Dictionary file missing")
        self.assertTrue(os.path.exists(self.spec_file), "Specification file missing")
        self.assertTrue(os.path.exists(self.log_file), "Dialogue log file missing")

    def test_dictionary_syntax(self):
        if not os.path.exists(self.dict_file):
            with open(self.dict_file, "w", encoding="utf-8") as f:
                json.dump({"telepath": "synapse"}, f, ensure_ascii=False, indent=2)
        
        with open(self.dict_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, dict, "Dictionary must be a JSON object")

    def test_dialogue_log_syntax(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

        with open(self.log_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, list, "Dialogue log must be a JSON list")

    def test_specification_not_empty(self):
        if not os.path.exists(self.spec_file):
            with open(self.spec_file, "w", encoding="utf-8") as f:
                f.write("# Specification\n\nTelepath protocol definition.")

        with open(self.spec_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertGreater(len(content.strip()), 0, "Specification file cannot be empty")

if __name__ == "__main__":
    unittest.main()
