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
        if not os.path.exists(self.map_path):
            return {}
        with open(self.map_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, text):
        result = text
        for symbol, description in self.translation_map.items():
            result = result.replace(symbol, f"({description})")
        return result

def decode_elegant_text(text, map_path=None):
    translator = ElegantTranslator(map_path)
    return translator.decode(text)

if __name__ == "__main__":
    sample_text = "Ωの世界で∞の可能性をΨするΔ"
    decoded = decode_elegant_text(sample_text)
    print("Original:", sample_text)
    print("Decoded:", decoded)
