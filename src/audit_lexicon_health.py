# -*- coding: utf-8 -*-
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
        "timestamp": os.path.exists(core_path) and os.path.getmtime(core_path) or 0,
        "core_stats": {},
        "macro_stats": {},
        "status": "success"
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
                report["core_stats"] = {
                    "total_symbols": len(lexicon_dict),
                    "categories": categories,
                    "compact_id_count": len(compact_ids)
                }
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                macro_dict = macro_data.get('lexicon', {})
                macro_categories = {}
                for sym, data in macro_dict.items():
                    cat = data.get('category', 'unknown')
                    macro_categories[cat] = macro_categories.get(cat, 0) + 1
                report["macro_stats"] = {
                    "total_macros": len(macro_dict),
                    "categories": macro_categories
                }
                
    except Exception as e:
        report["status"] = "error"
        report["error_message"] = str(e)
        report["traceback"] = traceback.format_exc()
        
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
