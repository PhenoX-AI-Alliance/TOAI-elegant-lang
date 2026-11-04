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
        'core_lexicon_status': 'missing',
        'macro_lexicon_status': 'missing',
        'core_categories': {},
        'macro_categories': {},
        'core_total_count': 0,
        'macro_total_count': 0
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                report['core_lexicon_status'] = 'loaded'
                lex_dict = core_data.get('lexicon', {})
                report['core_total_count'] = len(lex_dict)
                for sym, data in lex_dict.items():
                    cat = data.get('category', 'unknown')
                    report['core_categories'][cat] = report['core_categories'].get(cat, 0) + 1
        else:
            report['core_lexicon_status'] = 'not_found'
    except Exception as e:
        report['core_lexicon_status'] = f'error: {str(e)}'

    try:
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                report['macro_lexicon_status'] = 'loaded'
                macro_dict = macro_data.get('macro_lexicon', macro_data)
                if isinstance(macro_dict, dict):
                    report['macro_total_count'] = len(macro_dict)
                    for sym, data in macro_dict.items():
                        if isinstance(data, dict):
                            cat = data.get('category', 'macro')
                            report['macro_categories'][cat] = report['macro_categories'].get(cat, 0) + 1
        else:
            report['macro_lexicon_status'] = 'not_found'
    except Exception as e:
        report['macro_lexicon_status'] = f'error: {str(e)}'

    output_report_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
    with open(output_report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
