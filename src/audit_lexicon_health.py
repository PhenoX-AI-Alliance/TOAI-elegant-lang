import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    results = {}
    
    for name, path in [('core_lexicon', core_path), ('macro_lexicon', macro_path)]:
        if not os.path.exists(path):
            print(f"Warning: {path} does not exist.", file=sys.stderr)
            results[name] = {"error": "file not found"}
            continue
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading {path}: {e}", file=sys.stderr)
            results[name] = {"error": str(e)}
            continue
            
        lexicon_dict = data.get('lexicon', data)
        if not isinstance(lexicon_dict, dict):
            lexicon_dict = {}
            
        category_counts = {}
        compact_ids = []
        
        for sym, item in lexicon_dict.items():
            if isinstance(item, dict):
                cat = item.get('category', 'unknown')
                category_counts[cat] = category_counts.get(cat, 0) + 1
                
                cid = item.get('compact_id')
                if cid is not None:
                    compact_ids.append(cid)
                    
        results[name] = {
            "total_entries": len(lexicon_dict),
            "category_distribution": category_counts,
            "compact_id_stats": {
                "count": len(compact_ids),
                "min": min(compact_ids) if compact_ids else None,
                "max": max(compact_ids) if compact_ids else None
            }
        }
        
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
