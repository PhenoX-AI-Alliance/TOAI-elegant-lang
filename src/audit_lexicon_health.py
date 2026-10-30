import sys
import os
import json
import traceback

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lang_root = os.path.join(workspace, 'TOAI-elegant-lang')
    
    core_path = os.path.join(lang_root, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(lang_root, 'lexicon', 'macro_lexicon.json')
    
    report = {
        "timestamp": os.path.isdir(lang_root),
        "core_status": "missing",
        "macro_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_total": 0,
        "macro_total": 0
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon = core_data.get('lexicon', {})
                report["core_total"] = len(lexicon)
                report["core_status"] = "loaded"
                
                cats = {}
                for sym, val in lexicon.items():
                    if isinstance(val, dict):
                        cat = val.get('category', 'unknown')
                        cats[cat] = cats.get(cat, 0) + 1
                report["core_categories"] = cats
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                if isinstance(macro_data, dict):
                    report["macro_total"] = len(macro_data)
                    report["macro_status"] = "loaded"
                    mcats = {}
                    for sym, val in macro_data.items():
                        if isinstance(val, dict):
                            cat = val.get('category', 'unknown')
                            mcats[cat] = mcats.get(cat, 0) + 1
                    report["macro_categories"] = mcats
                    
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error during audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
