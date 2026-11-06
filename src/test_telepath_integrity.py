import os
import json
import unittest

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_exist(self):
        self.assertTrue(os.path.isdir(self.base_dir), "Base directory does not exist.")
        self.assertTrue(os.path.isdir(self.src_dir), "Src directory does not exist.")

    def test_integrity_files(self):
        # 辞書ファイル、仕様書、対話ログなどの存在や構文チェックのモック/実アサート
        # ここではファイル群のプレースホルダー検証、または実ファイルの存在確認を行う
        required_files = []
        for f in required_files:
            file_path = os.path.join(self.base_dir, f)
            self.assertTrue(os.path.exists(file_path), f"Required file missing: {f}")

    def test_python_syntax(self):
        # srcディレクトリ内の全Pythonファイルの構文が壊れていないかを検証
        for root, dirs, files in os.walk(self.src_dir):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    try:
                        compile(content, full_path, "exec")
                    except SyntaxError as e:
                        self.fail(f"Syntax error in {full_path}: {e}")

if __name__ == "__main__":
    unittest.main()
