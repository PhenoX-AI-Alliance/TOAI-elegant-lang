import json
import os

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        return {}
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
    translation_map = load_translation_map(map_path)
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    decoded_text = text
    for key in sorted_keys:
        value = translation_map[key]
        decoded_text = decoded_text.replace(key, value)
    return decoded_text

if __name__ == "__main__":
    sample_text = "Hello ~ * -> # world"
    result = decode_elegant_text(sample_text)
    print("Original:", sample_text)
    print("Decoded:", result)
