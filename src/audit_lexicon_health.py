import sys
import os
import json
import traceback

def audit_lexicons():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)
    
    core_path = os.path.join(parent_dir, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(parent_dir, 'lexicon', 'macro_lexicon.json')
    
    report = {
        "core_lexicon": {},
        "macro_lexicon": {}
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon = core_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lexicon.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                        if 'compact_id' in data:
                            compact_ids.append(data['compact_id'])
                report["core_lexicon"] = {
                    "total_symbols": len(lexicon),
                    "category_distribution": categories,
                    "compact_id_count": len(compact_ids)
                }
        else:
            report["core_lexicon"]["error"] = "core_lexicon.json not found"
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report["macro_lexicon"] = {
                    "total_entries": len(macro_data) if isinstance(macro_data, dict) else 0
                }
        else:
            report["macro_lexicon"]["error"] = "macro_lexicon.json not found"
            
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
