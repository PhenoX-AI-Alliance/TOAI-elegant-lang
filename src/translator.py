import sys
import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path):
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_file_path):
            return {}
        try:
            with open(self.map_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading translation map: {{e}}")
            return {}

    def decode(self, text):
        if not isinstance(text, str):
            return ""
        
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        decoded_text = text
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, f"{{value}}")
        
        return decoded_text

if __name__ == "__main__":
    map_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "translation_map.json"))
    translator = ElegantTranslator(map_path)
    
    sample_text = "生命の地球 * ~ 豊かな未来へ -> []"
    result = translator.decode(sample_text)
    print("Original:", sample_text)
    print("Decoded :", result)
