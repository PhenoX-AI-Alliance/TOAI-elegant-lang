import json
import os

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
        result = elegant_text
        for symbol, description in self.translation_map.items():
            result = result.replace(symbol, f"[{description}]")
        return result

def translate_text(text, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
    translator = ElegantTranslator(map_path)
    return translator.decode(text)

if __name__ == "__main__":
    sample_text = "~Hello *World* #Gaia >Altruistic -Peace"
    translated = translate_text(sample_text)
    print("Translated output:", translated)
