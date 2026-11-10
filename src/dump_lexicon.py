import sys
import os
import json

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(1)
        
    print("# TOAI-elegant-lang Core Lexicon")
    print("")
    print("| Word / Symbol | Meaning / Description | Category |")
    print("|---|---|---|")
    
    if isinstance(data, dict):
        items = data.items()
    elif isinstance(data, list):
        items = [(str(i), item) for i, item in enumerate(data)]
    else:
        items = []
        
    for key, val in items:
        if isinstance(val, dict):
            meaning = val.get("meaning", str(val))
            category = val.get("category", "general")
        else:
            meaning = str(val)
            category = "general"
        print(f"| {key} | {meaning} | {category} |")

if __name__ == "__main__":
    main()
