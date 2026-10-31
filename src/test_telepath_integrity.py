import sys
import os
import unittest
import json

class TestTelepathIntegrity(unittest.TestCase):
    def setUp(self):
        self.base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        self.src_dir = os.path.join(self.base_dir, "src")

    def test_directories_exist(self):
        self.assertTrue(os.path.exists(self.base_dir), "Base directory missing")
        self.assertTrue(os.path.exists(self.src_dir), "Src directory missing")

    def test_sample_integrity(self):
        test_file = os.path.join(self.src_dir, "test_telepath_integrity.py")
        self.assertTrue(os.path.exists(test_file), "Self file should exist")

if __name__ == "__main__":
    unittest.main()
