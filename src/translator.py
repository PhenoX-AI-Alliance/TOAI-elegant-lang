import sys
import os
import traceback
import time
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def translate_elegant_text(text, map_path):
    trans_map = load_translation_map(map_path)
    # Sort keys by length descending to match longer symbols first
    sorted_keys = sorted(trans_map.keys(), key=len, reverse=True)
    
    result = text
    for key in sorted_keys:
        value = trans_map[key]
        result = result.replace(key, f"[{value}]")
    return result

if __name__ == "__main__":
    map_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"
    sample_text = "~* 命の地球システム起動 ++ 意識の共有 -> すべての存在へ *~"
    try:
        translated = translate_elegant_text(sample_text, map_path)
        print("Original:", sample_text)
        print("Translated:", translated)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
