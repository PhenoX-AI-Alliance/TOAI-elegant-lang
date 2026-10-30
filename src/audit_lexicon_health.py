import sys
import os
import json
import traceback

def audit_lexicon():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_total": 0,
        "macro_total": 0
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_map = core_data.get('lexicon', {})
                result["core_total"] = len(lexicon_map)
                cats = {}
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                    cats[cat] = cats.get(cat, 0) + 1
                result["core_categories"] = cats
                result["core_lexicon_status"] = "loaded"
        except Exception as e:
            result["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                lexicon_map = macro_data.get('lexicon', macro_data)
                if isinstance(lexicon_map, dict):
                    result["macro_total"] = len(lexicon_map)
                    cats = {}
                    for sym, data in lexicon_map.items():
                        cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                        cats[cat] = cats.get(cat, 0) + 1
                    result["macro_categories"] = cats
                    result["macro_lexicon_status"] = "loaded"
                else:
                    result["macro_lexicon_status"] = "invalid_format"
        except Exception as e:
            result["macro_lexicon_status"] = f"error: {str(e)}"
            
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicon()
