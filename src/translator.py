import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        return {}
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path):
    trans_map = load_translation_map(map_path)
    sorted_keys = sorted(trans_map.keys(), key=len, reverse=True)
    
    decoded_text = text
    for key in sorted_keys:
        value = trans_map[key]
        decoded_text = decoded_text.replace(key, f"({value})")
    return decoded_text

if __name__ == "__main__":
    sample_text = "こんにちは ~ 世界 * 命の地球 #"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_file = os.path.join(current_dir, "translation_map.json")
    result = decode_elegant_text(sample_text, map_file)
    print("Decoded Result:", result)
