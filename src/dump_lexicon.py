import sys
import os
import traceback
import time
import json

def main():
    lexicon_path = "/home/phenox/gemini-sandbox/lexicon/core_lexicon.json"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/lexicon_table.md"
    
    if not os.path.exists(lexicon_path):
        print("Error: lexicon file not found at " + lexicon_path)
        sys.exit(1)
        
    try:
        with open(lexicon_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("Error reading JSON: " + str(e))
        sys.exit(1)
        
    md_lines = []
    md_lines.append("# Core Lexicon Table")
    md_lines.append("")
    md_lines.append("| Key / Word | Details / Meaning |")
    md_lines.append("|------------|-------------------|")
    
    if isinstance(data, dict):
        for k, v in data.items():
            meaning = ""
            if isinstance(v, dict):
                meaning = v.get("meaning", str(v))
            elif isinstance(v, list):
                meaning = ", ".join([str(item) for item in v])
            else:
                meaning = str(v)
            md_lines.append("| " + str(k) + " | " + str(meaning).replace("\n", " ") + " |")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            meaning = ""
            if isinstance(item, dict):
                meaning = item.get("meaning", str(item))
            else:
                meaning = str(item)
            md_lines.append("| [" + str(idx) + "] | " + str(meaning).replace("\n", " ") + " |")
    else:
        md_lines.append("| Data | " + str(data) + " |")
        
    output_content = "\n".join(md_lines)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_content)
        
    print("Lexicon table successfully dumped to " + output_path)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
