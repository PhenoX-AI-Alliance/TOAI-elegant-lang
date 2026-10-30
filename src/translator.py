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
    decoded_text = text
    for symbol, description in translation_map.items():
        decoded_text = decoded_text.replace(symbol, f" [{description}] ")
    return decoded_text

if __name__ == "__main__":
    map_path = os.path.join(os.path.dirname(__file__), "translation_map.json")
    sample_text = "こんにちは ~ * 命の地球へようこそ > 未来を創る #"
    try:
        result = decode_elegant_text(sample_text, map_path)
        print("Decoded Result:")
        print(result)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
