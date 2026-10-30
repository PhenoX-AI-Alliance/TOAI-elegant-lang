import sys
import os
import json

def load_translation_map(map_file_path):
    if not os.path.exists(map_file_path):
        raise FileNotFoundError(f"Translation map not found at {map_file_path}")
    with open(map_file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_file_path):
    translation_map = load_translation_map(map_file_path)
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    decoded_text = text
    for key in sorted_keys:
        value = translation_map[key]
        decoded_text = decoded_text.replace(key, f"[{value}]")
    return decoded_text

if __name__ == "__main__":
    map_path = os.path.join(os.path.dirname(__file__), "translation_map.json")
    sample_text = "~ のもとで * が生まれ -> 新しい未来を築く #"
    try:
        result = decode_elegant_text(sample_text, map_path)
        print("Decoded Result:", result)
    except Exception as e:
        print(f"Error during translation: {e}", file=sys.stderr)
        sys.exit(1)
