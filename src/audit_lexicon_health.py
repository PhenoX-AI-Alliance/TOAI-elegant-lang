import sys
import os
import json
import traceback

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    if not workspace.endswith('/'):
        workspace += '/'
    
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon": {"exists": False, "category_distribution": {}, "compact_id_stats": {}},
        "macro_lexicon": {"exists": False, "category_distribution": {}, "compact_id_stats": {}}
    }
    
    if os.path.exists(core_path):
        report["core_lexicon"]["exists"] = True
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_map = core_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
                report["core_lexicon"]["category_distribution"] = categories
                report["core_lexicon"]["compact_id_stats"] = {
                    "total_entries": len(lexicon_map),
                    "unique_compact_ids": len(set(compact_ids)),
                    "min_compact_id": min(compact_ids) if compact_ids else None,
                    "max_compact_id": max(compact_ids) if compact_ids else None
                }
        except Exception as e:
            report["core_lexicon"]["error"] = str(e)
            
    if os.path.exists(macro_path):
        report["macro_lexicon"]["exists"] = True
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                lexicon_map = macro_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
                report["macro_lexicon"]["category_distribution"] = categories
                report["macro_lexicon"]["compact_id_stats"] = {
                    "total_entries": len(lexicon_map),
                    "unique_compact_ids": len(set(compact_ids)),
                    "min_compact_id": min(compact_ids) if compact_ids else None,
                    "max_compact_id": max(compact_ids) if compact_ids else None
                }
        except Exception as e:
            report["macro_lexicon"]["error"] = str(e)
            
    output_path = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
