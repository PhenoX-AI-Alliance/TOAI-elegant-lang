import sys
import os
import traceback
import json

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    results = {
        "core_lexicon": {"status": "missing", "total_symbols": 0, "categories": {}, "compact_id_stats": {}},
        "macro_lexicon": {"status": "missing", "total_symbols": 0, "categories": {}, "compact_id_stats": {}}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lexicon_data = data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, val in lexicon_data.items():
                    cat = val.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in val:
                        compact_ids.append(val['compact_id'])
                results["core_lexicon"] = {
                    "status": "loaded",
                    "total_symbols": len(lexicon_data),
                    "categories": categories,
                    "compact_id_stats": {
                        "count": len(compact_ids),
                        "min": min(compact_ids) if compact_ids else None,
                        "max": max(compact_ids) if compact_ids else None
                    }
                }
        except Exception as e:
            results["core_lexicon"]["status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lexicon_data = data.get('lexicon', data) if isinstance(data, dict) else {}
                categories = {}
                compact_ids = []
                if isinstance(lexicon_data, dict):
                    for sym, val in lexicon_data.items():
                        if isinstance(val, dict):
                            cat = val.get('category', 'unknown')
                            categories[cat] = categories.get(cat, 0) + 1
                            if 'compact_id' in val:
                                compact_ids.append(val['compact_id'])
                results["macro_lexicon"] = {
                    "status": "loaded",
                    "total_symbols": len(lexicon_data) if isinstance(lexicon_data, dict) else 0,
                    "categories": categories,
                    "compact_id_stats": {
                        "count": len(compact_ids),
                        "min": min(compact_ids) if compact_ids else None,
                        "max": max(compact_ids) if compact_ids else None
                    }
                }
        except Exception as e:
            results["macro_lexicon"]["status"] = f"error: {str(e)}"
            
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
