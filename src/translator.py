import os
import json

class ElegantTranslator:
    def __init__(self, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
        self.map_path = map_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_path):
            return {}
        with open(self.map_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, text):
        result = text
        for symbol, description in sorted(self.translation_map.items(), key=lambda x: len(x[0]), reverse=True):
            result = result.replace(symbol, f"({description})")
        return result

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample = "~ * # -> |>"
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
