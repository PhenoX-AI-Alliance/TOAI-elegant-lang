import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "core_lexicon": {"status": "missing", "categories": {}, "total": 0},
        "macro_lexicon": {"status": "missing", "total": 0}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            categories = {}
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                categories[cat] = categories.get(cat, 0) + 1
            result["core_lexicon"] = {
                "status": "loaded",
                "categories": categories,
                "total": len(lexicon_dict)
            }
        except Exception as e:
            result["core_lexicon"] = {"status": "error", "message": str(e)}
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            total_macro = len(macro_data) if isinstance(macro_data, (dict, list)) else 0
            result["macro_lexicon"] = {
                "status": "loaded",
                "total": total_macro
            }
        except Exception as e:
            result["macro_lexicon"] = {"status": "error", "message": str(e)}
            
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
