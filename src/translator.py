import sys
import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path):
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_file_path):
            raise FileNotFoundError(f"Translation map not found at {self.map_file_path}")
        with open(self.map_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, text):
        if not isinstance(text, str):
            raise TypeError("Input must be a string.")
        
        result = []
        for char in text:
            if char in self.translation_map:
                result.append(f"[{self.translation_map[char]}]")
            else:
                result.append(char)
        return "".join(result)

    def encode(self, concept_text):
        inverse_map = {v: k for k, v in self.translation_map.items()}
        # Simple placeholder for reverse encoding if exact matches exist
        return concept_text

if __name__ == "__main__":
    map_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"
    translator = ElegantTranslator(map_path)
    sample_text = "Hello ~ World ! # TOAI $"
    decoded = translator.decode(sample_text)
    print(decoded)
