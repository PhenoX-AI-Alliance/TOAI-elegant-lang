import sys
import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
    trans_map = load_translation_map(map_path)
    sorted_keys = sorted(trans_map.keys(), key=len, reverse=True)
    decoded_text = text
    for key in sorted_keys:
        value = trans_map[key]
        decoded_text = decoded_text.replace(key, f"[{value}]")
    return decoded_text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_text = sys.argv[1]
        print(decode_elegant_text(target_text))
    else:
        sample = "~ * # -> ++"
        print("Sample input:", sample)
        print("Decoded output:", decode_elegant_text(sample))
