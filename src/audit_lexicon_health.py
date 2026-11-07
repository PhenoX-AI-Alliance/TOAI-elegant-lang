import sys
import os
import json
import traceback

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "core_compact_id_stats": {},
        "macro_categories": {}
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
                "total_entries": len(lexicon_dict),
                "has_compact_id_count": len(compact_ids),
                "min_compact_id": min(compact_ids) if compact_ids else None,
                "max_compact_id": max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            result["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            result["macro_lexicon_status"] = "loaded"
            macro_dict = macro_data.get("macro", macro_data)
            macro_cats = {}
            if isinstance(macro_dict, dict):
                for k, v in macro_dict.items():
                    if isinstance(v, dict):
                        cat = v.get("category", "unknown")
                        macro_cats[cat] = macro_cats.get(cat, 0) + 1
            result["macro_categories"] = macro_cats
        except Exception as e:
            result["macro_status"] = f"error: {str(e)}"
            
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    audit_lexicons()
