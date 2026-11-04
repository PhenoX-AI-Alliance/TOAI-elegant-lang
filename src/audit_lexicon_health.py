import sys
import os
import traceback
import json

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    audit_result = {
        "timestamp": os.path.getmtime(core_path) if os.path.exists(core_path) else 0,
        "core_lexicon": {},
        "macro_lexicon": {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_map = core_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            for sym, data in lexicon_map.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                if 'compact_id' in data:
                    compact_ids.append(data['compact_id'])
            
            audit_result['core_lexicon'] = {
                "total_entries": len(lexicon_map),
                "category_distribution": categories,
                "compact_id_count": len(compact_ids)
            }
        except Exception as e:
            audit_result['core_lexicon'] = {"error": str(e)}
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            audit_result['macro_lexicon'] = {
                "total_entries": len(macro_data)
            }
        except Exception as e:
            audit_result['macro_lexicon'] = {"error": str(e)}
            
    print(json.dumps(audit_result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
