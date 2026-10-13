import sys
import os
import traceback
import json

def load_lexicon(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    data = load_lexicon(lexicon_path)
    
    output = []
    output.endswith = output.append
    output.append("# TOAI Core Lexicon Dump\n")
    output.append("| Word/Key | Type / Details |")
    output.append("|---|---|")
    
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict):
                v_type = v.get("type", "unknown")
                output.append(f"| {k} | {v_type} |")
            elif isinstance(v, str):
                output.append(f"| {k} | {v} |")
            else:
                output.append(f"| {k} | {str(v)} |")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                name = item.get("name", str(item))
                output.append(f"| {name} | dict |")
            else:
                output.append(f"| {str(item)} | string |")
                
    markdown_text = "\n".join(output)
    
    out_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "lexicon_dump.md")
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(markdown_text)
        
    print(f"Successfully dumped lexicon to {out_file}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
