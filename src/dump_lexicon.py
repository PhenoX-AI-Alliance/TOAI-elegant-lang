import sys
import os
import traceback
import time
import json

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
        sys.exit(1)
        
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    if isinstance(data, dict):
        items = data.get("items", [])
    elif isinstance(data, list):
        items = data
    else:
        items = []
        
    md_lines = ["# Lexicon List", "", "| Term | Category | Description |", "|---|---|---|"]
    for item in items:
        if isinstance(item, dict):
            term = item.get("term", "")
            category = item.get("category", "")
            description = item.get("description", "")
            md_lines.append(f"| {{term}} | {{category}} | {{description}} |")
        elif isinstance(item, str):
            md_lines.append(f"| {{item}} | - | - |")
            
    output_md = "\n".join(md_lines)
    print(output_md)
    
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/lexicon_output.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_md)
    print(f"Successfully dumped lexicon to {{output_path}}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
