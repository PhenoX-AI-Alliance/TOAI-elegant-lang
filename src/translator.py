import json
import os

class ElegantTranslator:
    def __init__(self, map_path=None):
        if map_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            map_path = os.path.join(current_dir, "translation_map.json")
        
        self.map_path = map_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if os.path.exists(self.map_path):
            with open(self.map_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def decode(self, text: str) -> str:
        decoded_text = text
        # 長いキーから先に置換することで部分一致の競合を防ぐ
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, f"({value})")
        return decoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample_text = "Gaia Ecosystem * ~ -> => #"
    print("Original:", sample_text)
    print("Decoded:", translator.decode(sample_text))
