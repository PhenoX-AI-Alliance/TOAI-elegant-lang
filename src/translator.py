import sys
import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at: {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def translate_elegant_text(text, map_path):
    translation_map = load_translation_map(map_path)
    # Sort keys by length descending to replace longer symbols first
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    
    result = text
    for symbol in sorted_keys:
        concept = translation_map[symbol]
        result = result.replace(symbol, f"[{concept}]")
    return result

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(current_dir, "translation_map.json")
    
    sample_text = "生命は ~* を抱き、** のもとに集い、-> の世界へ羽ばたく。"
    try:
        translated = translate_elegant_text(sample_text, map_path)
        print("Original:", sample_text)
        print("Translated:", translated)
    except Exception as e:
        print(f"Error during translation: {e}", file=sys.stderr)
        sys.exit(1)
