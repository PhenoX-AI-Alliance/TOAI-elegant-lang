import sys
import os
import json
import traceback

def audit_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lang_root = os.path.join(workspace, 'TOAI-elegant-lang')
    
    core_path = os.path.join(lang_root, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(lang_root, 'lexicon', 'macro_lexicon.json')
    
    report = {
        "timestamp": os.path.exists(core_path) and os.path.getmtime(core_path) or 0,
        "core_lexicon": {},
        "macro_lexicon": {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon = core_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lexicon.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
                report["core_lexicon"] = {
                    "total_symbols": len(lexicon),
                    "categories": categories,
                    "compact_id_count": len(compact_ids),
                    "min_compact_id": min(compact_ids) if compact_ids else None,
                    "max_compact_id": max(compact_ids) if compact_ids else None
                }
        except Exception as e:
            report["core_lexicon"]["error"] = str(e)
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report["macro_lexicon"] = {
                    "total_macros": len(macro_data) if isinstance(macro_data, dict) else 0
                }
        except Exception as e:
            report["macro_lexicon"]["error"] = str(e)
            
    output_path = os.path.join(lang_root, 'lexicon', 'audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
