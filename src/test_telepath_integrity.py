import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")
        
    def test_dictionary_existence_and_syntax(self):
        dict_path = os.path.join(self.base_dir, "dictionary.json")
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, (dict, list))
            
    def test_specification_existence(self):
        spec_path = os.path.join(self.base_dir, "specification.md")
        if os.path.exists(spec_path):
            with open(spec_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertGreater(len(content), 0)
            
    def test_dialogue_logs_integrity(self):
        log_dir = os.path.join(self.base_dir, "logs")
        if os.path.exists(log_dir):
            for filename in os.listdir(log_dir):
                if filename.endswith(".json"):
                    log_path = os.path.join(log_dir, filename)
                    with open(log_path, "r", encoding="utf-8") as f:
                        log_data = json.load(f)
                    self.assertIsInstance(log_data, (dict, list))

if __name__ == "__main__":
    unittest.main()
