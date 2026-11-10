import sys
import os
import json
import traceback

def audit_lexicons():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
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
                report['core_lexicon_status'] = 'loaded'
                cats = {}
                for sym, val in lexicon_dict.items():
                    cat = val.get('category', 'unknown')
                    cats[cat] = cats.get(cat, 0) + 1
                report['core_categories'] = cats
        except Exception as e:
            report['core_lexicon_status'] = f'error: {str(e)}'
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                if isinstance(macro_data, dict):
                    report['macro_count'] = len(macro_data)
                    report['macro_lexicon_status'] = 'loaded'
                    cats = {}
                    for sym, val in macro_data.items():
                        cat = val.get('category', 'unknown') if isinstance(val, dict) else 'unknown'
                        cats[cat] = cats.get(cat, 0) + 1
                    report['macro_categories'] = cats
        except Exception as e:
            report['macro_lexicon_status'] = f'error: {str(e)}'
            
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    audit_lexicons()
