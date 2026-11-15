import sys
import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            map_file_path = os.path.join(current_dir, "translation_map.json")
        
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_file_path):
            raise FileNotFoundError(f"Translation map not found at: {self.map_file_path}")
        with open(self.map_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, text: str) -> str:
        result = text
        for symbol, meaning in self.translation_map.items():
            result = result.replace(symbol, f"[{meaning}]")
        return result

def decode_elegant_text(text: str, map_file_path: str = None) -> str:
    translator = ElegantTranslator(map_file_path)
    return translator.decode(text)

if __name__ == "__main__":
    sample_text = "Ωの世界で∞の愛と∇を統合するΨ"
    try:
        decoded = decode_elegant_text(sample_text)
        print(f"Original: {sample_text}")
        print(f"Decoded: {decoded}")
    except Exception as e:
        print(f"Error during translation: {e}", file=sys.stderr)
        sys.exit(1)
