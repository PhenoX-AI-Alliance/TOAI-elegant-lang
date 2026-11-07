import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    elegant_lang_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    core_path = os.path.join(elegant_lang_dir, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(elegant_lang_dir, 'lexicon', 'macro_lexicon.json')
    
    report = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_stats": {},
        "macro_stats": {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            report["core_lexicon_status"] = "loaded"
            lexicon_dict = core_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            
            for sym, data in lexicon_dict.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    cid = data.get('compact_id')
                    if cid is not None:
                        compact_ids.append(cid)
                        
            report["core_stats"] = {
                "total_entries": len(lexicon_dict),
                "category_distribution": categories,
                "compact_id_count": len(compact_ids),
                "compact_id_min": min(compact_ids) if compact_ids else None,
                "compact_id_max": max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            report["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report["macro_lexicon_status"] = "loaded"
            report["macro_stats"] = {
                "total_entries": len(macro_data) if isinstance(macro_data, (dict, list)) else 0
            }
        except Exception as e:
            report["macro_lexicon_status"] = f"error: {str(e)}"
            
    output_path = os.path.join(elegant_lang_dir, 'lexicon', 'audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
