import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path):
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_file_path):
            return {}
        with open(self.map_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, elegant_text):
        decoded_text = elegant_text
        # Sort keys by length descending to replace longer tokens first (e.g., '->' before '>')
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, f"[{value}]")
        return decoded_text

if __name__ == "__main__":
    import sys
    path = os.path.join(os.path.dirname(__file__), "translation_map.json")
    translator = ElegantTranslator(path)
    if len(sys.argv) > 1:
        text = sys.argv[1]
        print(translator.decode(text))
    else:
        print("ElegantTranslator initialized successfully.")
