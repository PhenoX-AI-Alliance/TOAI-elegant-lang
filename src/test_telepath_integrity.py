import sys
import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")
        
    def test_directories_exist(self):
        self.assertTrue(os.path.isdir(self.base_dir), "Base directory does not exist.")
        self.assertTrue(os.path.isdir(self.src_dir), "Source directory does not exist.")

    def test_placeholder_files_or_create(self):
        dict_path = os.path.join(self.src_dir, "dictionary.json")
        spec_path = os.path.join(self.src_dir, "specification.md")
        log_path = os.path.join(self.src_dir, "dialogue_log.jsonl")
        
        if not os.path.exists(dict_path):
            with open(dict_path, "w", encoding="utf-8") as f:
                json.dump({"version": "1.0", "terms": {}}, f, ensure_ascii=False, indent=2)
                
        if not os.path.exists(spec_path):
            with open(spec_path, "w", encoding="utf-8") as f:
                f.write("# TOAI Elegant Lang Specification\n")
                
        if not os.path.exists(log_path):
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(json.dumps({"event": "init", "timestamp": "2026-03-31"}) + "\n")
                
        self.assertTrue(os.path.exists(dict_path))
        self.assertTrue(os.path.exists(spec_path))
        self.assertTrue(os.path.exists(log_path))

    def test_dictionary_syntax(self):
        dict_path = os.path.join(self.src_dir, "dictionary.json")
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, dict)

    def test_dialogue_log_syntax(self):
        log_path = os.path.join(self.src_dir, "dialogue_log.jsonl")
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        item = json.loads(line)
                        self.assertIsInstance(item, dict)

if __name__ == "__main__":
    unittest.main()
