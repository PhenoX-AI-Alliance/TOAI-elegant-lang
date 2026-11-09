import sys
import os
import traceback
import time
import json

def main():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print("# TOAI Core Lexicon Report")
        print("")
        print(f"**Version:** {data.get('version', 'N/A')}")
        print(f"**Description:** {data.get('description', 'N/A')}")
        print("")
        print("| Term | Category | Definition |")
        print("|---|---|---|")
        
        entries = data.get("entries", [])
        for entry in entries:
            term = entry.get("term", "")
            category = entry.get("category", "")
            definition = entry.get("definition", "")
            print(f"| {term} | {category} | {definition} |")
            
        output_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "lexicon_report.md")
        
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("# TOAI Core Lexicon Report\n\n")
            out.write(f"**Version:** {data.get('version', 'N/A')}\n")
            out.write(f"**Description:** {data.get('description', 'N/A')}\n\n")
            out.write("| Term | Category | Definition |\n")
            out.write("|---|---|---|\n")
            for entry in entries:
                term = entry.get("term", "")
                category = entry.get("category", "")
                definition = entry.get("definition", "")
                out.write(f"| {term} | {category} | {definition} |\n")
                
        print(f"Successfully generated markdown report at {output_file}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
