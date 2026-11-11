import sys
import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
    translation_map = load_translation_map(map_path)
    # Sort keys by length descending to match multi-character symbols first (e.g. '=>' before '=')
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    
    decoded_text = text
    for symbol in sorted_keys:
        meaning = translation_map[symbol]
        decoded_text = decoded_text.replace(symbol, f"[{meaning}]")
    
    return decoded_text

if __name__ == "__main__":
    sample_text = "~Hello *World# @Toai -> Future => Success"
    print("Original:", sample_text)
    try:
        result = decode_elegant_text(sample_text)
        print("Decoded:", result)
    except Exception as e:
        print(f"Error during translation: {e}")
        sys.exit(1)