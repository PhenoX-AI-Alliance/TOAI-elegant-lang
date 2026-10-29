# -*- coding: utf-8 -*-
import sys
import os
import json

def load_lexicon(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Lexicon file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_markdown(data):
    lines = ["# Core Lexicon Reference Table", ""]
    lines.append("| Term | Category | Description |")
    lines.append("|---|---|---|")
    
    if isinstance(data, dict):
        items = data.items()
    elif isinstance(data, list):
        items = enumerate(data)
    else:
        items = []

    for k, v in items:
        if isinstance(v, dict):
            term = str(k)
            cat = str(v.get("category", "general"))
            desc = str(v.get("description", ""))
            lines.append(f"| {term} | {cat} | {desc} |")
        else:
            lines.append(f"| {k} | general | {str(v)} |")
            
    return "\n".join(lines)

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon_table.md"
    
    try:
        data = load_lexicon(lexicon_path)
        md = generate_markdown(data)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Successfully generated markdown table at: {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
