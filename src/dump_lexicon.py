import sys
import os
import json

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading lexicon JSON: {{e}}", file=sys.stderr)
        sys.exit(1)
        
    md_lines = []
    md_lines.append("# Core Lexicon Table")
    md_lines.append("")
    md_lines.append("| Term | Definition | Category |")
    md_lines.append("|---|---|---|")
    
    if isinstance(data, dict):
        items = data.items()
    elif isinstance(data, list):
        items = enumerate(data)
    else:
        items = []
        
    for k, v in items:
        if isinstance(v, dict):
            term = str(v.get("term", k))
            definition = str(v.get("definition", ""))
            category = str(v.get("category", ""))
        else:
            term = str(k)
            definition = str(v)
            category = ""
        md_lines.append(f"| {{term}} | {{definition}} | {{category}} |")
        
    output_md = "\n".join(md_lines)
    print(output_md)
    
    out_file = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon_table.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(output_md)
    print(f"Successfully generated Markdown table at {{out_file}}")

if __name__ == "__main__":
    main()
