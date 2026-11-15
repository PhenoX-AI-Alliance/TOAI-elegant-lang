import sys
import os
import traceback
import time
import json

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {{e}}", file=sys.stderr)
        sys.exit(1)
        
    version = data.get("version", "unknown")
    entries = data.get("entries", [])
    
    md_lines = []
    md_lines.append(f"# TOAI Core Lexicon (Version: {{version}})")
    md_lines.append("")
    md_lines.append("| Term | Category | Definition |")
    md_lines.append("|---|---|---|")
    
    for entry in entries:
        term = entry.get("term", "")
        category = entry.get("category", "")
        definition = entry.get("definition", "")
        md_lines.append(f"| {{term}} | {{category}} | {{definition}} |")
        
    output_md = "\n".join(md_lines)
    print(output_md)
    
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_table.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_md)
    print(f"Successfully dumped lexicon to {{output_path}}")

if __name__ == "__main__":
    try:
        dump_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
