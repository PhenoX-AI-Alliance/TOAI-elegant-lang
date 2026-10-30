import sys
import os
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
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        decoded_text = elegant_text
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, f"[{value}]")
        return decoded_text

if __name__ == "__main__":
    map_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "translation_map.json"))
    translator = ElegantTranslator(map_path)
    sample_text = "~*#@ -> =>"
    result = translator.decode(sample_text)
    print("Decoded Result:", result)
