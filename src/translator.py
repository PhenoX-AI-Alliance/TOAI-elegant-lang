# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def load_translation_map(map_file_path):
    if not os.path.exists(map_file_path):
        raise FileNotFoundError(f"Translation map not found at {map_file_path}")
    with open(map_file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, translation_map):
    decoded_text = text
    # Sort keys by length descending to prevent partial replacements of compound symbols
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    for key in sorted_keys:
        value = translation_map[key]
        decoded_text = decoded_text.replace(key, f"[{value}]")
    return decoded_text

if __name__ == "__main__":
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        map_file = os.path.join(base_dir, "translation_map.json")
        t_map = load_translation_map(map_file)
        
        sample_text = "生命の地球 ~ * 共に歩む -> @"
        result = decode_elegant_text(sample_text, t_map)
        print("Original:", sample_text)
        print("Decoded :", result)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
