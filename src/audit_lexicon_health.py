import sys
import os
import json
import traceback

def audit_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_count": 0,
        "macro_count": 0
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_map = core_data.get('lexicon', {})
                report["core_count"] = len(lexicon_map)
                report["core_lexicon_status"] = "loaded"
                
                cats = {}
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                report["core_categories"] = cats
        except Exception as e:
            report["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                if isinstance(macro_data, dict):
                    report["macro_count"] = len(macro_data)
                    report["macro_lexicon_status"] = "loaded"
                    cats = {}
                    for sym, data in macro_data.items():
                        if isinstance(data, dict):
                            cat = data.get('category', 'unknown')
                            cats[cat] = cats.get(cat, 0) + 1
                    report["macro_categories"] = cats
                elif isinstance(macro_data, list):
                    report["macro_count"] = len(macro_data)
                    report["macro_lexicon_status"] = "loaded_list"
        except Exception as e:
            report["macro_lexicon_status"] = f"error: {str(e)}"
            
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    audit_lexicon()
