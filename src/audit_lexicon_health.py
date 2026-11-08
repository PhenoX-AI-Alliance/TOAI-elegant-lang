import os
import sys
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
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
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_map = core_data.get('lexicon', {})
                result["core_count"] = len(lexicon_map)
                result["core_lexicon_status"] = "loaded"
                
                categories = {}
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown') if isinstance(data, dict) else 'unknown'
                    categories[cat] = categories.get(cat, 0) + 1
                result["core_categories"] = categories
        except Exception as e:
            result["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                if isinstance(macro_data, dict):
                    result["macro_count"] = len(macro_data)
                    result["macro_lexicon_status"] = "loaded"
                    categories = {}
                    for k, v in macro_data.items():
                        cat = v.get('category', 'unknown') if isinstance(v, dict) else 'unknown'
                        categories[cat] = categories.get(cat, 0) + 1
                    result["macro_categories"] = categories
                elif isinstance(macro_data, list):
                    result["macro_count"] = len(macro_data)
                    result["macro_lexicon_status"] = "loaded_list"
        except Exception as e:
            result["macro_lexicon_status"] = f"error: {str(e)}"
            
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
