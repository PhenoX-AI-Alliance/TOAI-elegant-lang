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

def decode_elegant_text(text, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
    try:
        trans_map = load_translation_map(map_path)
        # 長いキーから順に置換することで誤爆を防ぐ
        sorted_keys = sorted(trans_map.keys(), key=len, reverse=True)
        decoded_text = text
        for key in sorted_keys:
            replacement = f"[{trans_map[key]}]"
            decoded_text = decoded_text.replace(key, replacement)
        return decoded_text
    except Exception as e:
        print(f"Error during decoding: {e}", file=sys.stderr)
        traceback.print_exc()
        raise

if __name__ == "__main__":
    sample_text = "Gaia ~ * # -> => &"
    print("Original:", sample_text)
    try:
        result = decode_elegant_text(sample_text)
        print("Decoded:", result)
    except Exception:
        sys.exit(1)
