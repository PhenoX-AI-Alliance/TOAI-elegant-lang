import sys
import os
import traceback
import json

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print("# TOAI Core Lexicon Report")
        print(f"Version: {data.get('version', 'Unknown')}")
        print(f"Description: {data.get('description', '')}")
        print("")
        print("| Term | Category | Definition |")
        print("|---|---|---|")
        
        for entry in data.get("entries", []):
            term = entry.get("term", "")
            category = entry.get("category", "")
            definition = entry.get("definition", "")
            print(f"| {term} | {category} | {definition} |")
            
        output_md = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_report.md"
        with open(output_md, "w", encoding="utf-8") as out:
            out.write("# TOAI Core Lexicon Report\n")
            out.write(f"Version: {data.get('version', 'Unknown')}\n\n")
            out.write("| Term | Category | Definition |\n")
            out.write("|---|---|---|\n")
            for entry in data.get("entries", []):
                out.write(f"| {entry.get('term', '')} | {entry.get('category', '')} | {entry.get('definition', '')} |\n")
                
        print(f"Successfully generated markdown report at {output_md}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    dump_lexicon()
