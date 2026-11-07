# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

def audit_lexicons():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "core_lexicon": {"status": "missing", "total_symbols": 0, "categories": {}, "compact_id_stats": {}},
        "macro_lexicon": {"status": "missing", "total_symbols": 0, "categories": {}, "compact_id_stats": {}}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lex_dict = core_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            
            for sym, data in lex_dict.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                if 'compact_id' in data:
                    compact_ids.append(data['compact_id'])
            
            result["core_lexicon"] = {
                "status": "loaded",
                "total_symbols": len(lex_dict),
                "categories": categories,
                "compact_id_stats": {
                    "count": len(compact_ids),
                    "min": min(compact_ids) if compact_ids else None,
                    "max": max(compact_ids) if compact_ids else None
                }
            }
        except Exception as e:
            result["core_lexicon"]["status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            lex_dict = macro_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            
            for sym, data in lex_dict.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                if 'compact_id' in data:
                    compact_ids.append(data['compact_id'])
            
            result["macro_lexicon"] = {
                "status": "loaded",
                "total_symbols": len(lex_dict),
                "categories": categories,
                "compact_id_stats": {
                    "count": len(compact_ids),
                    "min": min(compact_ids) if compact_ids else None,
                    "max": max(compact_ids) if compact_ids else None
                }
            }
        except Exception as e:
            result["macro_lexicon"]["status"] = f"error: {str(e)}"
            
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
