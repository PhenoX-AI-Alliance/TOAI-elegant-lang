import sys
import os
import json

def dump_lexicon():
    lexicon_path = os.path.join(os.path.dirname(__file__), "lexicon", "core_lexicon.json")
    if not os.path.exists(lexicon_path):
        print(f"Error: {lexicon_path} not found.", file=sys.stderr)
        sys.exit(1)
        
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print("# TOAI Core Lexicon Dump\n")
    print("| Term | Definition | Category |")
    print("|---|---|---|")
    
    for term, details in data.items():
        if isinstance(details, dict):
            definition = details.get("definition", "N/A")
            category = details.get("category", "General")
        elif isinstance(details, str):
            definition = details
            category = "General"
        else:
            definition = str(details)
            category = "General"
        print(f"| {term} | {definition} | {category} |")

if __name__ == "__main__":
    dump_lexicon()
