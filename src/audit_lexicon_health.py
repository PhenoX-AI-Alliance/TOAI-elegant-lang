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
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_count": 0,
        "macro_count": 0
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_map = core_data.get('lexicon', {})
                result["core_count"] = len(lexicon_map)
                cats = {}
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                result["core_categories"] = cats
                result["core_lexicon_status"] = "loaded"
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                macro_map = macro_data.get('macro_lexicon', macro_data.get('lexicon', {}))
                result["macro_count"] = len(macro_map)
                cats = {}
                for sym, data in macro_map.items():
                    cat = data.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                result["macro_categories"] = cats
                result["macro_lexicon_status"] = "loaded"
                
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error during audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicon()
