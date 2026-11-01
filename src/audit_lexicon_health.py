import sys
import os
import traceback
import time
import json

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lang_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    core_path = os.path.join(lang_dir, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(lang_dir, 'lexicon', 'macro_lexicon.json')
    
    result = {
        "timestamp": time.time(),
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
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
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                if 'compact_id' in data:
                    compact_ids.append(data['compact_id'])
            
            result["core_lexicon_status"] = "loaded"
            result["core_stats"] = {
                "total_entries": len(lexicon_dict),
                "categories": categories,
                "compact_id_count": len(compact_ids),
                "compact_ids_sample": compact_ids[:10]
            }
        except Exception as e:
            result["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            result["macro_lexicon_status"] = "loaded"
            result["macro_stats"] = {
                "total_entries": len(macro_data) if isinstance(macro_data, dict) else 0
            }
        except Exception as e:
            result["macro_lexicon_status"] = f"error: {str(e)}"
            
    out_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, 'lexicon_audit_report.json')
    
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print(f"Audit report successfully generated at: {out_file}")

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
