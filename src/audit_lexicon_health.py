import sys
import os
import json
import traceback

def audit_lexicons():
    try:
        base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        lang_dir = os.path.join(base_dir, 'TOAI-elegant-lang')
        
        core_path = os.path.join(lang_dir, 'lexicon', 'core_lexicon.json')
        macro_path = os.path.join(lang_dir, 'lexicon', 'macro_lexicon.json')
        
        core_data = {}
        macro_data = {}
        
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                
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
                    
        audit_result = {
            "total_core_symbols": len(lexicon_dict),
            "categories": categories,
            "compact_id_stats": {
                "count": len(compact_ids),
                "min": min(compact_ids) if compact_ids else None,
                "max": max(compact_ids) if compact_ids else None
            },
            "macro_loaded": bool(macro_data),
            "timestamp": os.path.getmtime(core_path) if os.path.exists(core_path) else 0
        }
        
        output_path = os.path.join(lang_dir, 'lexicon', 'audit_report.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(audit_result, f, indent=2, ensure_ascii=False)
            
        print(json.dumps(audit_result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
