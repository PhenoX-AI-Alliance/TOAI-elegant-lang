# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def load_lexicon(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Lexicon file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_markdown(data):
    lines = []
    lines.append("# TOAI Elegant Lang - Core Lexicon")
    lines.append("")
    version = data.get("version", "Unknown")
    lines.append(f"**Version:** {version}")
    lines.append("")
    lines.append("| Term | Category | Description |")
    lines.append("|---|---|---|")
    
    lexicon_list = data.get("lexicon", [])
    for item in lexicon_list:
        term = item.get("term", "")
        category = item.get("category", "")
        description = item.get("description", "")
        lines.append(f"| {term} | {category} | {description} |")
        
    return "\n".join(lines)

def main():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
        data = load_lexicon(lexicon_path)
        md_output = generate_markdown(data)
        
        print(md_output)
        
        output_md_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon.md"
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(md_output)
            
        print(f"Successfully dumped lexicon to {output_md_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
