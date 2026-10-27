# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "timestamp": time.time(),
        "core_audit": {},
        "macro_audit": {}
    }
    
    if os.path.exists(core_path):
        try:
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
                    
            result["core_audit"] = {
                "total_entries": len(lexicon_dict),
                "categories": categories,
                "compact_id_count": len(compact_ids),
                "min_compact_id": min(compact_ids) if compact_ids else None,
                "max_compact_id": max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            result["core_audit"] = {"error": str(e)}
    else:
        result["core_audit"] = {"error": "core_lexicon.json not found"}
        
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            result["macro_audit"] = {
                "total_entries": len(macro_data) if isinstance(macro_data, dict) else 0
            }
        except Exception as e:
            result["macro_audit"] = {"error": str(e)}
    else:
        result["macro_audit"] = {"error": "macro_lexicon.json not found"}
        
    out_path = os.path.join(workspace, 'TOAI_Generated', 'lexicon_audit_report.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Audit report successfully generated at: {out_path}")

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
