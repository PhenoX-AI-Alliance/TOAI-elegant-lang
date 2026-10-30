import sys
import os
import json
import traceback

def audit_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
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
                lexicon_map = core_data.get('lexicon', {})
                result["core_total"] = len(lexicon_map)
                cats = {}
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                result["core_categories"] = cats
                result["core_status"] = "loaded"
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                if isinstance(macro_data, dict):
                    result["macro_total"] = len(macro_data)
                    mcats = {}
                    for sym, data in macro_data.items():
                        if isinstance(data, dict):
                            cat = data.get('category', 'unknown')
                            mcats[cat] = mcats.get(cat, 0) + 1
                    result["macro_categories"] = mcats
                result["macro_status"] = "loaded"
                
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicon()
