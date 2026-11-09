import os
import sys
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
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
            lexicon_dict = core_data.get('lexicon', {})
            report["core_count"] = len(lexicon_dict)
            report["core_lexicon_status"] = "loaded"
            
            categories = {}
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                categories[cat] = categories.get(cat, 0) + 1
            report["core_categories"] = categories
        except Exception as e:
            report["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            if isinstance(macro_data, dict):
                report["macro_count"] = len(macro_data)
                report["macro_lexicon_status"] = "loaded"
                categories = {}
                for sym, data in macro_data.items():
                    cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                    categories[cat] = categories.get(cat, 0) + 1
                report["macro_categories"] = categories
            elif isinstance(macro_data, list):
                report["macro_count"] = len(macro_data)
                report["macro_lexicon_status"] = "loaded (list format)"
        except Exception as e:
            report["macro_lexicon_status"] = f"error: {str(e)}"
            
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
