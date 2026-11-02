import json
import os

class ElegantTranslator:
    def __init__(self, map_file_path):
        self.map_file_path = map_file_path
        self.translation_map = self.load_map()

    def load_map(self):
        if not os.path.exists(self.map_file_path):
            return {}
        with open(self.map_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, elegant_text):
        decoded_text = elegant_text
        for symbol, description in self.translation_map.items():
            decoded_text = decoded_text.replace(symbol, f"({description})")
        return decoded_text

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(current_dir, "translation_map.json")
    translator = ElegantTranslator(map_path)
    sample_code = "~ * > + #"
    print("Original:", sample_code)
    print("Decoded:", translator.decode(sample_code))
