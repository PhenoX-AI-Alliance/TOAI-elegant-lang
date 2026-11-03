import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon": {},
        "macro_lexicon": {},
        "timestamp": os.path.exists(core_path)
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_dict = core_data.get("lexicon", {})
                categories = {}
                compact_ids = []
                for sym, info in lexicon_dict.items():
                    cat = info.get("category", "unknown")
                    categories[cat] = categories.get(cat, 0) + 1
                    cid = info.get("compact_id")
                    if cid is not None:
                        compact_ids.append(cid)
                report["core_lexicon"] = {
                    "total_entries": len(lexicon_dict),
                    "categories": categories,
                    "compact_id_count": len(compact_ids),
                    "min_compact_id": min(compact_ids) if compact_ids else None,
                    "max_compact_id": max(compact_ids) if compact_ids else None
                }
        else:
            report["core_lexicon"]["error"] = "core_lexicon.json not found"
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                macros_dict = macro_data.get("macros", {})
                report["macro_lexicon"] = {
                    "total_entries": len(macros_dict)
                }
        else:
            report["macro_lexicon"]["error"] = "macro_lexicon.json not found"
            
    except Exception as e:
        report["audit_error"] = str(e)
        
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
