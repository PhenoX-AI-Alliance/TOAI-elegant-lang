import json
import os

class ElegantTranslator:
    def __init__(self, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
        self.map_path = map_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if os.path.exists(self.map_path):
            try:
                with open(self.map_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def decode(self, text):
        if not isinstance(text, str):
            return ""
        result = text
        for symbol, meaning in self.translation_map.items():
            result = result.replace(symbol, f"({meaning})")
        return result

def decode_elegant_text(text):
    translator = ElegantTranslator()
    return translator.decode(text)

if __name__ == "__main__":
    sample = "~Hello * World > Gaia #"
    translator = ElegantTranslator()
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
