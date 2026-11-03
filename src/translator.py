import os
import json

class ElegantTranslator:
    def __init__(self, map_path=None):
        if map_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            map_path = os.path.join(current_dir, "translation_map.json")
        
        self.map_path = map_path
        self.load_map()

    def load_map(self):
        if os.path.exists(self.map_path):
            with open(self.map_path, "r", encoding="utf-8") as f:
                self.translation_map = json.load(f)
        else:
            self.translation_map = {}

    def decode(self, text: str) -> str:
        decoded_text = text
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, f"({value})")
        return decoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample_text = "生命の地球 ~ * # @ -> ++"
    result = translator.decode(sample_text)
    print("Original:", sample_text)
    print("Decoded:", result)
