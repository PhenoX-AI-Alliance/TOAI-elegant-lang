import sys
import os
import json
import traceback

def audit():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "category_distribution": {},
        "compact_id_stats": {}
    }
    
    categories = {}
    compact_ids = []
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lexicon_data = data.get("lexicon", {})
                report["core_lexicon_status"] = "loaded"
                for sym, val in lexicon_data.items():
                    cat = val.get("category", "unknown")
                    categories[cat] = categories.get(cat, 0) + 1
                    cid = val.get("compact_id")
                    if cid is not None:
                        compact_ids.append(cid)
        except Exception as e:
            report["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                macros_data = data.get("macros", {})
                report["macro_lexicon_status"] = "loaded"
                for sym, val in macros_data.items():
                    cat = val.get("category", "macro")
                    categories[cat] = categories.get(cat, 0) + 1
                    cid = val.get("compact_id")
                    if cid is not None:
                        compact_ids.append(cid)
        except Exception as e:
            report["macro_lexicon_status"] = f"error: {str(e)}"
            
    report["category_distribution"] = categories
    if compact_ids:
        report["compact_id_stats"] = {
            "min": min(compact_ids),
            "max": max(compact_ids),
            "count": len(compact_ids)
        }
    else:
        report["compact_id_stats"] = {"count": 0}
        
    output_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon', 'audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
