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

    def decode(self, text: str) -> str:
        result = text
        for symbol, meaning in self.translation_map.items():
            result = result.replace(symbol, f"({meaning})")
        return result

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample_text = "Hello * World ~"
    print("Original:", sample_text)
    print("Decoded:", translator.decode(sample_text))
