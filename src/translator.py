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
        for symbol, meaning in self.translation_map.items():
            result = result.replace(symbol, f"({meaning})")
        return result

    def encode(self, text):
        result = text
        for symbol, meaning in self.translation_map.items():
            result = result.replace(f"({meaning})", symbol)
        return result

if __name__ == "__main__":
    t = ElegantTranslator()
    sample = "こんにちは ~ 世界 *"
    print("Original:", sample)
    decoded = t.decode(sample)
    print("Decoded:", decoded)
