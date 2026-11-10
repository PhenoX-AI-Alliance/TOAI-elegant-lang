import sys
import os
import traceback
import time
import json

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "core_lexicon": {"exists": False, "category_distribution": {}, "compact_id_stats": {}},
        "macro_lexicon": {"exists": False, "category_distribution": {}, "compact_id_stats": {}}
    }
    
    if os.path.exists(core_path):
        result["core_lexicon"]["exists"] = True
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                if 'compact_id' in data:
                    compact_ids.append(data['compact_id'])
            result["core_lexicon"]["category_distribution"] = categories
            result["core_lexicon"]["compact_id_stats"] = {
                "total": len(compact_ids),
                "unique": len(set(compact_ids))
            }
        except Exception as e:
            result["core_lexicon"]["error"] = str(e)
            
    if os.path.exists(macro_path):
        result["macro_lexicon"]["exists"] = True
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            lexicon_dict = macro_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                if 'compact_id' in data:
                    compact_ids.append(data['compact_id'])
            result["macro_lexicon"]["category_distribution"] = categories
            result["macro_lexicon"]["compact_id_stats"] = {
                "total": len(compact_ids),
                "unique": len(set(compact_ids))
            }
        except Exception as e:
            result["macro_lexicon"]["error"] = str(e)
            
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
