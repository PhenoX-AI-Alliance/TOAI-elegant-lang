# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def load_and_dump():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_dump.md"
    
    try:
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        md_lines = []
        md_lines.append("# Core Lexicon Summary")
        md_lines.append("")
        md_lines.append("| Term | Definition / Category |")
        md_lines.append("| --- | --- |")
        
        if isinstance(data, dict):
            for key, value in data.items():
                md_lines.append(f"| {key} | {str(value)} |")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    term = item.get("term", item.get("name", "Unknown"))
                    desc = item.get("description", item.get("definition", str(item)))
                    md_lines.append(f"| {term} | {desc} |")
                else:
                    md_lines.append(f"| {str(item)} | - |")
        else:
            md_lines.append(f"| Raw Data | {str(data)} |")
            
        output_content = "\n".join(md_lines)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_content)
            
        print(f"Successfully dumped lexicon to {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    load_and_dump()
