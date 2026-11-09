import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        "core_lexicon_status": "missing",
        "macro_lexicon_status": "missing",
        "core_categories": {},
        "core_compact_ids": [],
        "macro_categories": {},
        "macro_compact_ids": []
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
                report["core_compact_ids_count"] = len(compact_ids)
        except Exception as e:
            report["core_lexicon_status"] = f"error: {str(e)}"
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report["macro_lexicon_status"] = "loaded"
                lexicon_map = macro_data.get('lexicon', {})
                categories = {}
                compact_ids = []
                for sym, data in lexicon_map.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                        if 'compact_id' in data:
                            compact_ids.append(data['compact_id'])
                report["macro_categories"] = categories
                report["macro_compact_ids_count"] = len(compact_ids)
        except Exception as e:
            report["macro_lexicon_status"] = f"error: {str(e)}"
            
    output_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon_health_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Audit report successfully written to {output_path}")

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
