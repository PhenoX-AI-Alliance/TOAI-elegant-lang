import sys
import os
import json

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/lexicon_table.md"
    
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(1)
        
    md_lines = []
    md_lines.append("# TOAI Core Lexicon Table")
    md_lines.append("")
    md_lines.append("| Term | Definition | Category |")
    md_lines.append("|---|---|---|")
    
    items = data if isinstance(data, list) else data.get("items", [])
    if isinstance(data, dict) and not items:
        for k, v in data.items():
            md_lines.append(f"| {k} | {v} | general |")
    else:
        for item in items:
            term = item.get("term", "")
            definition = item.get("definition", "")
            category = item.get("category", "general")
            md_lines.append(f"| {term} | {definition} | {category} |")
            
    output_content = "\n".join(md_lines) + "\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_content)
        
    print(f"Successfully generated lexicon table at {output_path}")

if __name__ == "__main__":
    main()
