import os
import json

class ElegantTranslator:
    def __init__(self, map_path=None):
        if map_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            map_path = os.path.join(base_dir, "translation_map.json")
        
        with open(map_path, "r", encoding="utf-8") as f:
            self.translation_map = json.load(f)

    def decode(self, text: str) -> str:
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        decoded_text = text
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, f"({value})")
        return decoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample = "こんにちは~ #* @ ->"
    print(translator.decode(sample))
