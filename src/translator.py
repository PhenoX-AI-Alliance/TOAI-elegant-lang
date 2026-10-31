import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            map_file_path = os.path.join(base_dir, "translation_map.json")
        
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_file_path):
            return {}
        try:
            with open(self.map_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading translation map: {e}")
            return {}

    def decode(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        
        decoded_text = text
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, f"({value})")
            
        return decoded_text

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample = "こんにちは ~ * 毎回感謝を込めて -> 未来へ"
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
