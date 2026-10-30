import os
import json

class ElegantTranslator:
    def __init__(self, map_path=None):
        if map_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            map_path = os.path.join(current_dir, "translation_map.json")
        
        self.map_path = map_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_path):
            return {}
        with open(self.map_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, text):
        decoded_text = text
        # 長いキーから先に置換するためのソート
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, f"({value})")
        return decoded_text

def decode_elegant_text(text):
    translator = ElegantTranslator()
    return translator.decode(text)

if __name__ == "__main__":
    sample = "Hello ~* and +! -> world =*"
    print("Original:", sample)
    print("Decoded:", decode_elegant_text(sample))
