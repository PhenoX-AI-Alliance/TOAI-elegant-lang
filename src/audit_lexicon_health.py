import sys
import os
import json
import traceback

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "status": "success",
        "core_lexicon_stats": {},
        "macro_lexicon_stats": {},
        "errors": []
    }
    
    try:
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
                report['core_lexicon_stats'] = {
                    "total_entries": len(lexicon_dict),
                    "categories": categories,
                    "total_compact_ids": len(compact_ids)
                }
        else:
            report['errors'].append("core_lexicon.json not found")
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report['macro_lexicon_stats'] = {
                    "total_entries": len(macro_data)
                }
        else:
            report['errors'].append("macro_lexicon.json not found")
            
    except Exception as e:
        report["status"] = "error"
        report["errors"].append(str(e))
        report["traceback"] = traceback.format_exc()
        
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicon()
