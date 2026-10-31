import json
import os

class ElegantTranslator:
    def __init__(self, map_path=None):
        if map_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            map_path = os.path.join(base_dir, "translation_map.json")
        
        self.map_path = map_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_path):
            return {}
        with open(self.map_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, text):
        decoded_text = text
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            value = self.translation_map[key]
            explanation = f"[{value}]"
            decoded_text = decoded_text.replace(key, explanation)
        return decoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample_text = "Gaia ~ * # -> +"
    print("Original:", sample_text)
    print("Decoded:", translator.decode(sample_text))
