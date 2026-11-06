import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        return {}
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def translate_elegant_text(text, map_path):
    t_map = load_translation_map(map_path)
    sorted_keys = sorted(t_map.keys(), key=len, reverse=True)
    
    result = text
    for key in sorted_keys:
        value = t_map[key]
        result = result.replace(key, f"({value})")
    return result

if __name__ == "__main__":
    sample = "Gaia Ecosystem * ~ -> #"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    m_path = os.path.join(current_dir, "translation_map.json")
    print("Original:", sample)
    print("Translated:", translate_elegant_text(sample, m_path))
