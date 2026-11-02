import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        return {}
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def translate_elegant_text(text, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
    translation_map = load_translation_map(map_path)
    
    # Sort keys by length descending to replace longer tokens first (e.g. "=>" before ">")
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    
    translated_text = text
    for key in sorted_keys:
        value = translation_map[key]
        translated_text = translated_text.replace(key, f"[{value}]")
        
    return translated_text

if __name__ == "__main__":
    sample_text = "Gaia Ecosystem ~ active * # -> sustainable => success"
    result = translate_elegant_text(sample_text)
    print("Original:", sample_text)
    print("Translated:", result)
