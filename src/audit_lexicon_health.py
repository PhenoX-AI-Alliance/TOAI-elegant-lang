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
        "core_stats": {},
        "macro_stats": {},
        "status": "success"
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon = core_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lexicon.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                        if 'compact_id' in data:
                            compact_ids.append(data['compact_id'])
                report["core_stats"] = {
                    "total_symbols": len(lexicon),
                    "categories": categories,
                    "compact_id_count": len(compact_ids)
                }
        else:
            report["core_stats"] = {"error": "core_lexicon.json not found"}
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report["macro_stats"] = {
                    "total_entries": len(macro_data) if isinstance(macro_data, (dict, list)) else 0
                }
        else:
            report["macro_stats"] = {"error": "macro_lexicon.json not found"}
            
        output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'lexicon_audit_report.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicon()
