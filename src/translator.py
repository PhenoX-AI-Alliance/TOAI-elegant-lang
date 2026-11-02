import sys
import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at: {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path=None):
    if map_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        map_path = os.path.join(current_dir, "translation_map.json")
    
    translation_map = load_translation_map(map_path)
    
    decoded_text = text
    # Sort keys by length descending to replace longer symbols first
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    for symbol in sorted_keys:
        meaning = translation_map[symbol]
        decoded_text = decoded_text.replace(symbol, f"({meaning})")
        
    return decoded_text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
    else:
        input_text = "Hello ~* World +! -> and =*"
    
    try:
        result = decode_elegant_text(input_text)
        print("Decoded Result:")
        print(result)
    except Exception as e:
        print(f"Error during translation: {e}", file=sys.stderr)
        sys.exit(1)
