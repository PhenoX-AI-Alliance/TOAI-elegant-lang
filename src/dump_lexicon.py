import sys
import os
import traceback
import json

def dump_lexicon():
    try:
        base_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        lexicon_path = os.path.join(base_path, "lexicon", "core_lexicon.json")
        
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print("# TOAI Core Lexicon Dump")
        print(f"Version: {data.get('version', 'N/A')}")
        print(f"Description: {data.get('description', 'N/A')}")
        print("")
        print("| Term | Type | Definition |")
        print("|---|---|---|")
        
        for entry in data.get("entries", []):
            term = entry.get("term", "")
            t_type = entry.get("type", "")
            definition = entry.get("definition", "")
            print(f"| {term} | {t_type} | {definition} |")
            
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    dump_lexicon()
