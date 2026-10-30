import json
import os

class ElegantTranslator:
    def __init__(self, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
        self.map_path = map_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if os.path.exists(self.map_path):
            with open(self.map_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def decode(self, text: str) -> str:
        result = text
        # 長いキーから順に置換するためにソート
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            value = self.translation_map[key]
            result = result.replace(key, f"({value})")
        return result

if __name__ == "__main__":
    translator = ElegantTranslator()
    sample = "こんにちは ~ * 友人よ # @ -> 世界を温かく"
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
