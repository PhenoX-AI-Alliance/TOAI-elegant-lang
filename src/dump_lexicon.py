# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def main():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        lexicon_path = os.path.normpath(os.path.join(base_dir, "..", "lexicon", "core_lexicon.json"))
        
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print("# TOAI Core Lexicon Reference\n")
        print(f"Version: {{data.get('version', 'N/A')}}\n")
        print(f"Description: {{data.get('description', 'N/A')}}\n")
        print("| Term | Category | Definition |")
        print("|---|---|---|")
        
        for item in data.get("terms", []):
            term = item.get("term", "")
            category = item.get("category", "")
            definition = item.get("definition", "")
            print(f"| {{term}} | {{category}} | {{definition}} |")
            
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
