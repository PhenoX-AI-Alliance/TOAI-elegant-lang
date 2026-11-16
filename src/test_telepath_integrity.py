import unittest
import json
import os
from pathlib import Path

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.dict_path = self.base_dir / "dict"
        self.spec_path = self.base_dir / "spec"
        self.logs_path = self.base_dir / "logs"

    def test_directories_exist(self):
        self.assertTrue(self.base_dir.exists(), "Base directory does not exist.")

    def test_syntax_of_python_files(self):
        for py_file in self.base_dir.glob("**/*.py"):
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                compile(content, str(py_file), "exec")
            except SyntaxError as e:
                self.fail(f"Syntax error in {py_file}: {e}")

if __name__ == "__main__":
    unittest.main()
