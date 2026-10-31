import json
import os

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
        result = text
        for symbol, meaning in self.translation_map.items():
            result = result.replace(symbol, f"({meaning})")
        return result

def decode_elegant_text(text: str, map_path=None) -> str:
    translator = ElegantTranslator(map_path)
    return translator.decode(text)
