import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            map_file_path = os.path.join(base_dir, "translation_map.json")
        
        self.map_file_path = map_file_path
        self.translation_map = self.load_map()

    def load_map(self):
        if not os.path.exists(self.translation_map_file_path if hasattr(self, 'translation_map_file_path') else self.map_file_path):
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
        for symbol, description in self.translation_map.items():
            decoded_text = decoded_text.replace(symbol, f"({description})")
        return decoded_text

def translate_text(text):
    translator = ElegantTranslator()
    return translator.decode(text)

if __name__ == "__main__":
    sample = "Hello * World ~ #Toai +"
    translator = ElegantTranslator()
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
