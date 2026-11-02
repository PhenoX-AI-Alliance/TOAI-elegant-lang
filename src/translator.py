import json
import os

class ElegantTranslator:
    def __init__(self, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
        self.map_path = map_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if os.path.exists(self.map_path):
            try:
                with open(self.map_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load translation map: {e}")
        return {}

    def decode(self, text: str) -> str:
        decoded_text = text
        # Sort keys by length descending to replace longer tokens first (e.g., => before =)
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, f"[{value}]")
        return decoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample = "Gaia ~ * # -> =>"
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
