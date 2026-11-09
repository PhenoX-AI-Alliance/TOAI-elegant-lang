import sys
import os
import json
import traceback

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon": {},
        "macro_lexicon": {}
    }
    
    if os.path.exists(core_path):
        with open(core_path, 'r', encoding='utf-8') as f:
            core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                if 'compact_id' in data:
                    compact_ids.append(data['compact_id'])
            report["core_lexicon"] = {
                "total_entries": len(lexicon_dict),
                "category_distribution": categories,
                "compact_id_count": len(compact_ids)
            }
            
    if os.path.exists(macro_path):
        with open(macro_path, 'r', encoding='utf-8') as f:
            macro_data = json.load(f)
            if isinstance(macro_data, dict):
                report["macro_lexicon"] = {
                    "total_entries": len(macro_data)
                }
            elif isinstance(macro_data, list):
                report["macro_lexicon"] = {
                    "total_entries": len(macro_data)
                }
                
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
