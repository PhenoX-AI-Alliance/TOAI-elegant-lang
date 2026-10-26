# -*- coding: utf-8 -*-
import sys
import os
import json

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(1)
        
    terms = data.get("terms", [])
    
    md_lines = []
    md_lines.append("# TOAI Core Lexicon Summary")
    md_lines.append("")
    md_lines.append(f"Version: {data.get('version', 'Unknown')}")
    md_lines.append(f"Description: {data.get('description', '')}")
    md_lines.append("")
    md_lines.append("| Word | Meaning | Category |")
    md_lines.append("|---|---|---|")
    
    for item in terms:
        word = item.get("word", "")
        meaning = item.get("meaning", "")
        category = item.get("category", "")
        md_lines.append(f"| {word} | {meaning} | {category} |")
        
    markdown_output = "\n".join(md_lines)
    print(markdown_output)
    
    output_md_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon_summary.md"
    try:
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(markdown_output)
        print(f"Successfully wrote markdown summary to {output_md_path}")
    except Exception as e:
        print(f"Error writing markdown file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    dump_lexicon()
