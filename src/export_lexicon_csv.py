import sys
import os
import traceback
import time
import json
import csv

def export_lexicon():
    source_json = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.json"
    output_csv = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/core_lexicon.csv"
    
    if not os.path.exists(source_json):
        print(f"Error: Source JSON not found at {{source_json}}", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(source_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {{e}}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
        
    try:
        with open(output_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["key", "value", "category", "description"])
            
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, dict):
                        writer.writerow([
                            k,
                            v.get("value", ""),
                            v.get("category", ""),
                            v.get("description", "")
                        ])
                    else:
                        writer.writerow([k, str(v), "", ""])
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        writer.writerow([
                            item.get("key", ""),
                            item.get("value", ""),
                            item.get("category", ""),
                            item.get("description", "")
                        ])
                    else:
                        writer.writerow(["", str(item), "", ""])
        print(f"Successfully exported lexicon to {{output_csv}}")
    except Exception as e:
        print(f"Error writing CSV: {{e}}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        export_lexicon()
    except Exception as e:
        print(f"Fatal error: {{e}}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
