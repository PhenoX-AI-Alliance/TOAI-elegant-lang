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
        
    print("# TOAI Core Lexicon Dump\n")
    print("This document lists the core lexicon definitions.\n")
    print("| Term / Key | Definition / Value |")
    print("|---|---|")
    
    if isinstance(data, dict):
        for term, definition in data.items():
            print(f"| {term} | {definition} |")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            if isinstance(item, dict):
                term = item.get("term", item.get("name", str(idx)))
                definition = item.get("definition", item.get("desc", json.dumps(item, ensure_ascii=False)))
                print(f"| {term} | {definition} |")
            else:
                print(f"| {idx} | {item} |")
    else:
        print(f"| Value | {data} |")

if __name__ == "__main__":
    main()
