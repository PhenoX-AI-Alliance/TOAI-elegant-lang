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
    translation_map = load_translation_map(map_path)
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    
    decoded_parts = []
    i = 0
    while i < len(text):
        matched = False
        for k in sorted_keys:
            if text.startswith(k, i):
                decoded_parts.append(f"[{translation_map[k]}]")
                i += len(k)
                matched = True
                break
        if not matched:
            decoded_parts.append(text[i])
            i += 1
            
    return "".join(decoded_parts)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python translator.py '<elegant_text>'")
        sys.exit(1)
    
    target_text = sys.argv[1]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_path = os.path.join(current_dir, "translation_map.json")
    
    try:
        result = decode_elegant_text(target_text, map_path)
        print(result)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
