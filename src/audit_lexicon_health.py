import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    results = {
        "core_lexicon": {"status": "missing", "stats": {}},
        "macro_lexicon": {"status": "missing", "stats": {}}
    }
    
    if os.path.exists(core_path):
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
                    
            results["core_lexicon"] = {
                "status": "success",
                "total_entries": len(lexicon_dict),
                "category_distribution": categories,
                "compact_id_stats": {
                    "count": len(compact_ids),
                    "min": min(compact_ids) if compact_ids else None,
                    "max": max(compact_ids) if compact_ids else None
                }
            }
        except Exception as e:
            results["core_lexicon"] = {"status": "error", "message": str(e)}
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            results["macro_lexicon"] = {
                "status": "success",
                "total_entries": len(macro_data) if isinstance(macro_data, dict) else 0
            }
        except Exception as e:
            results["macro_lexicon"] = {"status": "error", "message": str(e)}
            
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return results

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
