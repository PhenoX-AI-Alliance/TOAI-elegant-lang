import json
import os

class ElegantTranslator:
    def __init__(self, map_file_path):
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_file_path):
            return {}
        with open(self.map_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, text):
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        result = text
        for key in sorted_keys:
            value = self.translation_map[key]
            result = result.replace(key, f"({value})")
        return result

def translate_elegant_text(text, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
    translator = ElegantTranslator(map_path)
    return translator.decode(text)

if __name__ == "__main__":
    sample = "Gaia # * ~ -> harmony"
    print("Original:", sample)
    print("Decoded:", translate_elegant_text(sample))
