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
        "timestamp": os.path.getmtime(core_path) if os.path.exists(core_path) else None,
        "core_status": "missing",
        "macro_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_count": 0,
        "macro_count": 0
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon = core_data.get('lexicon', {})
                report["core_count"] = len(lexicon)
                report["core_status"] = "loaded"
                cats = {}
                for sym, data in lexicon.items():
                    cat = data.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                report["core_categories"] = cats
        except Exception as e:
            report["core_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report["macro_count"] = len(macro_data)
                report["macro_status"] = "loaded"
                cats = {}
                for sym, data in macro_data.items():
                    cat = data.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                report["macro_categories"] = cats
        except Exception as e:
            report["macro_status"] = f"error: {str(e)}"
            
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
