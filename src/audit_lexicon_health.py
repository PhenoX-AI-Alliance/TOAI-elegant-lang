import sys
import os
import traceback
import time
import json

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    core_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon', 'macro_lexicon.json')
    output_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon', 'lexicon_audit_report.json')

    report = {
        "timestamp": time.time(),
        "core_lexicon": {},
        "macro_lexicon": {}
    }

    try:
        if os.path.exists(core_path):
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
                report['core_lexicon'] = {
                    "total_entries": len(lexicon),
                    "categories": categories,
                    "compact_id_count": len(compact_ids)
                }
        else:
            report['core_lexicon'] = {"error": "core_lexicon.json not found"}

        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report['macro_lexicon'] = {
                    "total_entries": len(macro_data) if isinstance(macro_data, dict) else 0
                }
        else:
            report['macro_lexicon'] = {"error": "macro_lexicon.json not found"}

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print("Audit report successfully generated at:", output_path)

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
