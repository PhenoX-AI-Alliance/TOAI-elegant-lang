import sys
import os
import json
import traceback

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    output_path = os.path.join(lexicon_dir, 'lexicon_audit_report.json')

    report = {
        'timestamp': os.path.exists(core_path) and os.path.getmtime(core_path) or 0,
        'core_lexicon': {},
        'macro_lexicon': {}
    }

    try:
        if os.path.exists(core_path):
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
                report['core_lexicon'] = {
                    'total_symbols': len(lexicon_map),
                    'category_distribution': categories,
                    'compact_id_count': len(compact_ids)
                }
        else:
            report['core_lexicon'] = {'error': 'core_lexicon.json not found'}

        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report['macro_lexicon'] = {
                    'total_macros': len(macro_data) if isinstance(macro_data, dict) else 0
                }
        else:
            report['macro_lexicon'] = {'error': 'macro_lexicon.json not found'}

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Audit report successfully written to {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
