import json
import os

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        return {}
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path):
    translation_map = load_translation_map(map_path)
    decoded_text = text
    for symbol, meaning in translation_map.items():
        decoded_text = decoded_text.replace(symbol, f"({meaning})")
    return decoded_text

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_file = os.path.join(current_dir, "translation_map.json")
    sample_text = "~*# @+"
    result = decode_elegant_text(sample_text, map_file)
    print(f"Original: {sample_text}")
    print(f"Decoded: {result}")
