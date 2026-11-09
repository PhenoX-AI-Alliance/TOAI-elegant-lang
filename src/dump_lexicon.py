import sys
import os
import json
import traceback

def main():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print("# TOAI Core Lexicon Report")
        print(f"Version: {{data.get('version', 'unknown')}}")
        print()
        print("| Term | Type | Meaning |")
        print("|---|---|---|")
        
        for item in data.get("lexicon", []):
            term = item.get("term", "")
            t_type = item.get("type", "")
            meaning = item.get("meaning", "")
            print(f"| {{term}} | {{t_type}} | {{meaning}} |")
            
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
