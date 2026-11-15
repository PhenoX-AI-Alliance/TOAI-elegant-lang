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
    decoded_parts = []
    i = 0
    while i < len(text):
        matched = False
        for length in range(4, 0, -1):
            chunk = text[i:i+length]
            if chunk in trans_map:
                decoded_parts.append(trans_map[chunk])
                i += length
                matched = True
                break
        if not matched:
            decoded_parts.append(text[i])
            i += 1
    return "".join(decoded_parts)

if __name__ == "__main__":
    sample_text = "🌟のプロジェクトが💫を生み出し、⚡で加速する。"
    print("Original:", sample_text)
    print("Decoded:", decode_elegant_text(sample_text))
