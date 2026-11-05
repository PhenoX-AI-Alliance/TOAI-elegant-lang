import unittest
from pathlib import Path

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path("/home/phenox/gemini-sandbox/TOAI-elegant-lang")
        self.src_dir = self.base_dir / "src"

    def test_directories_exist(self):
        self.assertTrue(self.base_dir.exists(), "Base directory does not exist.")
        self.assertTrue(self.src_dir.exists(), "Src directory does not exist.")

    def test_syntax_of_python_files(self):
        python_files = list(self.src_dir.glob("*.py"))
        for py_file in python_files:
            if py_file.name == "test_telepath_integrity.py":
                continue
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
            try:
                compile(content, str(py_file), "exec")
            except SyntaxError as e:
                self.fail(f"Syntax error in {py_file.name}: {e}")

if __name__ == "__main__":
    unittest.main()
