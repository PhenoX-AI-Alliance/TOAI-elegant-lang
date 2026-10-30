import sys
import os
import traceback
import json

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "core_status": "missing",
        "macro_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_compact_ids": [],
        "macro_compact_ids": []
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                result["core_status"] = "loaded"
                lexicon_map = core_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
                result["core_categories"] = categories
                result["core_compact_ids_count"] = len(compact_ids)
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                result["macro_status"] = "loaded"
                macro_map = macro_data.get('lexicon', macro_data)
                if isinstance(macro_map, dict):
                    categories = {}
                    compact_ids = []
                    for sym, data in macro_map.items():
                        if isinstance(data, dict):
                            cat = data.get('category', 'unknown')
                            categories[cat] = categories.get(cat, 0) + 1
                            if 'compact_id' in data:
                                compact_ids.append(data['compact_id'])
                    result["macro_categories"] = categories
                    result["macro_compact_ids_count"] = len(compact_ids)
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
