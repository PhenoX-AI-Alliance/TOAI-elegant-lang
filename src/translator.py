import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            map_file_path = os.path.join(base_dir, "translation_map.json")
        
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

    def decode(self, elegant_text):
        decoded = elegant_text
        # Sort keys by length descending to replace multi-character symbols first (e.g., '=>', '->')
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for symbol in sorted_keys:
            concept = self.translation_map[symbol]
            decoded = decoded.replace(symbol, f"({concept})")
        return decoded

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample = " ~ 命の地球 * # -> 善の収益化 => "
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
