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
            return ""
        result = text
        # Sort keys by length descending to replace longer tokens first
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            value = self.translation_map[key]
            result = result.replace(key, value)
        return result

def decode_elegant_text(text):
    translator = ElegantTranslator()
    return translator.decode(text)

if __name__ == "__main__":
    sample = "こんにちは ~* +! ->"
    translator = ElegantTranslator()
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
