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
        decoded_text = text
        for symbol, explanation in self.translation_map.items():
            decoded_text = decoded_text.replace(symbol, explanation)
        return decoded_text

def translate_elegant_text(text, map_file_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
    translator = ElegantTranslator(map_file_path)
    return translator.decode(text)
