import sys
import os
import json

def load_and_dump():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    if not os.path.exists(lexicon_path):
        print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)
        
    print("# TOAI Core Lexicon")
    print("")
    print("| Term | Definition |")
    print("| :--- | :--- |")
    
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                term = item.get("term", "")
                definition = item.get("definition", "")
                print(f"| {term} | {definition} |")
            elif isinstance(item, str):
                print(f"| {item} | - |")
    elif isinstance(data, dict):
        for term, definition in data.items():
            print(f"| {term} | {definition} |")
            
    output_md = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.md"
    # Also write to md file for persistent record
    with open(output_md, "w", encoding="utf-8") as out:
        out.write("# TOAI Core Lexicon\n\n")
        out.write("| Term | Definition |\n")
        out.write("| :--- | :--- |\n")
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    term = item.get("term", "")
                    definition = item.get("definition", "")
                    out.write(f"| {term} | {definition} |\n")
                elif isinstance(item, str):
                    out.write(f"| {item} | - |\n")
        elif isinstance(data, dict):
            for term, definition in data.items():
                out.write(f"| {term} | {definition} |\n")

if __name__ == "__main__":
    load_and_dump()
