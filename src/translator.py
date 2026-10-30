import os
import json

class ElegantTranslator:
    def __init__(self, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
        self.map_path = map_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if os.path.exists(self.map_path):
            try:
                with open(self.map_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load translation map: {e}")
                return {}
        return {}

    def decode(self, elegant_text):
        if not isinstance(elegant_text, str):
            return ""
        
        result = elegant_text
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        
        for key in sorted_keys:
            value = self.translation_map[key]
            explanation = f"[{value}]"
            result = result.replace(key, explanation)
            
        return result

def translate_string(text):
    translator = ElegantTranslator()
    return translator.decode(text)

if __name__ == "__main__":
    sample = "Hello ~ * # +"
    print("Original:", sample)
    print("Translated:", translate_string(sample))
