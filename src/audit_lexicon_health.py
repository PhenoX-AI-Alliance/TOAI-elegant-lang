import sys
import os
import json

def audit():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(base_dir, 'lexicon')
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    categories = {}
    compact_ids = []
    
    for path in [core_path, macro_path]:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for sym, item in data.get('lexicon', {}).items():
                    cat = item.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    cid = item.get('compact_id')
                    if cid is not None:
                        compact_ids.append(cid)
                        
    report = {
        "categories": categories,
        "compact_ids_stats": {
            "count": len(compact_ids),
            "min": min(compact_ids) if compact_ids else None,
            "max": max(compact_ids) if compact_ids else None
        }
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    audit()
