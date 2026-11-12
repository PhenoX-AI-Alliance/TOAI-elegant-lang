import sys
import os
import json

class ElegantTranslator:
    def __init__(self, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
        self.map_path = map_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_path):
            raise FileNotFoundError(f"Translation map not found at {self.map_path}")
        with open(self.map_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, text: str) -> str:
        result = text
        for symbol, description in self.translation_map.items():
            result = result.replace(symbol, f"[{description}]")
        return result

    def encode(self, text: str) -> str:
        result = text
        sorted_items = sorted(self.translation_map.items(), key=lambda x: len(x[1]), reverse=True)
        for symbol, description in sorted_items:
            result = result.replace(f"[{description}]", symbol)
        return result

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample_text = "✧の力で✦を実現し、✤を守る⟡。"
    decoded = translator.decode(sample_text)
    print("Decoded:", decoded)
