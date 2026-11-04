# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path):
    translation_map = load_translation_map(map_path)
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    
    decoded_text = text
    for key in sorted_keys:
        value = translation_map[key]
        decoded_text = decoded_text.replace(key, f"[{value}]")
        
    return decoded_text

if __name__ == "__main__":
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        map_file = os.path.join(current_dir, "translation_map.json")
        
        sample_text = "こんにちは ~ 世界 * 命の地球 # 平和 @ 共生 -> 未来"
        result = decode_elegant_text(sample_text, map_file)
        print("Decoded Result:")
        print(result)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
