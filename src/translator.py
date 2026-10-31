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
    translation_map = load_translation_map(map_path)
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    
    decoded_text = text
    for key in sorted_keys:
        value = translation_map[key]
        explanation = f"[{key}: {value}]"
        decoded_text = decoded_text.replace(key, explanation)
        
    return decoded_text

if __name__ == "__main__":
    sample_text = "こんにちは ~ 世界 * 命の地球 # 未来へ -> 到達 => 善の収益化"
    try:
        result = decode_elegant_text(sample_text)
        print("Decoded Result:")
        print(result)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
