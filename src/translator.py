# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at: {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path):
    try:
        translation_map = load_translation_map(map_path)
        sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
        decoded_text = text
        for key in sorted_keys:
            replacement = f"[{translation_map[key]}]"
            decoded_text = decoded_text.replace(key, replacement)
        return decoded_text
    except Exception as e:
        print(f"Error during decoding: {e}", file=sys.stderr)
        traceback.print_exc()
        raise e

if __name__ == "__main__":
    map_path = os.path.join(os.path.dirname(__file__), "translation_map.json")
    sample_text = "Hello ~ world * this is # TOAI @ ecosystem -> ++"
    print("Original:", sample_text)
    try:
        result = decode_elegant_text(sample_text, map_path)
        print("Decoded:", result)
    except Exception:
        sys.exit(1)
