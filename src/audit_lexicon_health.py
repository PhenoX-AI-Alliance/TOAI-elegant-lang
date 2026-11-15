import sys
import os
import json
import traceback

def audit_lexicons():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    elegant_lang_dir = os.path.join(base_dir, 'TOAI-elegant-lang')
    
    core_path = os.path.join(elegant_lang_dir, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(elegant_lang_dir, 'lexicon', 'macro_lexicon.json')
    
    report = {
        "timestamp": os.path.getmtime(core_path) if os.path.exists(core_path) else 0,
        "core_lexicon": {"exists": False, "category_distribution": {}, "compact_id_stats": {}},
        "macro_lexicon": {"exists": False, "category_distribution": {}, "compact_id_stats": {}}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            report["core_lexicon"]["exists"] = True
            lexicon_dict = core_data.get("lexicon", {})
            categories = {}
            compact_ids = []
            for sym, data in lexicon_dict.items():
                if isinstance(data, dict):
                    cat = data.get("category", "unknown")
                    categories[cat] = categories.get(cat, 0) + 1
                    if "compact_id" in data:
                        compact_ids.append(data["compact_id"])
            report["core_lexicon"]["category_distribution"] = categories
            report["core_lexicon"]["compact_id_stats"] = {
                "total_entries": len(lexicon_dict),
                "with_compact_id": len(compact_ids),
                "min": min(compact_ids) if compact_ids else None,
                "max": max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            report["core_lexicon"]["error"] = str(e)
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report["macro_lexicon"]["exists"] = True
            lexicon_dict = macro_data.get("lexicon", {})
            categories = {}
            compact_ids = []
            for sym, data in lexicon_dict.items():
                if isinstance(data, dict):
                    cat = data.get("category", "unknown")
                    categories[cat] = categories.get(cat, 0) + 1
                    if "compact_id" in data:
                        compact_ids.append(data["compact_id"])
            report["macro_lexicon"]["category_distribution"] = categories
            report["macro_lexicon"]["compact_id_stats"] = {
                "total_entries": len(lexicon_dict),
                "with_compact_id": len(compact_ids),
                "min": min(compact_ids) if compact_ids else None,
                "max": max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            report["macro_lexicon"]["error"] = str(e)
            
    output_path = os.path.join(elegant_lang_dir, 'lexicon', 'audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
