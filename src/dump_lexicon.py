# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def load_and_dump():
    try:
        base_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang"
        lexicon_path = os.path.join(base_path, "lexicon", "core_lexicon.json")
        
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        md_lines = []
        md_lines.append("# TOAI Core Lexicon")
        md_lines.append("")
        md_lines.append(f"Version: {data.get('version', 'Unknown')}")
        md_lines.append(f"Description: {data.get('description', '')}")
        md_lines.append("")
        md_lines.append("| Word | Meaning | Category |")
        md_lines.append("|:---|:---|:---|")
        
        for entry in data.get("entries", []):
            word = entry.get("word", "")
            meaning = entry.get("meaning", "")
            category = entry.get("category", "")
            md_lines.append(f"| {word} | {meaning} | {category} |")
            
        md_output = "\n".join(md_lines)
        
        output_md_path = os.path.join(base_path, "lexicon", "core_lexicon.md")
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(md_output)
            
        print(md_output)
        print(f"Successfully dumped lexicon to {output_md_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    load_and_dump()
