import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            map_file_path = os.path.join(base_dir, "translation_map.json")
        
        self.map_file_path = map_file_path
        self.translation_map = self.load_map()

    def load_map(self):
        if not os.path.exists(self.map_file_path):
            return {}
        with open(self.map_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, text):
        result = text
        for symbol, description in self.translation_map.items():
            result = result.replace(symbol, f"[{description}]")
        return result

def translate_text(text, map_file_path=None):
    translator = ElegantTranslator(map_file_path)
    return translator.decode(text)

if __name__ == "__main__":
    sample_text = "システムは Δ を経て Ω に到達し、Ψ を通じて Φ を形成する Σ。"
    decoded = translate_text(sample_text)
    print("Original:", sample_text)
    print("Decoded:", decoded)
