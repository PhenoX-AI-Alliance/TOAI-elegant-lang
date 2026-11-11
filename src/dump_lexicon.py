import sys
import os
import json
import traceback

def main():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {{lexicon_path}}", file=sys.stderr)
            sys.exit(1)

        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        print("# TOAI-elegant-lang Core Lexicon")
        print()
        print("| Word / Symbol | Type / Category | Description |")
        print("|:---|:---|:---|")

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    cat = value.get("category", "N/A")
                    desc = value.get("description", str(value))
                    print(f"| `{{key}}` | {{cat}} | {{desc}} |")
                else:
                    print(f"| `{{key}}` | general | {{value}} |")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    name = item.get("name", item.get("word", "N/A"))
                    cat = item.get("category", "N/A")
                    desc = item.get("description", "N/A")
                    print(f"| `{{name}}` | {{cat}} | {{desc}} |")
                else:
                    print(f"| `-` | item | {{item}} |")
        else:
            print(f"Unexpected JSON structure: {{type(data)}}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
