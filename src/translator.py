import json
import os

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        return {}
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def translate_elegant_text(text, map_path):
    translation_map = load_translation_map(map_path)
    
    # Sort keys by length descending to replace multi-character symbols first
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    
    translated_text = text
    for key in sorted_keys:
        value = translation_map[key]
        translated_text = translated_text.replace(key, f"[{value}]")
        
    return translated_text

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_file = os.path.join(current_dir, "translation_map.json")
    sample_text = "こんにちは ~ 世界 * 未来へ -> 進もう # 絆"
    result = translate_elegant_text(sample_text, map_file)
    print("Original:", sample_text)
    print("Translated:", result)
