import sys
import os
import traceback
import time
import json

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_table.md"
    
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        entries = data.get("entries", [])
        
        md_lines = []
        md_lines.append("# TOAI Core Lexicon")
        md_lines.append("")
        md_lines.append(f"Version: {data.get('version', 'unknown')}")
        md_lines.append(f"Description: {data.get('description', '')}")
        md_lines.append("")
        md_lines.append("| Term | Category | Definition |")
        md_lines.append("|---|---|---|")
        
        for entry in entries:
            term = entry.get("term", "")
            category = entry.get("category", "")
            definition = entry.get("definition", "")
            md_lines.append(f"| {term} | {category} | {definition} |")
            
        md_content = "\n".join(md_lines)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        print(md_content)
        print(f"Successfully dumped lexicon to {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    dump_lexicon()
