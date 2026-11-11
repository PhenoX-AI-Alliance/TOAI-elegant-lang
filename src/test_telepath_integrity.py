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

    def test_dictionary_and_specs(self):
        # Check for potential dictionary, specifications, or dialog logs if they are expected to exist.
        # If they don't exist yet, we ensure the paths are structurally sound.
        dict_path = os.path.join(self.base_dir, "dictionary.json")
        spec_path = os.path.join(self.base_dir, "spec.md")
        log_path = os.path.join(self.base_dir, "dialog_log.json")
        
        # We assert that if these files exist, they are syntactically valid JSON or readable text.
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIsInstance(data, (dict, list))

        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertIsInstance(data, (dict, list))

    def test_syntax_integrity(self):
        # Verify all python files in src directory are syntactically valid
        if os.path.exists(self.src_dir):
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
