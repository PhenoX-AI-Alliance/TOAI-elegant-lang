import os
import sys
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon_audit": {},
        "macro_lexicon_audit": {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
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
            report["core_lexicon_audit"] = {
                "total_entries": len(lexicon_dict),
                "category_distribution": categories,
                "compact_id_count": len(compact_ids),
                "compact_id_stats": {
                    "min": min(compact_ids) if compact_ids else None,
                    "max": max(compact_ids) if compact_ids else None
                }
            }
        except Exception as e:
            report["core_lexicon_audit"] = {"error": str(e)}
    else:
        report["core_lexicon_audit"] = {"error": "core_lexicon.json not found"}
        
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report["macro_lexicon_audit"] = {
                "total_entries": len(macro_data) if isinstance(macro_data, dict) else 0
            }
        except Exception as e:
            report["macro_lexicon_audit"] = {"error": str(e)}
    else:
        report["macro_lexicon_audit"] = {"error": "macro_lexicon.json not found"}
        
    output_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'src', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    audit_lexicons()
