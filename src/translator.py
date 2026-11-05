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

    def decode(self, text: str) -> str:
        result = text
        for symbol, meaning in self.translation_map.items():
            result = result.replace(symbol, f"({meaning})")
        return result

def translate_elegant_text(text: str) -> str:
    translator = ElegantTranslator()
    return translator.decode(text)

if __name__ == "__main__":
    sample = "こんにちは ~ 世界 * 地球 # 命 @"
    print("Original:", sample)
    print("Decoded:", translate_elegant_text(sample))
