import unittest
import os
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"

    def test_src_directory_exists(self):
        src_path = os.path.join(self.base_dir, "src")
        self.assertTrue(os.path.isdir(src_path), "src directory must exist.")

    def test_dictionary_and_specs(self):
        # 辞書ファイルや仕様書、対話ログが存在する場合の整合性チェック用アサート
        # ファイルが存在しない場合は空のパスとして許容しつつ、存在する場合は中身の構文を検証する
        dict_path = os.path.join(self.base_dir, "src", "dictionary.json")
        if os.path.exists(dict_path):
            with open(dict_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, (dict, list), "Dictionary must be valid JSON object or list.")

if __name__ == "__main__":
    unittest.main()
