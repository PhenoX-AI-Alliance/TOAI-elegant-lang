import sys
import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path=None):
    if map_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        map_path = os.path.join(current_dir, "translation_map.json")
    
    trans_map = load_translation_map(map_path)
    
    sorted_keys = sorted(trans_map.keys(), key=len, reverse=True)
    
    decoded_text = text
    for key in sorted_keys:
        value = trans_map[key]
        decoded_text = decoded_text.replace(key, f"[{value}]")
        
    return decoded_text

if __name__ == "__main__":
    sample = "Hello * ~ # -> !"
    print("Original:", sample)
    print("Decoded:", decode_elegant_text(sample))
