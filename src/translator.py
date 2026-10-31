import sys
import os
import json

class ElegantTranslator:
    def __init__(self, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
        self.map_path = map_path
        self.translation_map = self.load_map()

    def load_map(self):
        if not os.path.exists(self.map_path):
            return {}
        try:
            with open(self.map_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading translation map: {e}", file=sys.stderr)
            return {}

    def decode(self, text):
        if not isinstance(text, str):
            return text
        
        # Sort keys by length descending to prevent partial replacements of compound symbols (e.g. '->' before '-')
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        
        decoded_text = text
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, f"({value})")
            
        return decoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample_text = "# * ~ -> => ++"
    print("Original:", sample_text)
    print("Decoded:", translator.decode(sample_text))
