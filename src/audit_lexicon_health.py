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
        "core_stats": {},
        "macro_stats": {}
    }
    
    if os.path.exists(core_path):
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
            result["core_stats"] = {
                "total_entries": len(lexicon_dict),
                "category_distribution": categories,
                "compact_id_count": len(compact_ids)
            }
            
    if os.path.exists(macro_path):
        with open(macro_path, 'r', encoding='utf-8') as f:
            macro_data = json.load(f)
            result["macro_stats"] = {
                "total_entries": len(macro_data) if isinstance(macro_data, dict) else 0
            }
            
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
