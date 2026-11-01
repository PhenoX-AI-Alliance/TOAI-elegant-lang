import os
import sys
import json

class ElegantTranslator:
    def __init__(self, map_file_path):
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_file_path):
            raise FileNotFoundError(f"Translation map not found at {self.map_file_path}")
        with open(self.map_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, elegant_text):
        result = elegant_text
        # Sort keys by length descending to replace longer tokens first
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            concept = self.translation_map[key]
            result = result.replace(key, f"[{concept}]")
        return result

if __name__ == "__main__":
    map_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"
    translator = ElegantTranslator(map_path)
    sample_text = "システム起動 ~* +! データを転送 -> 新たな価値を創出 =#"
    decoded = translator.decode(sample_text)
    print("Decoded Output:", decoded)
