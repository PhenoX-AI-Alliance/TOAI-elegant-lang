import sys
import os
import traceback
import time
import json

def audit_lexicon():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        'timestamp': time.time(),
        'core_lexicon_status': 'missing',
        'macro_lexicon_status': 'missing',
        'core_categories': {},
        'macro_categories': {},
        'core_count': 0,
        'macro_count': 0
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_dict = core_data.get('lexicon', {})
                report['core_count'] = len(lexicon_dict)
                categories = {}
                for sym, data in lexicon_dict.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                report['core_categories'] = categories
                report['core_lexicon_status'] = 'loaded'
        except Exception as e:
            report['core_lexicon_status'] = f'error: {str(e)}'
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                if isinstance(macro_data, dict):
                    report['macro_count'] = len(macro_data)
                    categories = {}
                    for sym, data in macro_data.items():
                        if isinstance(data, dict):
                            cat = data.get('category', 'unknown')
                            categories[cat] = categories.get(cat, 0) + 1
                    report['macro_categories'] = categories
                report['macro_status'] = 'loaded'
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
