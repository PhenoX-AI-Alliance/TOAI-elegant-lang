import sys
import os
import traceback
import time
import json
from pathlib import Path

def dump_lexicon():
    try:
        lexicon_path = Path("/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json")
        if not lexicon_path.exists():
            print(f"Error: {lexicon_path} does not exist.", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        items = data.get("lexicon", [])
        
        output = "# TOAI-elegant-lang Core Lexicon\n\n"
        output += "| Term | Category | Description |\n"
        output += "|---|---|---|\n"
        
        for item in items:
            term = item.get("term", "")
            category = item.get("category", "")
            desc = item.get("description", "")
            output += f"| {term} | {category} | {desc} |\n"
            
        print(output)
        
        out_file = Path("/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_table.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(output)
            
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    dump_lexicon()
