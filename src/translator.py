import json
import os

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            map_file_path = os.path.join(os.path.dirname(__file__), "translation_map.json")
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if os.path.exists(self.map_file_path):
            with open(self.map_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def decode(self, elegant_text):
        decoded_text = elegant_text
        # Sort keys by length descending to replace multi-character symbols first (e.g. "=>" before ">")
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for symbol in sorted_keys:
            meaning = self.translation_map[symbol]
            decoded_text = decoded_text.replace(symbol, f"({meaning})")
        return decoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample_text = "Gaia * ~ @ -> => #"
    print("Original:", sample_text)
    print("Decoded:", translator.decode(sample_text))
