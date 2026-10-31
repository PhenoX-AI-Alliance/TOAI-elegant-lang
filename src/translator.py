import sys
import os
import json

class ElegantTranslator:
    def __init__(self, map_path):
        self.map_path = map_path
        self.translation_map = self.load_map()

    def load_map(self):
        if not os.path.exists(self.map_path):
            raise FileNotFoundError(f"Translation map not found at {self.map_path}")
        with open(self.map_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, text):
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        result = text
        for key in sorted_keys:
            value = self.translation_map[key]
            result = result.replace(key, f"[{value}]")
        return result

def translate_elegant_text(text, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
    translator = ElegantTranslator(map_path)
    return translator.decode(text)

if __name__ == "__main__":
    sample_text = "Gaia * ~ -> # ecosystem"
    decoded = translate_elegant_text(sample_text)
    print(f"Original: {sample_text}")
    print(f"Decoded: {decoded}")
