import sys
import os
import json

def load_lexicon(filepath):
    if not os.path.exists(filepath):
        print(f"Error: Lexicon file not found at {filepath}", file=sys.stderr)
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}", file=sys.stderr)
            return {}

def dump_markdown(lexicon_data):
    print("# TOAI Core Lexicon Table\n")
    print("| Key | Definition / Value |")
    print("|---|---|")
    if isinstance(lexicon_data, dict):
        for k, v in lexicon_data.items():
            print(f"| {k} | {v} |")
    elif isinstance(lexicon_data, list):
        for item in lexicon_data:
            print(f"| Item | {item} |")
    else:
        print(f"| Raw | {lexicon_data} |")

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    data = load_lexicon(lexicon_path)
    dump_markdown(data)

if __name__ == "__main__":
    main()
