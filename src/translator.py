import sys
import os
import json
import traceback

class ElegantTranslator:
    def __init__(self, map_file_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_file_path):
            return {}
        try:
            with open(self.map_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading translation map: {e}", file=sys.stderr)
            return {}

    def decode(self, text):
        if not isinstance(text, str):
            return ""
        result = text
        for symbol, description in self.translation_map.items():
            result = result.replace(symbol, f"[{description}]")
        return result

def translate_text(text):
    translator = ElegantTranslator()
    return translator.decode(text)

if __name__ == "__main__":
    sample_text = "Hello ☆ World ◇"
    translator = ElegantTranslator()
    print(translator.decode(sample_text))
