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
        print(f"Error reading lexicon json: {e}", file=sys.stderr)
        sys.exit(1)
        
    print("# TOAI Core Lexicon Table\n")
    print("| Key | Value / Definition |")
    print("|---|---|")
    
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"| {k} | {v} |")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                k = item.get("key", "N/A")
                v = item.get("value", str(item))
                print(f"| {k} | {v} |")
            else:
                print(f"| - | {item} |")
    else:
        print(f"| Data | {str(data)} |")

if __name__ == "__main__":
    main()
