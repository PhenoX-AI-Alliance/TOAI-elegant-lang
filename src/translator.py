import sys
import os
import json

def load_translation_map(map_path):
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Translation map not found at {map_path}")
    with open(map_path, "r", encoding="utf-8") as f:
        return json.load(f)

def translate_elegant_text(text, map_path="/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/translation_map.json"):
    t_map = load_translation_map(map_path)
    result = []
    for char in text:
        if char in t_map:
            result.append(f"[{t_map[char]}]")
        else:
            result.append(char)
    return "".join(result)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
    else:
        input_text = "Ω と ∞ が交差する時、φ の調和が生まれる。"
    
    translated = translate_elegant_text(input_text)
    print("Original:", input_text)
    print("Translated:", translated)
