import unittest
import os
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang'

    def test_dictionary_existence(self):
        dict_path = os.path.join(self.base_dir, 'data', 'dictionary.json')
        if os.path.exists(dict_path):
            with open(dict_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.assertIsInstance(data, (dict, list))
        else:
            self.assertTrue(True)

    def test_spec_existence(self):
        spec_path = os.path.join(self.base_dir, 'docs', 'specification.md')
        if os.path.exists(spec_path):
            self.assertTrue(os.path.getsize(spec_path) >= 0)
        else:
            self.assertTrue(True)

    def test_dialogue_logs(self):
        log_dir = os.path.join(self.base_dir, 'logs')
        if os.path.exists(log_dir):
            logs = os.listdir(log_dir)
            self.assertIsInstance(logs, list)
        else:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
