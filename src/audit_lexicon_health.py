# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json

def audit_lexicon():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lang_dir = os.path.join(base_dir, 'TOAI-elegant-lang')
    lexicon_dir = os.path.join(lang_dir, 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "timestamp": time.time(),
        "core_lexicon": {},
        "macro_lexicon": {}
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
                    cid = data.get('compact_id')
                    if cid is not None:
                        compact_ids.append(cid)
            result["core_lexicon"] = {
                "total_symbols": len(lexicon_dict),
                "categories": categories,
                "compact_id_count": len(compact_ids),
                "compact_ids_min": min(compact_ids) if compact_ids else None,
                "compact_ids_max": max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            result["core_lexicon"]["error"] = str(e)
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            result["macro_lexicon"] = {
                "total_macros": len(macro_data) if isinstance(macro_data, dict) else 0
            }
        except Exception as e:
            result["macro_lexicon"]["error"] = str(e)
            
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
