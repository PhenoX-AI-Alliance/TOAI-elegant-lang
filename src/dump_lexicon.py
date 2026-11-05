import sys
import os
import traceback
import json

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_table.md"
    
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
        
    lines = ["# Core Lexicon Table", "", "| Key | Value / Definition |", "| --- | --- |"]
    
    if isinstance(data, dict):
        for k, v in data.items():
            lines.append(f"| {k} | {v} |")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            lines.append(f"| {idx} | {item} |")
    else:
        lines.append(f"| Data | {data} |")
        
    markdown_content = "\n".join(lines) + "\n"
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Successfully generated markdown lexicon table at {output_path}")
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unhandled exception: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
