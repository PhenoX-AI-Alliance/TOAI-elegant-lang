import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'
        self.src_dir = os.path.join(self.base_dir, 'src')

    def test_directories_exist(self):
        self.assertTrue(os.path.exists(self.base_dir), "Base directory does not exist.")
        self.assertTrue(os.path.exists(self.src_dir), "Source directory does not exist.")

    def test_syntax_of_source_files(self):
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    try:
                        compile(content, file_path, 'exec')
                    except SyntaxError as e:
                        self.fail(f"Syntax error in {file_path}: {e}")

    def test_dictionary_and_specs(self):
        dict_path = os.path.join(self.base_dir, 'dictionary.json')
        spec_path = os.path.join(self.base_dir, 'specification.md')
        
        if os.path.exists(dict_path):
            with open(dict_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.assertIsInstance(data, (dict, list), "Dictionary file is not valid JSON.")
        
        if os.path.exists(spec_path):
            with open(spec_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertGreater(len(content), 0, "Specification file is empty.")

if __name__ == '__main__':
    unittest.main()
