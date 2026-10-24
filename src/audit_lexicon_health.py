import sys
import os
import json
import traceback

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "core_lexicon": {"status": "missing", "categories": {}, "total": 0},
        "macro_lexicon": {"status": "missing", "categories": {}, "total": 0}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lexicon_map = data.get('lexicon', {})
                categories = {}
                for sym, val in lexicon_map.items():
                    cat = val.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                result["core_lexicon"] = {
                    "status": "success",
                    "categories": categories,
                    "total": len(lexicon_map)
                }
        except Exception as e:
            result["core_lexicon"]["status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lexicon_map = data.get('lexicon', {}) if isinstance(data, dict) and 'lexicon' in data else data
                categories = {}
                if isinstance(lexicon_map, dict):
                    for sym, val in lexicon_map.items():
                        cat = val.get('category', 'unknown') if isinstance(val, dict) else 'unknown'
                        categories[cat] = categories.get(cat, 0) + 1
                result["macro_lexicon"] = {
                    "status": "success",
                    "categories": categories,
                    "total": len(lexicon_map) if isinstance(lexicon_map, dict) else 0
                }
        except Exception as e:
            result["macro_lexicon"]["status"] = f"error: {str(e)}"
            
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
