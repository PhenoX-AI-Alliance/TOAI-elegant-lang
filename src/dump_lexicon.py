import sys
import os
import json

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon_table.md"
    
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {{e}}", file=sys.stderr)
        sys.exit(1)
        
    markdown_lines = []
    markdown_lines.append("# Core Lexicon Table")
    markdown_lines.append("")
    markdown_lines.append("| Word / Term | Definition / Description | Category |")
    markdown_lines.append("| :--- | :--- | :--- |")
    
    if isinstance(data, dict):
        items = data.items()
    elif isinstance(data, list):
        items = [(str(i), item) for i, item in enumerate(data)]
    else:
        items = []
        
    for key, val in items:
        if isinstance(val, dict):
            desc = val.get("description", str(val))
            cat = val.get("category", "General")
        else:
            desc = str(val)
            cat = "General"
        markdown_lines.append(f"| {{key}} | {{desc}} | {{cat}} |")
        
    output_content = "\n".join(markdown_lines) + "\n"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_content)
        
    print(output_content)

if __name__ == "__main__":
    main()
