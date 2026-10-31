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

    def decode(self, text):
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        decoded_text = text
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, value)
        return decoded_text

    def encode_concept(self, text):
        inverse_map = {v: k for k, v in self.translation_map.items()}
        sorted_values = sorted(inverse_map.keys(), key=len, reverse=True)
        encoded_text = text
        for val in sorted_values:
            key = inverse_map[val]
            encoded_text = encoded_text.replace(val, key)
        return encoded_text

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
        map_path = os.path.join(os.path.dirname(__file__), "translation_map.json")
        translator = ElegantTranslator(map_path)
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(translator.decode(content))
    else:
        print("ElegantTranslator initialized successfully.")
