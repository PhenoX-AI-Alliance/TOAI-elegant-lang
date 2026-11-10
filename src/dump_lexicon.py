import sys
import os
import json
import traceback

def main():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
        
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        md_lines = []
        md_lines.append("# TOAI Elegant Lang - Core Lexicon")
        md_lines.append("")
        md_lines.append("| Key | Value / Definition | Description |")
        md_lines.append("|---|---|---|")
        
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict):
                    val_str = str(v.get("value", ""))
                    desc_str = str(v.get("description", ""))
                else:
                    val_str = str(v)
                    desc_str = ""
                md_lines.append(f"| `{k}` | {val_str} | {desc_str} |")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    k = item.get("key", "N/A")
                    v = item.get("value", "N/A")
                    desc = item.get("description", "")
                    md_lines.append(f"| `{k}` | {v} | {desc} |")
                else:
                    md_lines.append(f"| - | {item} | - |")
                    
        output_markdown = "\n".join(md_lines)
        print(output_markdown)
        
        out_md_path = "/home/phenox/gemini-sandbox/TOAI_Generated/core_lexicon.md"
        with open(out_md_path, "w", encoding="utf-8") as out_f:
            out_f.write(output_markdown)
        print(f"Successfully generated markdown at {out_md_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
