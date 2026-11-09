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
        'core_lexicon': {'exists': False, 'categories': {}, 'total_symbols': 0},
        'macro_lexicon': {'exists': False, 'total_macros': 0}
    }
    
    if os.path.exists(core_path):
        report['core_lexicon']['exists'] = True
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            report['core_lexicon']['total_symbols'] = len(lexicon_dict)
            
            categories = {}
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'uncategorized')
                categories[cat] = categories.get(cat, 0) + 1
            report['core_lexicon']['categories'] = categories
        except Exception as e:
            report['core_lexicon']['error'] = str(e)
            
    if os.path.exists(macro_path):
        report['macro_lexicon']['exists'] = True
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            if isinstance(macro_data, dict):
                report['macro_lexicon']['total_macros'] = len(macro_data)
            elif isinstance(macro_data, list):
                report['macro_lexicon']['total_macros'] = len(macro_data)
        except Exception as e:
            report['macro_lexicon']['error'] = str(e)
            
    output_path = os.path.join(lang_dir, 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
