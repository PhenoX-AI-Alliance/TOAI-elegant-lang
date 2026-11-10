import sys
import os
import json

def dump_lexicon(lexicon_file_path):
    if not os.path.exists(lexicon_file_path):
        print(f"Error: Lexicon file not found at {lexicon_file_path}", file=sys.stderr)
        sys.exit(1)
        
    with open(lexicon_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    lexicon_dict = data.get("lexicon", data)
    
    print("# TOAI Elegant Lang - Core Lexicon")
    print("")
    print("| Term | Definition | Type |")
    print("|---|---|---|")
    
    for term, value in lexicon_dict.items():
        if isinstance(value, dict):
            definition = str(value.get("definition", "N/A"))
            term_type = str(value.get("type", "N/A"))
        else:
            definition = str(value)
            term_type = "N/A"
        print(f"| {term} | {definition} | {term_type} |")

if __name__ == "__main__":
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    dump_lexicon(lexicon_path)
