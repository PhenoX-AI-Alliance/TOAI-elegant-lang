import sys
import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def translate_elegant_text(text, map_path):
    mapping = load_translation_map(map_path)
    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
    
    translated_text = text
    for key in sorted_keys:
        value = mapping[key]
        translated_text = translated_text.replace(key, f"[{value}]")
        
    return translated_text

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(current_dir, "translation_map.json")
    
    sample_text = "こんにちは ~* 世界。 ** と ## が交差するとき、 ++ が生まれ、 -- が訪れる。"
    try:
        result = translate_elegant_text(sample_text, map_path)
        print("Original:", sample_text)
        print("Translated:", result)
    except Exception as e:
        print(f"Error during translation: {e}", file=sys.stderr)
        sys.exit(1)
