import sys
import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def translate_elegant_text(text, map_path):
    trans_map = load_translation_map(map_path)
    result = text
    for symbol, meaning in trans_map.items():
        result = result.replace(symbol, f" [{meaning}] ")
    return result

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(current_dir, "translation_map.json")
    
    sample_text = "~Hello*World#TOAI@"
    print("Original:", sample_text)
    translated = translate_elegant_text(sample_text, map_path)
    print("Translated:", translated)
