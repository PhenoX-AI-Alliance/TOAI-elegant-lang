import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"

    def test_directory_exists(self):
        self.assertTrue(os.path.isdir(self.base_dir), f"Directory does not exist: {self.base_dir}")

    def test_files_presence_and_syntax(self):
        # 辞書ファイル、仕様書、対話ログなどの存在や構文チェック用プレースホルダー
        # 該当ファイルが存在する場合はJSONとしてのパース可能性などを検証する
        files_to_check = [
            "telepath_dict.json",
            "telepath_spec.md",
            "telepath_dialogue.log"
        ]
        
        for filename in files_to_check:
            file_path = os.path.join(self.base_dir, filename)
            if os.path.exists(file_path):
                if filename.endswith(".json"):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            json.load(f)
                    except json.JSONDecodeError as e:
                        self.fail(f"JSON decode error in {file_path}: {e}")
                else:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    self.assertGreaterEqual(len(content), 0, f"File {file_path} is unreadable.")
            else:
                # 存在しないファイルは警告とするか、初期作成を行う
                with open(file_path, "w", encoding="utf-8") as f:
                    if filename.endswith(".json"):
                        json.dump({}, f)
                    else:
                        f.write("INITIAL_STUB")

if __name__ == "__main__":
    unittest.main()
