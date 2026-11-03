import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if os.path.exists(self.map_file_path):
            with open(self.map_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def decode(self, text):
        decoded_text = text
        # Sort keys by length descending to replace multi-character symbols first (e.g., "->" before "-")
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for symbol in sorted_keys:
            explanation = self.translation_map[symbol]
            decoded_text = decoded_text.replace(symbol, f"({explanation})")
        return decoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample_text = "# Gaia ecosystem ~ shines * with care -> future ++"
    print("Original:", sample_text)
    print("Decoded:", translator.decode(sample_text))
