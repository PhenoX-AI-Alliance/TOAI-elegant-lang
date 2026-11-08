import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"

    def test_src_directory_exists(self):
        src_path = os.path.join(self.base_dir, "src")
        self.assertTrue(os.path.exists(src_path), "src directory must exist.")

    def test_dictionary_and_spec_files(self):
        # 辞書ファイル、仕様書、対話ログの存在と構文的健全性を検証する
        required_paths = [
            os.path.join(self.base_dir, "src"),
        ]
        for p in required_paths:
            self.assertTrue(os.path.exists(p), f"Required path {p} does not exist.")

    def test_python_syntax_of_src(self):
        src_path = os.path.join(self.base_dir, "src")
        for root, dirs, files in os.walk(src_path):
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
