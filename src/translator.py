import json
import os

class ElegantTranslator:
    def __init__(self, map_path):
        if not os.path.exists(map_path):
            raise FileNotFoundError(f"Translation map not found at {map_path}")
        with open(map_path, "r", encoding="utf-8") as f:
            self.translation_map = json.load(f)
        
        # Sort keys by length descending to replace longer symbols first (e.g., '=>' before '=')
        self.sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)

    def decode(self, text):
        result = text
        for key in self.sorted_keys:
            value = self.translation_map[key]
            explanation = f"[{value}]"
            result = result.replace(key, explanation)
        return result

def decode_elegant_text(text, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
    translator = ElegantTranslator(map_path)
    return translator.decode(text)

if __name__ == "__main__":
    sample_text = "Gaia ~ * # @ -> =>"
    print("Original:", sample_text)
    print("Decoded:", decode_elegant_text(sample_text))
