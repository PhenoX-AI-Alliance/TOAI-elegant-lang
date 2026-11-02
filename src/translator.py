import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            self.map_file_path = os.path.join(os.path.dirname(__file__), "translation_map.json")
        else:
            self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if os.path.exists(self.map_file_path):
            with open(self.map_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def decode(self, text):
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        decoded_text = text
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, value)
        return decoded_text

    def encode(self, text):
        reverse_map = {v: k for k, v in self.translation_map.items()}
        sorted_keys = sorted(reverse_map.keys(), key=len, reverse=True)
        encoded_text = text
        for key in sorted_keys:
            value = reverse_map[key]
            encoded_text = encoded_text.replace(key, value)
        return encoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample = "こんにちは ~ と * が # で @ につなぐ ->"
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
