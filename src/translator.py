import sys
import os
import traceback
import time
import json

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            base_dir = '/home/phenox/gemini-sandbox/TOAI-elegant-lang/src'
            map_file_path = os.path.join(base_dir, 'translation_map.json')
        
        self.map_file_path = map_file_path
        self.translation_map = self.load_map()

    def load_map(self):
        if not os.path.exists(self.map_file_path):
            raise FileNotFoundError(f"Translation map not found at {self.map_file_path}")
        with open(self.map_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def decode(self, elegant_text):
        result = []
        i = 0
        n = len(elegant_text)
        while i < n:
            char = elegant_text[i]
            if char in self.translation_map:
                result.append(f"[{self.translation_map[char]}]")
            else:
                result.append(char)
            i += 1
        return "".join(result)

if __name__ == "__main__":
    try:
        translator = ElegantTranslator()
        sample_text = "Hello ~ world *!"
        decoded = translator.decode(sample_text)
        print("Original:", sample_text)
        print("Decoded:", decoded)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
