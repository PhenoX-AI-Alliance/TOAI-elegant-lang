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
    decoded_text = text
    # Sort keys by length descending to prevent partial replacements
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    for key in sorted_keys:
        value = translation_map[key]
        decoded_text = decoded_text.replace(key, f"[{value}]")
    return decoded_text

if __name__ == "__main__":
    sample_text = "こんにちは ~* 世界よ ** 命の地球は ++ 進んでいく --。"
    try:
        result = decode_elegant_text(sample_text)
        print("Original:", sample_text)
        print("Decoded:", result)
    except Exception as e:
        print(f"Error during translation: {e}", file=sys.stderr)
        sys.exit(1)
