import os
import json
import sys

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lang_root = os.path.join(workspace, 'TOAI-elegant-lang')
    
    core_path = os.path.join(lang_root, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(lang_root, 'lexicon', 'macro_lexicon.json')
    
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
                "total_symbols": len(lexicon_dict),
                "category_distribution": categories,
                "compact_id_count": len(compact_ids),
                "compact_ids_sample": compact_ids[:10]
            }
    else:
        report["core_lexicon"] = {"error": "core_lexicon.json not found"}
        
    if os.path.exists(macro_path):
        with open(macro_path, 'r', encoding='utf-8') as f:
            macro_data = json.load(f)
            report["macro_lexicon"] = {
                "total_macros": len(macro_data) if isinstance(macro_data, dict) else 0
            }
    else:
        report["macro_lexicon"] = {"error": "macro_lexicon.json not found"}
        
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
