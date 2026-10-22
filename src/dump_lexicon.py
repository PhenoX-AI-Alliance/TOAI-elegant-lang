import sys
import os
import json

def dump_lexicon():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI_Generated/lexicon_dump.md"

    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)

    markdown_lines = []
    markdown_lines.append("# TOAI Core Lexicon Dump")
    markdown_lines.append("")
    markdown_lines.append("| Key | Value / Definition |")
    markdown_lines.append("|---|---|")

    if isinstance(data, dict):
        for k, v in data.items():
            markdown_lines.append(f"| `{k}` | {v} |")
    elif isinstance(data, list):
        for item in data:
            markdown_lines.append(f"| {item} | - |")
    else:
        markdown_lines.append(f"| Raw Data | {str(data)} |")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_lines))

    print(f"Lexicon successfully dumped to {output_path}")

if __name__ == "__main__":
    dump_lexicon()
