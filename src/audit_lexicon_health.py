import sys
import os
import json
from collections import Counter

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon": {},
        "macro_lexicon": {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            categories = []
            compact_ids = []
            for sym, data in lexicon_dict.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories.append(cat)
                    cid = data.get('compact_id')
                    if cid is not None:
                        compact_ids.append(cid)
            report["core_lexicon"] = {
                "total_entries": len(lexicon_dict),
                "category_distribution": dict(Counter(categories)),
                "compact_id_stats": {
                    "total_compact_ids": len(compact_ids),
                    "unique_compact_ids": len(set(compact_ids))
                }
            }
        except Exception as e:
            report["core_lexicon"]["error"] = str(e)
    else:
        report["core_lexicon"]["error"] = "File not found"
        
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            if isinstance(macro_data, dict):
                report["macro_lexicon"] = {
                    "total_entries": len(macro_data),
                    "keys": list(macro_data.keys())
                }
            elif isinstance(macro_data, list):
                report["macro_lexicon"] = {
                    "total_entries": len(macro_data)
                }
        except Exception as e:
            report["macro_lexicon"]["error"] = str(e)
    else:
        report["macro_lexicon"]["error"] = "File not found"
        
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    audit_lexicons()
