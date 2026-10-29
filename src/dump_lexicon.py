import sys
import os
import traceback
import json

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon_summary.md"
    
    try:
        if not os.path.exists(lexicon_path):
            print(f"Error: Lexicon file not found at {lexicon_path}", file=sys.stderr)
            sys.exit(1)
            
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        lines = []
        lines.endswith = lambda x: None # dummy to prevent any attr issues if needed, but standard list is fine
        lines.append("# Core Lexicon Summary\n")
        lines.append("| Word / Term | Definition / Description | Category |")
        lines.append("| :--- | :--- | :--- |")
        
        if isinstance(data, dict):
            for key, val in data.items():
                if isinstance(val, dict):
                    desc = val.get("description", str(val))
                    cat = val.get("category", "General")
                else:
                    desc = str(val)
                    cat = "General"
                lines.append(f"| {key} | {desc} | {cat} |")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    term = item.get("term", item.get("name", "Unknown"))
                    desc = item.get("description", str(item))
                    cat = item.get("category", "General")
                    lines.append(f"| {term} | {desc} | {cat} |")
                else:
                    lines.append(f"| {str(item)} | - | General |")
                    
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
            
        print(f"Successfully generated lexicon summary at {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
