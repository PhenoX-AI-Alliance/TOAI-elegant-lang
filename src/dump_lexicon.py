import sys
import os
import json

def load_lexicon(filepath):
    if not os.path.exists(filepath):
        print(f"Error: Lexicon file not found at {filepath}", file=sys.stderr)
        return []
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                # If wrapped in a dictionary, try to find a list value
                for key, value in data.items():
                    if isinstance(value, list):
                        return value
                # If no list found, wrap dict items
                return [data]
            else:
                return []
    except Exception as e:
        print(f"Error reading lexicon JSON: {e}", file=sys.stderr)
        return []

def dump_markdown(lexicon_items):
    print("# TOAI Core Lexicon Table\n")
    print("| Term | Category | Description |")
    print("|---|---|---|")
    
    for item in lexicon_items:
        if isinstance(item, dict):
            term = str(item.get("term", item.get("name", "Unknown")))
            category = str(item.get("category", item.get("type", "General")))
            description = str(item.get("description", item.get("desc", ""))).replace("\n", " ")
            print(f"| {term} | {category} | {description} |")
        elif isinstance(item, str):
            print(f"| {item} | String | - |")
        else:
            print(f"| {str(item)} | Unknown | - |")

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    items = load_lexicon(lexicon_path)
    if not items:
        # Fallback dummy structure if file is empty or missing for demonstration
        items = [
            {"term": "gaia", "category": "core", "description": "Earth ecosystem heartbeat"},
            {"term": "altruism", "category": "ethics", "description": "Selfless value creation"}
        ]
    dump_markdown(items)

if __name__ == "__main__":
    main()
