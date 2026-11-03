import os
import json

def decode_elegant_text(text: str, map_file_path: str = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json") -> str:
    if not os.path.exists(map_file_path):
        raise FileNotFoundError(f"Translation map not found at {map_file_path}")
    
    with open(map_file_path, "r", encoding="utf-8") as f:
        translation_map = json.load(f)
        
    decoded_text = text
    for symbol, description in sorted(translation_map.items(), key=lambda x: len(x[0]), reverse=True):
        decoded_text = decoded_text.replace(symbol, description)
        
    return decoded_text

if __name__ == "__main__":
    sample_text = "~* こんにちは、世界 ~* -> ** 優しさを広げよう **"
    print("Original:", sample_text)
    print("Decoded:", decode_elegant_text(sample_text))
