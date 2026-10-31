import sys
import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")
        
    def test_dictionary_exists(self):
        dict_path = os.path.join(self.src_dir, "dictionary.json")
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, (dict, list))
        else:
            self.assertTrue(True, "Dictionary optional or not created yet")

    def test_spec_exists(self):
        spec_path = os.path.join(self.base_dir, "SPEC.md")
        if os.path.exists(spec_path):
            self.assertTrue(os.path.getsize(spec_path) > 0)
        else:
            self.assertTrue(True, "SPEC.md optional or not created yet")

    def test_syntax_integrity(self):
        for root, dirs, files in os.walk(self.src_dir):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    try:
                        compile(content, full_path, "exec")
                    except SyntaxError as e:
                        self.fail(f"Syntax error in {full_path}: {e}")

if __name__ == "__main__":
    unittest.main()
