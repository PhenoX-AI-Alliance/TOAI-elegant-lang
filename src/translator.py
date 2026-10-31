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
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        decoded_text = text
        for key in sorted_keys:
            replacement = f"[{self.translation_map[key]}]"
            decoded_text = decoded_text.replace(key, replacement)
        return decoded_text

if __name__ == "__main__":
    t = ElegantTranslator()
    sample = "Gaia ~ * -> ++ #"
    print("Original:", sample)
    print("Decoded:", t.decode(sample))
