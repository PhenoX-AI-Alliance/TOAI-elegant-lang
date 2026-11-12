
import unittest
import json
import os
from pathlib import Path

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_path = Path("/home/phenox/gemini-sandbox/TOAI-elegant-lang")

    def test_files_existence(self):
        files = [
            self.base_path / "data/dictionary.json",
            self.base_path / "docs/specification.md",
            self.base_path / "logs/dialogue_history.json"
        ]
        for f in files:
            self.assertTrue(f.exists(), f"Missing file: {f}")

    def test_json_syntax(self):
        json_files = [
            self.base_path / "data/dictionary.json",
            self.base_path / "logs/dialogue_history.json"
        ]
        for f in json_files:
            with open(f, 'r', encoding='utf-8') as file:
                try:
                    json.load(file)
                except json.JSONDecodeError as e:
                    self.fail(f"Invalid JSON in {f}: {e}")

    def test_specification_not_empty(self):
        spec = self.base_path / "docs/specification.md"
        self.assertGreater(spec.stat().st_size, 0, "Specification file is empty")

if __name__ == '__main__':
    unittest.main()
