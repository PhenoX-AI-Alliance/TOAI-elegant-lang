import sys
import os
import traceback
import json

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon": {"status": "missing", "categories": {}, "compact_id_stats": {}},
        "macro_lexicon": {"status": "missing", "total_entries": 0}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_map = core_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            
            for sym, data in lexicon_map.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    cid = data.get('compact_id')
                    if cid is not None:
                        compact_ids.append(cid)
            
            report["core_lexicon"]["status"] = "ok"
            report["core_lexicon"]["categories"] = categories
            report["core_lexicon"]["compact_id_stats"] = {
                "total_count": len(compact_ids),
                "min": min(compact_ids) if compact_ids else None,
                "max": max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            report["core_lexicon"]["status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            if isinstance(macro_data, dict):
                report["macro_lexicon"]["status"] = "ok"
                report["macro_lexicon"]["total_entries"] = len(macro_data)
            elif isinstance(macro_data, list):
                report["macro_lexicon"]["status"] = "ok"
                report["macro_lexicon"]["total_entries"] = len(macro_data)
        except Exception as e:
            report["macro_lexicon"]["status"] = f"error: {str(e)}"
            
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicon()
