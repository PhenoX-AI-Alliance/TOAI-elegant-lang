import os
import json

class ElegantTranslator:
    def __init__(self, map_path=None):
        if map_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            map_path = os.path.join(base_dir, "translation_map.json")
        
        with open(map_path, "r", encoding="utf-8") as f:
            self.translation_map = json.load(f)
            
        # Sort keys by length descending to match multi-character symbols first (e.g., "->")
        self.sorted_symbols = sorted(self.translation_map.keys(), key=len, reverse=True)

    def decode(self, text: str) -> str:
        result = text
        for symbol in self.sorted_symbols:
            meaning = self.translation_map[symbol]
            replacement = f"[{symbol}: {meaning}]"
            result = result.replace(symbol, replacement)
        return result

def decode_elegant_text(text: str, map_path=None) -> str:
    translator = ElegantTranslator(map_path)
    return translator.decode(text)

if __name__ == "__main__":
    sample = "Hello ~ * # @ -> World"
    print("Original:", sample)
    print("Decoded:", decode_elegant_text(sample))
