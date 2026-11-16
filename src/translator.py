# -*- coding: utf-8 -*-
import sys
import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path):
    trans_map = load_translation_map(map_path)
    result = text
    for symbol, description in trans_map.items():
        result = result.replace(symbol, f"[{description}]")
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python translator.py '<elegant_text>'")
        sys.exit(1)
    
    target_text = sys.argv[1]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_file = os.path.join(current_dir, "translation_map.json")
    
    try:
        decoded = decode_elegant_text(target_text, map_file)
        print("Decoded Output:", decoded)
    except Exception as e:
        print("Error during translation:", str(e), file=sys.stderr)
        sys.exit(1)
