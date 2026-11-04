import sys
import os
import json
import traceback

class ElegantTranslator:
    def __init__(self, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
        self.map_path = map_path
        self.translation_map = self.load_map()

    def load_map(self):
        try:
            if not os.path.exists(self.map_path):
                return {}
            with open(self.map_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading translation map: {e}", file=sys.stderr)
            return {}

    def decode(self, text: str) -> str:
        try:
            sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
            decoded_text = text
            for key in sorted_keys:
                value = self.translation_map[key]
                decoded_text = decoded_text.replace(key, value)
            return decoded_text
        except Exception as e:
            print(f"Error during decoding: {e}", file=sys.stderr)
            return text

def translate_string(text: str) -> str:
    translator = ElegantTranslator()
    return translator.decode(text)

if __name__ == "__main__":
    sample_text = "こんにちは # ~ * + -> --> 世界"
    translator = ElegantTranslator()
    result = translator.decode(sample_text)
    print("Original:", sample_text)
    print("Decoded:", result)
