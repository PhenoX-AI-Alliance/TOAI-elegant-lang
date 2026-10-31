import sys
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

    def decode(self, text):
        if not isinstance(text, str):
            return text
        decoded_text = text
        for symbol, description in self.translation_map.items():
            decoded_text = decoded_text.replace(symbol, f"[{description}]")
        return decoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample_text = "こんにちは ~* 世界。 =+ 素晴らしい未来へ向かって進もう ->"
    print("Original:", sample_text)
    print("Decoded:", translator.decode(sample_text))
