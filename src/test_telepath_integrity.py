import unittest
import os
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
        self.src_dir = os.path.join(self.base_dir, 'src')

    def test_directory_structure(self):
        self.assertTrue(os.path.exists(self.base_dir), "Base directory must exist.")
        self.assertTrue(os.path.exists(self.src_dir), "Src directory must exist.")

    def test_syntax_of_source_files(self):
        for root, dirs, files in os.walk(self.src_dir):
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    try:
                        compile(content, full_path, 'exec')
                    except SyntaxError as e:
                        self.fail(f"Syntax error in {full_path}: {e}")

if __name__ == '__main__':
    unittest.main()
