import unittest
from pathlib import Path

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path("/home/phenox/gemini-sandbox/TOAI-elegant-lang")
        self.src_dir = self.base_dir / "src"

    def test_directories_exist(self):
        self.assertTrue(self.base_dir.exists(), f"Base directory does not exist: {self.base_dir}")
        self.assertTrue(self.src_dir.exists(), f"Src directory does not exist: {self.src_dir}")

    def test_dictionary_and_spec_integrity(self):
        dict_files = list(self.base_dir.glob("**/*.json"))
        spec_files = list(self.base_dir.glob("**/*.md"))
        log_files = list(self.base_dir.glob("**/*.log"))
        
        for json_file in dict_files:
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    json.load(f)
            except Exception as e:
                self.fail(f"JSON syntax error in {json_file}: {e}")

if __name__ == "__main__":
    unittest.main()
