import sys
import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path):
    translation_map = load_translation_map(map_path)
    # Sort keys by length descending to replace longer symbols first (e.g. '=>' before '=')
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    
    decoded_text = text
    for symbol in sorted_keys:
        meaning = translation_map[symbol]
        replacement = f"[{symbol} -> {meaning}]"
        decoded_text = decoded_text.replace(symbol, replacement)
        
    return decoded_text

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(current_dir, "translation_map.json")
    
    sample_text = "Gaia Ecosystem * ~ => # @"
    try:
        result = decode_elegant_text(sample_text, map_path)
        print("Decoded Result:")
        print(result)
    except Exception as e:
        print(f"Error during translation: {e}", file=sys.stderr)
        sys.exit(1)
