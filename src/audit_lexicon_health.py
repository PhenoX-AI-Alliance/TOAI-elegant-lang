import sys
import os
import json
import traceback

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    base_lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(base_lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(base_lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_stats": {},
        "macro_stats": {}
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
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
                        
            report["core_stats"] = {
                "total_symbols": len(lexicon_dict),
                "categories": categories,
                "compact_id_count": len(compact_ids)
            }
        except Exception as e:
            report["core_stats"]["error"] = str(e)
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            if isinstance(macro_data, dict):
                macro_count = len(macro_data.get('macros', macro_data))
                report["macro_stats"] = {
                    "total_macros": macro_count
                }
        except Exception as e:
            report["macro_stats"]["error"] = str(e)
            
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    audit_lexicons()
