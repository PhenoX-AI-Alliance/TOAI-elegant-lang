import sys
import os
import json

def load_and_dump():
    lexicon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lexicon", "core_lexicon.json"))
    
    data = {}
    if os.path.exists(lexicon_path):
        with open(lexicon_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error parsing JSON: {e}", file=sys.stderr)
                data = {}
    else:
        data = {
            "example_key": "example_value",
            "description": "Default core lexicon entry for TOAI-elegant-lang"
        }
        
    print("# TOAI Core Lexicon Dump")
    print("")
    print("| Key | Value / Description |")
    print("|---|---|")
    
    if isinstance(data, dict):
        for k, v in sorted(data.items()):
            print(f"| `{k}` | {v} |")
    else:
        print(f"| Data | {str(data)} |")

if __name__ == "__main__":
    load_and_dump()
