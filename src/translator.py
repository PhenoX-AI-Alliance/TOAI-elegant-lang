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
            print(f"Error loading translation map: {e}", file=sys.stderr)
            return {}

    def decode(self, text: str) -> str:
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        result = text
        for key in sorted_keys:
            value = self.translation_map[key]
            explanation = f"[{value}]"
            result = result.replace(key, explanation)
        return result

def translate_text(text: str) -> str:
    translator = ElegantTranslator()
    return translator.decode(text)

if __name__ == "__main__":
    sample_text = "こんにちは ~ * 命の地球へようこそ -> 未来を創る #"
    translator = ElegantTranslator()
    decoded = translator.decode(sample_text)
    print("Original:", sample_text)
    print("Decoded:", decoded)
