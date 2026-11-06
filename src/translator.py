import os
import json

class ElegantTranslator:
    def __init__(self, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
        self.map_path = map_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if os.path.exists(self.map_path):
            with open(self.map_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def decode(self, text):
        result = text
        # Sort keys by length descending to replace multi-character symbols first (e.g., "->")
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            replacement = f"[{self.translation_map[key]}]"
            result = result.replace(key, replacement)
        return result

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample = "Hello ~ world * + -> # eco"
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
