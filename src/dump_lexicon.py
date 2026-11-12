import sys
import os
import traceback
import time
import json

def main():
    try:
        lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        print("# Core Lexicon Summary\n")
        print("| Term / Key | Details / Structure |")
        print("|---|---|")
        
        if isinstance(data, dict):
            for key, details in data.items():
                if isinstance(details, dict):
                    category = details.get("category", "N/A")
                    desc = details.get("description", str(details))
                    print(f"| {key} | **Category:** {category} - {desc} |")
                elif isinstance(details, list):
                    print(f"| {key} | List items: {len(details)} items |")
                else:
                    print(f"| {key} | {str(details)} |")
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                if isinstance(item, dict):
                    name = item.get("name", item.get("term", f"Item {idx}"))
                    print(f"| {name} | {json.dumps(item, ensure_ascii=False)} |")
                else:
                    print(f"| Item {idx} | {str(item)} |")
        else:
            print(f"| Data | {str(data)} |")
            
        output_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
        os.makedirs(output_dir, exist_ok=True)
        out_file = os.path.join(output_dir, "lexicon_summary.md")
        
        print(f"\nSuccessfully processed lexicon and outputted markdown report.")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
