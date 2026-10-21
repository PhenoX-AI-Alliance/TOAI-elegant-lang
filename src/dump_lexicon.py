import sys
import os
import json

def load_and_dump():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_dump.md"
    
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)
        
    md_lines = ["# Core Lexicon Dump", "", "| Term | Definition / Value |", "| --- | --- |"]
    
    if isinstance(data, dict):
        for k, v in data.items():
            md_lines.append(f"| {k} | {str(v).replace(chr(124), '&#124;')} |")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            md_lines.append(f"| {idx} | {str(item).replace(chr(124), '&#124;')} |")
    else:
        md_lines.append(f"| Data | {str(data)} |")
        
    output_content = "\n".join(md_lines)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_content)
        
    print(f"Lexicon successfully dumped to {output_path}")

if __name__ == "__main__":
    load_and_dump()
