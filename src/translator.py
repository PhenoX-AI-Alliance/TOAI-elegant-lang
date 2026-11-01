import sys
import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path):
        if not os.path.exists(map_file_path):
            raise FileNotFoundError(f"Translation map not found at {map_file_path}")
        with open(map_file_path, "r", encoding="utf-8") as f:
            self.translation_map = json.load(f)
            
    def decode(self, elegant_text):
        decoded_text = elegant_text
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, value)
        return decoded_text

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(current_dir, "translation_map.json")
    translator = ElegantTranslator(map_path)
    sample_text = "Gaia ~ * # -> ()"
    print("Original:", sample_text)
    print("Decoded:", translator.decode(sample_text))
