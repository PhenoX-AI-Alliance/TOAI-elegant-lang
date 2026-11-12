import sys
import os
import traceback
import time
import json

def main():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        lexicon_path = os.path.join(base_dir, "lexicon", "core_lexicon.json")
        
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print("# TOAI Core Lexicon Table\n")
        print(f"Version: {data.get('version', 'N/A')}\n")
        print("| Term | Category | Definition |")
        print("|:---|:---|:---|")
        
        for entry in data.get("entries", []):
            term = entry.get("term", "")
            category = entry.get("category", "")
            definition = entry.get("definition", "")
            print(f"| {term} | {category} | {definition} |")
            
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
