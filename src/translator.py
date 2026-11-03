import os
import json
import sys

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path):
    translation_map = load_translation_map(map_path)
    decoded_text = text
    for symbol, description in translation_map.items():
        decoded_text = decoded_text.replace(symbol, f"[{description}]")
    return decoded_text

if __name__ == "__main__":
    map_file = os.path.join(os.path.dirname(__file__), "translation_map.json")
    sample_text = "§ 命の地球へようこそ。† エラーを防ぎながら ‡ 善の収益化を達成する ※ ∞"
    try:
        result = decode_elegant_text(sample_text, map_file)
        print("Decoded Result:")
        print(result)
    except Exception as e:
        print(f"Error during translation: {e}", file=sys.stderr)
        sys.exit(1)
