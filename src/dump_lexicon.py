import sys
import os
import json

def generate_lexicon_markdown():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {{e}}", file=sys.stderr)
        sys.exit(1)
        
    md_lines = ["# TOAI Core Lexicon", "", "| Term | Definition | Category |", "|---|---|---|"]
    
    for term, details in sorted(data.items()):
        if isinstance(details, dict):
            definition = details.get("definition", "N/A")
            category = details.get("category", "N/A")
        else:
            definition = str(details)
            category = "N/A"
        md_lines.append(f"| {{term}} | {{definition}} | {{category}} |")
        
    output_md = "\n".join(md_lines)
    print(output_md)
    
    out_file = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_table.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(output_md)
    print(f"Successfully generated markdown at {{out_file}}")

if __name__ == "__main__":
    generate_lexicon_markdown()