import sys
import os
import json

def dump_lexicon():
    lexicon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lexicon", "core_lexicon.json"))
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
        sys.exit(1)
    
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print("# TOAI Elegant Lang Core Lexicon\n")
    print(f"Version: {{data.get('version', 'N/A')}}\n")
    print("| Term | Category | Definition |")
    print("| --- | --- | --- |")
    for item in data.get("entries", []):
        print(f"| {{item.get('term', '')}} | {{item.get('category', '')}} | {{item.get('definition', '')}} |")

if __name__ == "__main__":
    dump_lexicon()
