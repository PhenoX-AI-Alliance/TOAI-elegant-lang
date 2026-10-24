import sys
import os
import json
import traceback

def audit_lexicons(base_dir):
    core_path = os.path.join(base_dir, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(base_dir, 'lexicon', 'macro_lexicon.json')
    
    report = {
        "core_lexicon": {"status": "missing", "total_symbols": 0, "categories": {}, "compact_id_stats": {}},
        "macro_lexicon": {"status": "missing", "total_symbols": 0, "categories": {}, "compact_id_stats": {}}
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
            
            report["core_lexicon"] = {
                "status": "loaded",
                "total_symbols": len(lexicon_dict),
                "categories": categories,
                "compact_id_stats": {
                    "count": len(compact_ids),
                    "min": min(compact_ids) if compact_ids else None,
                    "max": max(compact_ids) if compact_ids else None
                }
            }
        except Exception as e:
            report["core_lexicon"]["status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
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
            
            report["macro_lexicon"] = {
                "status": "loaded",
                "total_symbols": len(lexicon_dict),
                "categories": categories,
                "compact_id_stats": {
                    "count": len(compact_ids),
                    "min": min(compact_ids) if compact_ids else None,
                    "max": max(compact_ids) if compact_ids else None
                }
            }
        except Exception as e:
            report["macro_lexicon"]["status"] = f"error: {str(e)}"
            
    return report

if __name__ == '__main__':
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/TOAI-elegant-lang')
    result = audit_lexicons(base_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
