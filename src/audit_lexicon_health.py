import sys
import os
import traceback
import time
import json

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    results = {
        "timestamp": time.time(),
        "core_lexicon": {},
        "macro_lexicon": {}
    }
    
    if os.path.exists(core_path):
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
            results["core_lexicon"] = {
                "total_symbols": len(lexicon_map),
                "categories": categories,
                "compact_id_count": len(compact_ids),
                "min_compact_id": min(compact_ids) if compact_ids else None,
                "max_compact_id": max(compact_ids) if compact_ids else None
            }
    else:
        results["core_lexicon"]["error"] = "core_lexicon.json not found"

    if os.path.exists(macro_path):
        with open(macro_path, 'r', encoding='utf-8') as f:
            macro_data = json.load(f)
            if isinstance(macro_data, dict):
                results["macro_lexicon"]["total_macros"] = len(macro_data)
                results["macro_lexicon"]["keys"] = list(macro_data.keys())
            elif isinstance(macro_data, list):
                results["macro_lexicon"]["total_macros"] = len(macro_data)
    else:
        results["macro_lexicon"]["error"] = "macro_lexicon.json not found"

    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
