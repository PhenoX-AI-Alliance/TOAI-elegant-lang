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

def decode_elegant_text(text, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
    try:
        translation_map = load_translation_map(map_path)
        decoded_text = text
        for symbol, meaning in translation_map.items():
            decoded_text = decoded_text.replace(symbol, f"({meaning})")
        return decoded_text
    except Exception as e:
        print(f"Error during decoding: {e}", file=sys.stderr)
        traceback.print_exc()
        raise e

if __name__ == "__main__":
    sample_text = "Gaia Ecosystem ~* starts with +! and connects <> via -> with ##."
    print("Original:", sample_text)
    try:
        result = decode_elegant_text(sample_text)
        print("Decoded:", result)
    except Exception as e:
        sys.exit(1)
