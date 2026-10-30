import json
import os

class ElegantTranslator:
    def __init__(self, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
        self.map_path = map_path
        self.translation_map = self.load_map()

    def load_map(self):
        if os.path.exists(self.map_path):
            with open(self.map_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def decode(self, text):
        result = text
        for symbol, meaning in self.translation_map.items():
            result = result.replace(symbol, f"({meaning})")
        return result

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample = "Hello ~ * # @ +"
    print("Original:", sample)
    print("Translated:", translator.decode(sample))
