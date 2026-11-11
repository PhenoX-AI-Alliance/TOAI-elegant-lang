import json
import os

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
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        result = text
        for key in sorted_keys:
            replacement = self.translation_map[key]
            result = result.replace(key, replacement)
        return result

    def encode(self, text):
        reverse_map = {v: k for k, v in self.translation_map.items()}
        sorted_keys = sorted(reverse_map.keys(), key=len, reverse=True)
        result = text
        for key in sorted_keys:
            replacement = reverse_map[key]
            result = result.replace(key, replacement)
        return result

if __name__ == "__main__":
    t = ElegantTranslator()
    sample = "Hello ~ * # -> => World"
    decoded = t.decode(sample)
    print("Decoded:", decoded)
