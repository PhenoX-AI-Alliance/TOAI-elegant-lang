import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            map_file_path = os.path.join(base_dir, "translation_map.json")
        
        with open(map_file_path, "r", encoding="utf-8") as f:
            self.translation_map = json.load(f)

    def decode(self, text):
        decoded_text = text
        for symbol, description in self.translation_map.items():
            decoded_text = decoded_text.replace(symbol, f"[{description}]")
        return decoded_text

    def encode(self, text):
        encoded_text = text
        for symbol, description in self.translation_map.items():
            encoded_text = encoded_text.replace(f"[{description}]", symbol)
        return encoded_text

def translate_elegant_code(text):
    translator = ElegantTranslator()
    return translator.decode(text)
