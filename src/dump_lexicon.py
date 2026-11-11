import sys
import os
import traceback
import time
import json

def dump_lexicon():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
            sys.exit(1)

        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        markdown_lines = []
        markdown_lines.append("# TOAI Elegant Lang - Core Lexicon")
        markdown_lines.append("")
        markdown_lines.append(f"Version: `{data.get('version', 'unknown')}`")
        markdown_lines.append("")
        markdown_lines.append("| Term | Category | Definition |")
        markdown_lines.append("|---|---|---|")

        for item in data.get("lexicon", []):
            term = item.get("term", "")
            category = item.get("category", "")
            definition = item.get("definition", "")
            markdown_lines.append(f"| {term} | {category} | {definition} |")

        output_md = "\n".join(markdown_lines)
        print(output_md)

        out_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_dump.md"
        with open(out_path, "w", encoding="utf-8") as out_f:
            out_f.write(output_md)

    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    dump_lexicon()
