import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            map_file_path = os.path.join(base_dir, "translation_map.json")
        
        self.map_file_path = map_file_path
        self.load_map()

    def load_map(self):
        if os.path.exists(self.map_file_path):
            with open(self.map_file_path, "r", encoding="utf-8") as f:
                self.translation_map = json.load(f)
        else:
            self.translation_map = {}

    def decode(self, text):
        if not isinstance(text, str):
            return ""
        
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        decoded_text = text
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, f"[{value}]")
        return decoded_text

def translate_text(text):
    translator = ElegantTranslator()
    return translator.decode(text)

if __name__ == "__main__":
    sample = "Hello ~ * World # @ -> +"
    translator = ElegantTranslator()
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
