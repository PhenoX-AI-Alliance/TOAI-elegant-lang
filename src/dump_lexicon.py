import sys
import os
import json

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(1)
        
    print("# TOAI Elegant Lang - Core Lexicon Table\n")
    print("| Key | Value / Description |")
    print("|---|---|")
    
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"| `{k}` | {str(v)} |")
    elif isinstance(data, list):
        for item in data:
            print(f"| {str(item)} | - |")
            
if __name__ == "__main__":
    main()
