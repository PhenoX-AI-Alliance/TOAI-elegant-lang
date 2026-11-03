import sys
import os
import json
import traceback

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def decode_elegant_text(text, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
    try:
        trans_map = load_translation_map(map_path)
        decoded_text = text
        for symbol, description in trans_map.items():
            decoded_text = decoded_text.replace(symbol, f"[{description}]")
        return decoded_text
    except Exception as e:
        print(f"Error during decoding: {e}", file=sys.stderr)
        traceback.print_exc()
        return text

if __name__ == "__main__":
    sample = "こんにちは ~* 今日も ++ を目指して進もう -> // 落ち着いて @@ を感じる"
    result = decode_elegant_text(sample)
    print("Original:", sample)
    print("Decoded: ", result)
