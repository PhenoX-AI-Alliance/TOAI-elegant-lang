import sys
import os
import json
import traceback

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        "core_status": "missing",
        "macro_status": "missing",
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
            result["core_status"] = "ok"
            result["core_stats"] = {
                "total_symbols": len(lexicon_dict),
                "categories": categories,
                "total_compact_ids": len(compact_ids)
            }
        except Exception as e:
            result["core_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            result["macro_status"] = "ok"
            result["macro_stats"] = {
                "total_macros": len(macro_data) if isinstance(macro_data, dict) else 0
            }
        except Exception as e:
            result["macro_status"] = f"error: {str(e)}"
            
    output_audit_path = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
    with open(output_audit_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        
    print(f"Audit completed. Report saved to {output_audit_path}")

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
