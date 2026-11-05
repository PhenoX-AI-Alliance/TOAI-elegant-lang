import json
import os

class ElegantTranslator:
    def __init__(self, map_path=None):
        if map_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            map_path = os.path.join(current_dir, "translation_map.json")
        
        with open(map_path, "r", encoding="utf-8") as f:
            self.translation_map = json.load(f)

    def decode(self, text: str) -> str:
        result = []
        i = 0
        length = len(text)
        while i < length:
            char = text[i]
            if char in self.translation_map:
                result.append(f"[{self.translation_map[char]}]")
            else:
                result.append(char)
            i += 1
        return "".join(result)

    def encode(self, text: str) -> str:
        reverse_map = {v: k for k, v in self.translation_map.items()}
        sorted_keys = sorted(reverse_map.keys(), key=len, reverse=True)
        
        encoded_text = text
        for key in sorted_keys:
            encoded_text = encoded_text.replace(f"[{key}]", reverse_map[key])
        return encoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample = "Hello * World + Peace -"
    decoded = translator.decode(sample)
    print("Decoded:", decoded)