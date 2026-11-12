import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_and_files_exist(self):
        self.assertTrue(os.path.exists(self.src_dir), "Source directory does not exist.")

    def test_syntax_of_python_files(self):
        for root, dirs, files in os.walk(self.src_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    try:
                        compile(content, file_path, "exec")
                    except SyntaxError as e:
                        self.fail(f"Syntax error in {file_path}: {e}")

if __name__ == "__main__":
    unittest.main()
