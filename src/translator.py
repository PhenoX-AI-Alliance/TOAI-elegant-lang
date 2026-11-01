import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            self.map_file_path = os.path.join(
                os.path.dirname(__file__),
                "translation_map.json"
            )
        else:
            self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if os.path.exists(self.map_file_path):
            with open(self.map_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def decode(self, text: str) -> str:
        decoded_text = text
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, f"[{value}]")
        return decoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample_text = "~Hello * World -> #"
    print("Original:", sample_text)
    print("Decoded:", translator.decode(sample_text))
