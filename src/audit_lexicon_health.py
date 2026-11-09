import sys
import os
import json
import traceback

def audit_lexicons():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_total_entries": 0,
        "macro_total_entries": 0
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_map = core_data.get('lexicon', {})
                report["core_lexicon_status"] = "loaded"
                report["core_total_entries"] = len(lexicon_map)
                categories = {}
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                report["core_categories"] = categories
        except Exception as e:
            report["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report["macro_lexicon_status"] = "loaded"
                if isinstance(macro_data, dict):
                    report["macro_total_entries"] = len(macro_data)
                    categories = {}
                    for k, v in macro_data.items():
                        if isinstance(v, dict):
                            cat = v.get('category', 'unknown')
                            categories[cat] = categories.get(cat, 0) + 1
                    report["macro_categories"] = categories
        except Exception as e:
            report["macro_lexicon_status"] = f"error: {str(e)}"
            
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
