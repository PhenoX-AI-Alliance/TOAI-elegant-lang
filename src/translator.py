import sys
import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
    t_map = load_translation_map(map_path)
    result = text
    for symbol, description in t_map.items():
        result = result.replace(symbol, f"[{description}]")
    return result

if __name__ == "__main__":
    sample_text = "Ω を起動し、∞ の中で Ψ を観測する。"
    decoded = decode_elegant_text(sample_text)
    print("Original:", sample_text)
    print("Decoded:", decoded)
