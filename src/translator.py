# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

class ElegantTranslator:
    def __init__(self, map_file_path=None):
        if map_file_path is None:
            base_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
            map_file_path = os.path.join(base_dir, "src", "translation_map.json")
        
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_file_path):
            raise FileNotFoundError(f"Translation map not found at {self.map_file_path}")
        with open(self.map_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, text: str) -> str:
        result = []
        for char in text:
            if char in self.translation_map:
                result.append(f"[{self.translation_map[char]}]")
            else:
                result.append(char)
        return "".join(result)

    def encode(self, text: str) -> str:
        reverse_map = {v: k for k, v in self.translation_map.items()}
        sorted_keys = sorted(reverse_map.keys(), key=len, reverse=True)
        
        decoded_text = text
        for key in sorted_keys:
            symbol = reverse_map[key]
            decoded_text = decoded_text.replace(f"[{key}]", symbol)
        return decoded_text

if __name__ == "__main__":
    try:
        translator = ElegantTranslator()
        sample_text = "~ ! @ #"
        decoded = translator.decode(sample_text)
        print("Original:", sample_text)
        print("Decoded:", decoded)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
