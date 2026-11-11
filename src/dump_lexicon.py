import sys
import os
import traceback
import time
import json

def load_and_dump():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
        if not os.path.exists(lexicon_path):
            print(f"Error: {lexicon_path} does not exist.", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        items = data.get("lexicon", [])
        
        md_lines = []
        md_lines.append("# TOAI Core Lexicon")
        md_lines.append("")
        md_lines.append("| Term | Type | Definition |")
        md_lines.append("|---|---|---|")
        
        for item in items:
            term = item.get("term", "")
            t_type = item.get("type", "")
            definition = item.get("definition", "")
            md_lines.append(f"| {term} | {t_type} | {definition} |")
            
        output_content = "\n".join(md_lines)
        print(output_content)
        
        output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.md"
        with open(output_path, "w", encoding="utf-8") as out_f:
            out_f.write(output_content)
            
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    load_and_dump()
