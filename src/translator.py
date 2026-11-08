import os
import json

def decode_elegant_text(text, map_file_path=None):
    if map_file_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        map_file_path = os.path.join(current_dir, "translation_map.json")
    
    if not os.path.exists(map_file_path):
        raise FileNotFoundError(f"Translation map not found at {map_file_path}")
        
    with open(map_file_path, "r", encoding="utf-8") as f:
        trans_map = json.load(f)
        
    sorted_keys = sorted(trans_map.keys(), key=len, reverse=True)
    
    decoded_text = text
    for key in sorted_keys:
        value = trans_map[key]
        decoded_text = decoded_text.replace(key, f"[{value}]")
        
    return decoded_text

if __name__ == "__main__":
    sample_text = "~ * Hello World # -> => &"
    print("Original:", sample_text)
    print("Decoded:", decode_elegant_text(sample_text))
