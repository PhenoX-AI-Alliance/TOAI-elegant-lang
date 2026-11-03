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
    mapping = load_translation_map(map_path)
    decoded_text = text
    for symbol, meaning in mapping.items():
        decoded_text = decoded_text.replace(symbol, f"({meaning})")
    return decoded_text

if __name__ == "__main__":
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        map_path = os.path.join(current_dir, "translation_map.json")
        
        sample_text = "~Hello *World* #Gaia @All >Future"
        result = decode_elegant_text(sample_text, map_path)
        print("Decoded Result:")
        print(result)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
