import os
import json

class ElegantTranslator:
    def __init__(self, map_path=None):
        if map_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            map_path = os.path.join(current_dir, "translation_map.json")
        
        with open(map_path, "r", encoding="utf-8") as f:
            self.translation_map = json.load(f)

    def decode(self, text: str) -> str:
        result = text
        for symbol, meaning in self.translation_map.items():
            result = result.replace(symbol, f"({meaning})")
        return result

def decode_elegant_text(text: str) -> str:
    translator = ElegantTranslator()
    return translator.decode(text)

if __name__ == "__main__":
    sample = "~ 命の地球 * 未来への架け橋 #"
    print("Original:", sample)
    print("Decoded:", decode_elegant_text(sample))
