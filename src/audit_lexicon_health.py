import sys
import os
import json
import traceback

def audit_lexicons():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "timestamp": os.path.getmtime(core_path) if os.path.exists(core_path) else 0,
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_compact_id_stats": {},
        "macro_compact_id_stats": {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            result["core_lexicon_status"] = "loaded"
            lexicon_dict = core_data.get("lexicon", {})
            categories = {}
            compact_ids = []
            for sym, data in lexicon_dict.items():
                cat = data.get("category", "unknown")
                categories[cat] = categories.get(cat, 0) + 1
                if "compact_id" in data:
                    compact_ids.append(data["compact_id"])
            result["core_categories"] = categories
            result["core_compact_id_stats"] = {
                "total_items": len(lexicon_dict),
                "unique_compact_ids": len(set(compact_ids)),
                "min_id": min(compact_ids) if compact_ids else None,
                "max_id": max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            result["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            result["macro_lexicon_status"] = "loaded"
            macro_dict = macro_data.get("lexicon", macro_data) if isinstance(macro_data, dict) else {}
            categories = {}
            compact_ids = []
            for sym, data in macro_dict.items():
                if isinstance(data, dict):
                    cat = data.get("category", "unknown")
                    categories[cat] = categories.get(cat, 0) + 1
                    if "compact_id" in data:
                        compact_ids.append(data["compact_id"])
            result["macro_categories"] = categories
            result["macro_compact_id_stats"] = {
                "total_items": len(macro_dict),
                "unique_compact_ids": len(set(compact_ids))
            }
        except Exception as e:
            result["macro_lexicon_status"] = f"error: {str(e)}"
            
    output_path = os.path.join(base_dir, 'TOAI_Generated', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()