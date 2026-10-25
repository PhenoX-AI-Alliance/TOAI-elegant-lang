import sys
import os
import json
from collections import Counter

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    core_path = os.path.join(workspace_dir, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(workspace_dir, 'lexicon', 'macro_lexicon.json')
    
    results = {
        "core_lexicon": {},
        "macro_lexicon": {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            categories = Counter()
            compact_ids = []
            for sym, data in lexicon_dict.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories[cat] += 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
            results["core_lexicon"] = {
                "total_symbols": len(lexicon_dict),
                "category_distribution": dict(categories),
                "compact_id_count": len(compact_ids)
            }
        except Exception as e:
            results["core_lexicon"] = {"error": str(e)}
    else:
        results["core_lexicon"] = {"error": "file not found"}
        
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            if isinstance(macro_data, dict):
                results["macro_lexicon"] = {
                    "total_entries": len(macro_data),
                    "keys": list(macro_data.keys())
                }
            elif isinstance(macro_data, list):
                results["macro_lexicon"] = {
                    "total_entries": len(macro_data)
                }
        except Exception as e:
            results["macro_lexicon"] = {"error": str(e)}
    else:
        results["macro_lexicon"] = {"error": "file not found"}
        
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
