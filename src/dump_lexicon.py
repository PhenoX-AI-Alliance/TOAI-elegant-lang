# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_dump.md"

    try:
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
            sys.exit(1)

        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        lines = []
        lines.append("# TOAI Core Lexicon Dump")
        lines.append("")
        lines.append("| Key | Value / Definition |")
        lines.append("|---|---|")

        if isinstance(data, dict):
            for k, v in data.items():
                lines.append(f"| {{k}} | {{str(v)}} |")
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                lines.append(f"| {{idx}} | {{str(item)}} |")
        else:
            lines.append(f"| Data | {{str(data)}} |")

        markdown_content = "\n".join(lines)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"Successfully dumped lexicon to {{output_path}}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    dump_lexicon()
