import json
import unittest
from pathlib import Path


class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.src_dir = Path(__file__).resolve().parent
        self.base_dir = Path(__file__).resolve().parents[1]

    def test_directories_exist(self):
        self.assertTrue(self.base_dir.is_dir(), "Base directory does not exist.")
        self.assertTrue(self.src_dir.is_dir(), "Source directory does not exist.")

    def test_lexicon_and_spec_integrity(self):
        pkg_lex_path = self.src_dir / "lexicon" / "core_lexicon.json"
        repo_lex_path = self.base_dir / "lexicon" / "core_lexicon.json"
        rosetta_path = self.src_dir / "lexicon" / "rosetta_layer.json"

        self.assertTrue(pkg_lex_path.is_file(), f"Package lexicon file missing: {pkg_lex_path}")
        with pkg_lex_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data.get("lexicon", {})), 256, "Core lexicon must contain 256 primitives.")

        if repo_lex_path.is_file():
            with repo_lex_path.open("r", encoding="utf-8") as f:
                repo_data = json.load(f)
            self.assertEqual(len(repo_data.get("lexicon", {})), 256)

        self.assertTrue(rosetta_path.is_file(), f"Rosetta layer file missing: {rosetta_path}")
        with rosetta_path.open("r", encoding="utf-8") as f:
            rosetta_data = json.load(f)
        self.assertIsInstance(rosetta_data, dict)


if __name__ == "__main__":
    unittest.main()
