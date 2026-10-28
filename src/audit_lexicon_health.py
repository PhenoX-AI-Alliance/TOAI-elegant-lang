import sys
import os
import traceback
import json

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "macro_categories": {},
        "core_compact_id_stats": {},
        "macro_compact_id_stats": {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            report["core_lexicon_status"] = "loaded"
            lex_dict = core_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            for sym, data in lex_dict.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
            report["core_categories"] = categories
            report["core_compact_id_stats"] = {
                "total_count": len(lex_dict),
                "with_compact_id": len(compact_ids),
                "min_compact_id": min(compact_ids) if compact_ids else None,
                "max_compact_id": max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            report["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report["macro_lexicon_status"] = "loaded"
            lex_dict = macro_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            for sym, data in lex_dict.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
            report["macro_categories"] = categories
            report["macro_compact_id_stats"] = {
                "total_count": len(lex_dict),
                "with_compact_id": len(compact_ids),
                "min_compact_id": min(compact_ids) if compact_ids else None,
                "max_compact_id": max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            report["macro_lexicon_status"] = f"error: {str(e)}"
            
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)