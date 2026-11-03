import os
import json
import sys

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
        result = text
        # Sort keys by length descending to replace longer tokens first
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            value = self.translation_map[key]
            result = result.replace(key, f"[{value}]")
        return result

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample_text = "Hello ~* -> <=> #+ ?!"
    decoded = translator.decode(sample_text)
    print(decoded)
