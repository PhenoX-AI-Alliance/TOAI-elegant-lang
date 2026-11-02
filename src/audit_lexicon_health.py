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
        "core_total": 0,
        "macro_total": 0
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_dict = core_data.get('lexicon', {})
                report["core_total"] = len(lexicon_dict)
                cats = {}
                for sym, data in lexicon_dict.items():
                    cat = data.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                report["core_categories"] = cats
                report["core_lexicon_status"] = "loaded"
        else:
            report["core_lexicon_status"] = "not_found"
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                if isinstance(macro_data, dict):
                    report["macro_total"] = len(macro_data)
                    mcats = {}
                    for k, v in macro_data.items():
                        if isinstance(v, dict):
                            cat = v.get('category', 'unknown')
                            mcats[cat] = mcats.get(cat, 0) + 1
                    report["macro_categories"] = mcats
                    report["macro_lexicon_status"] = "loaded"
                else:
                    report["macro_lexicon_status"] = "invalid_format"
        else:
            report["macro_lexicon_status"] = "not_found"
            
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error during audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicon()
