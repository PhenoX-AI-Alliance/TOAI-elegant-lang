import os
import json

class ElegantTranslator:
    def __init__(self, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
        self.map_path = map_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_path):
            return {}
        try:
            with open(self.map_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading translation map: {e}")
            return {}

    def decode(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        result = text
        for symbol, description in self.translation_map.items():
            result = result.replace(symbol, f"({description})")
        return result

def translate_text(text: str) -> str:
    translator = ElegantTranslator()
    return translator.decode(text)

if __name__ == "__main__":
    sample = "こんにちは~ *の世界へようこそ # @ >"
    translator = ElegantTranslator()
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
