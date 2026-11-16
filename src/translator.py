# -*- coding: utf-8 -*-
import sys
import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def decode_elegant_text(text, map_path):
    translation_map = load_translation_map(map_path)
    decoded_parts = []
    for char in text:
        if char in translation_map:
            decoded_parts.append(f"[{translation_map[char]}]")
        else:
            decoded_parts.append(char)
    return "".join(decoded_parts)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(current_dir, 'translation_map.json')
    
    sample_text = "Hello ~ and * ! Welcome to #@"
    print(f"Original: {sample_text}")
    try:
        result = decode_elegant_text(sample_text, map_path)
        print(f"Decoded: {result}")
    except Exception as e:
        print(f"Error during decoding: {e}", file=sys.stderr)
        sys.exit(1)
