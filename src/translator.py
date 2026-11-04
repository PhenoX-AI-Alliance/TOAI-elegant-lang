import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            map_file_path = os.path.join(current_dir, "translation_map.json")
        
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_file_path):
            return {}
        try:
            with open(self.map_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading translation map: {e}")
            return {}

    def decode(self, text):
        if not isinstance(text, str):
            return ""
        decoded_text = text
        for symbol, explanation in self.translation_map.items():
            decoded_text = decoded_text.replace(symbol, f"[{explanation}]")
        return decoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample_text = "Hello ~ * World #"
    print("Original:", sample_text)
    print("Decoded:", translator.decode(sample_text))
