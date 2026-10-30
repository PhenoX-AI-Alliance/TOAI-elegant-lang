import json
import os

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            map_file_path = os.path.join(current_dir, "translation_map.json")
        
        with open(map_file_path, "r", encoding="utf-8") as f:
            self.translation_map = json.load(f)

    def decode(self, text):
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        decoded_text = text
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, f"({value})")
        return decoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample = "~ Hello * World # @ ->"
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
