import sys
import os
import json

def main():
    input_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon.md"
    
    if not os.path.exists(input_path):
        print(f"Error: Source file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
        
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    lines = []
    lines.append("# Core Lexicon List")
    lines.append("")
    lines.append(f"Version: {data.get('version', 'unknown')}")
    lines.append("")
    lines.append("| Term | Category | Description |")
    lines.append("|---|---|---|")
    
    for item in data.get("lexicon", []):
        term = item.get("term", "")
        category = item.get("category", "")
        desc = item.get("description", "")
        lines.append(f"| {term} | {category} | {desc} |")
        
    markdown_content = "\n".join(lines) + "\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print(markdown_content)

if __name__ == "__main__":
    main()
