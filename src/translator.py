import json
import os
import sys

class ElegantTranslator:
    def __init__(self, map_file_path):
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_file_path):
            raise FileNotFoundError(f"Translation map not found at {self.map_file_path}")
        with open(self.map_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, text):
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        decoded_text = text
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, value)
        return decoded_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python translator.py '<elegant_text>'")
        sys.exit(1)
    
    target_text = sys.argv[1]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(current_dir, "translation_map.json")
    
    translator = ElegantTranslator(map_path)
    result = translator.decode(target_text)
    print(result)
