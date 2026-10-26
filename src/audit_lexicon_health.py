import sys
import os
import traceback
import time
import json

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "timestamp": time.time(),
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "core_compact_id_stats": {},
        "macro_categories": {},
        "macro_compact_id_stats": {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                report["core_lexicon_status"] = "loaded"
                lexicon_map = core_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lexicon_map.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                        if 'compact_id' in data:
                            compact_ids.append(data['compact_id'])
                report["core_categories"] = categories
                report["core_compact_id_stats"] = {
                    "total_items": len(lexicon_map),
                    "unique_compact_ids": len(set(compact_ids)),
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
                lexicon_map = macro_data.get('lexicon', macro_data)
                if isinstance(lexicon_map, dict):
                    categories = {}
                    compact_ids = []
                    for sym, data in lexicon_map.items():
                        if isinstance(data, dict):
                            cat = data.get('category', 'unknown')
                            categories[cat] = categories.get(cat, 0) + 1
                            if 'compact_id' in data:
                                compact_ids.append(data['compact_id'])
                    report["macro_categories"] = categories
                    report["macro_compact_id_stats"] = {
                        "total_items": len(lexicon_map),
                        "unique_compact_ids": len(set(compact_ids)),
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
