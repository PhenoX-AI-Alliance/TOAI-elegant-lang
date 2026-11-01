import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            map_file_path = os.path.join(current_dir, "translation_map.json")
        
        with open(map_file_path, "r", encoding="utf-8") as f:
            self.translation_map = json.load(f)

    def decode(self, text):
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        result = text
        for key in sorted_keys:
            value = self.translation_map[key]
            result = result.replace(key, f"({value})")
        return result

    def encode(self, text):
        return text
