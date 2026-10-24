# -*- coding: utf-8 -*-
import sys
import os
import json

def load_lexicon(filepath):
    if not os.path.exists(filepath):
        print(f"Error: Lexicon file not found at {filepath}", file=sys.stderr)
        sys.exit(1)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_markdown(data):
    lines = []
    lines.append("# TOAI-elegant-lang Core Lexicon")
    lines.append("")
    if "version" in data:
        lines.append(f"**Version:** {data['version']}")
    if "description" in data:
        lines.append(f"**Description:** {data['description']}")
    lines.append("")
    lines.append("| Term | Category | Definition |")
    lines.append("| :--- | :--- | :--- |")
    
    entries = data.get("entries", [])
    for entry in entries:
        term = entry.get("term", "")
        category = entry.get("category", "")
        definition = entry.get("definition", "")
        lines.append(f"| {term} | {category} | {definition} |")
        
    return "\n".join(lines)

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
    data = load_lexicon(lexicon_path)
    markdown_output = generate_markdown(data)
    
    output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "lexicon_table.md")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_output)
        
    print(markdown_output)
    print(f"Successfully dumped lexicon to {output_file}")

if __name__ == "__main__":
    main()
