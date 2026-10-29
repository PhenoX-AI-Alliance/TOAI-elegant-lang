import sys
import os
import json

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}")
        sys.exit(1)
        
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print("# Core Lexicon Summary\n")
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"## {k}")
            print(f"{v}\n")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                t = item.get("term", "Item")
                d = item.get("definition", str(item))
                print(f"## {t}")
                print(f"{d}\n")
            else:
                print(f"- {item}")
    else:
        print(str(data))

if __name__ == "__main__":
    main()
