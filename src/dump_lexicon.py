import sys
import os
import json

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_table.md"
    
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {{e}}", file=sys.stderr)
        sys.exit(1)
        
    lines = ["# TOAI Core Lexicon Table", "", "| Term | Definition |", "|---|---|"]
    
    if isinstance(data, dict):
        for term, definition in data.items():
            lines.append(f"| {{term}} | {{definition}} |")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                term = item.get("term", str(item))
                definition = item.get("definition", "")
                lines.append(f"| {{term}} | {{definition}} |")
            else:
                lines.append(f"| {{item}} | - |")
    else:
        lines.append(f"| {{str(data)}} | - |")
        
    markdown_content = "\n".join(lines) + "\n"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print(markdown_content)

if __name__ == "__main__":
    main()
