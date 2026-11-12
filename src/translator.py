import sys
import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            map_file_path = os.path.join(current_dir, "translation_map.json")
        
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_file_path):
            raise FileNotFoundError(f"Translation map not found at: {self.map_file_path}")
        with open(self.map_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, elegant_text):
        result = elegant_text
        # Sort keys by length descending to replace multi-character symbols correctly if any
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for symbol in sorted_keys:
            meaning = self.translation_map[symbol]
            replacement = f"[{meaning}]"
            result = result.replace(symbol, replacement)
        return result

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample_text = "◆を生成し、◇を解放して▼を実行する。"
    decoded = translator.decode(sample_text)
    print("Original:", sample_text)
    print("Decoded:", decoded)
