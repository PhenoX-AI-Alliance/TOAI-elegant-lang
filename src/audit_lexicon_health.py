import sys
import os
import json
import traceback

def audit_lexicons():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lang_dir = os.path.join(base_dir, 'TOAI-elegant-lang')
    lexicon_dir = os.path.join(lang_dir, 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "status": "success",
        "core_lexicon": {},
        "macro_lexicon": {},
        "errors": []
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
                report["core_lexicon"] = {
                    "total_symbols": len(lexicon_dict),
                    "categories": categories,
                    "compact_id_count": len(compact_ids),
                    "compact_id_min": min(compact_ids) if compact_ids else None,
                    "compact_id_max": max(compact_ids) if compact_ids else None
                }
        else:
            report["errors"].append(f"Core lexicon not found at {core_path}")
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report["macro_lexicon"] = {
                    "total_macros": len(macro_data) if isinstance(macro_data, dict) else 0
                }
        else:
            report["errors"].append(f"Macro lexicon not found at {macro_path}")
            
        output_path = os.path.join(base_dir, 'TOAI_Generated', 'lexicon_audit_report.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"Audit report successfully written to {output_path}")
        
    except Exception as e:
        print(f"Error during lexicon audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
