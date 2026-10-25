import sys
import os
import traceback
import time
import json

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "timestamp": time.time(),
        "core_status": "missing",
        "macro_status": "missing",
        "core_stats": {},
        "macro_stats": {}
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            report["core_status"] = "loaded"
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
        
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report["macro_status"] = "loaded"
            report["macro_stats"] = {
                "total_macros": len(macro_data) if isinstance(macro_data, (list, dict)) else 0
            }
            
    except Exception as e:
        report["error"] = str(e)
        report["traceback"] = traceback.format_exc()
        
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(report, out, ensure_ascii=False, indent=2)
    print(f"Audit completed. Report saved to {output_path}")

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        print(f"Error in audit script: {e}")
        traceback.print_exc()
        sys.exit(1)
