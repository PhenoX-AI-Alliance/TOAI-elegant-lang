import os
import json

class ElegantTranslator:
    def __init__(self, map_path=None):
        if map_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            map_path = os.path.join(base_dir, "translation_map.json")
        
        self.map_path = map_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_path):
            return {}
        try:
            with open(self.map_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading translation map: {e}")
            return {}

    def decode(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        
        result = text
        # 長いキーから先に置換するなどの配慮が必要であればソートする
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            value = self.translation_map[key]
            explanation = f"[{value}]"
            result = result.replace(key, explanation)
            
        return result

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample = "こんにちは~ *の世界へようこそ #>+"
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
