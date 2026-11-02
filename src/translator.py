import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path):
    translation_map = load_translation_map(map_path)
    decoded_text = text
    # Sort keys by length descending to prevent partial replacements
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    for key in sorted_keys:
        value = translation_map[key]
        decoded_text = decoded_text.replace(key, f"[{value}]")
    return decoded_text

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_file = os.path.join(current_dir, "translation_map.json")
    sample_text = "こんにちは ~* 世界 +* 愛と平和 #@"
    result = decode_elegant_text(sample_text, map_file)
    print("Decoded result:", result)
