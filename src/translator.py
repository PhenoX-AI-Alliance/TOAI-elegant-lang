import json
import os
import sys

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            map_file_path = os.path.join(current_dir, 'translation_map.json')
        
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_file_path):
            raise FileNotFoundError(f"Translation map not found at {self.map_file_path}")
        with open(self.map_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def decode(self, text):
        decoded_text = text
        # Sort keys by length descending to replace longer symbols first if any overlap
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for symbol in sorted_keys:
            meaning = self.translation_map[symbol]
            decoded_text = decoded_text.replace(symbol, f"[{meaning}]")
        return decoded_text

    def encode(self, text):
        # Inverse mapping approximation or direct lookup if needed
        encoded_text = text
        for symbol, meaning in self.translation_map.items():
            encoded_text = encoded_text.replace(meaning, symbol)
        return encoded_text

if __name__ == '__main__':
    translator = ElegantTranslator()
    sample_text = "Ωの世界で∞の愛とΨを具現化するΦ。"
    result = translator.decode(sample_text)
    print("Original:", sample_text)
    print("Decoded:", result)
