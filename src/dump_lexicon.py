import sys
import os
import traceback
import time
import json

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: {lexicon_path} not found", file=sys.stderr)
        sys.exit(1)
    
    with open(lexicon_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print("# TOAI Core Lexicon Dump")
    print("")
    for k, v in data.items() if isinstance(data, dict) else enumerate(data):
        print(f"- **{k}**: {v}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
