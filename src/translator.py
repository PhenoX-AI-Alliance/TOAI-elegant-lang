import json
import os

def decode_elegant_text(text, map_file_path):
    if not os.path.exists(map_file_path):
        return text
    
    with open(map_file_path, "r", encoding="utf-8") as f:
        translation_map = json.load(f)
    
    sorted_keys = sorted(translation_map.keys(), key=len, reverse=True)
    
    decoded_text = text
    for key in sorted_keys:
        value = translation_map[key]
        decoded_text = decoded_text.replace(key, f"[{value}]")
        
    return decoded_text

if __name__ == "__main__":
    sample_text = "~ * # -> Hello Gaia"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_file = os.path.join(current_dir, "translation_map.json")
    result = decode_elegant_text(sample_text, map_file)
    print("Decoded result:", result)
