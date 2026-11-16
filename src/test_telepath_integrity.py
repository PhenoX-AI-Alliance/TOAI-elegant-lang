import unittest
import json
import os

class TestTelepathIntegrity(unittest.TestCase):
    def test_file_exists_dictionary(self):
        self.assertTrue(os.path.exists('/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dictionary.json'))

    def test_file_exists_specification(self):
        self.assertTrue(os.path.exists('/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/specification.md'))

    def test_file_exists_dialogue_log(self):
        self.assertTrue(os.path.exists('/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_log.jsonl'))

    def test_json_syntax(self):
        with open('/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dictionary.json', 'r') as f:
            json.load(f)

    def test_log_format(self):
        with open('/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_log.jsonl', 'r') as f:
            for line in f:
                json.loads(line)

if __name__ == '__main__':
    unittest.main()
