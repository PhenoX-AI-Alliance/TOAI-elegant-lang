# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def load_and_dump():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_dump.md"

    try:
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
            sys.exit(1)

        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        markdown_lines = []
        markdown_lines.append("# TOAI Core Lexicon Dump")
        markdown_lines.append("")
        markdown_lines.append("| Key | Definition / Value |")
        markdown_lines.append("|---|---|")

        if isinstance(data, dict):
            for k, v in data.items():
                markdown_lines.append(f"| `{{k}}` | {{str(v)}} |")
        elif isinstance(data, list):
            for item in data:
                markdown_lines.append(f"| `-` | {{str(item)}} |")
        else:
            markdown_lines.append(f"| Data | {{str(data)}} |")

        output_content = "\n".join(markdown_lines)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_content)

        print(f"Successfully dumped lexicon to {{output_path}}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    load_and_dump()
