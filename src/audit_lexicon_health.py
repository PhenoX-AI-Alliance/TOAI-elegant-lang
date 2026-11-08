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
        'core_lexicon': {'status': 'not_found', 'categories': {}, 'total_symbols': 0},
        'macro_lexicon': {'status': 'not_found', 'total_macros': 0}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            
            lexicon_dict = core_data.get('lexicon', {})
            categories = {}
            total = len(lexicon_dict)
            
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'uncategorized')
                categories[cat] = categories.get(cat, 0) + 1
                
            report['core_lexicon'] = {
                'status': 'success',
                'categories': categories,
                'total_symbols': total
            }
        except Exception as e:
            report['core_lexicon'] = {
                'status': 'error',
                'message': str(e)
            }
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            
            macro_count = len(macro_data) if isinstance(macro_data, (dict, list)) else 0
            report['macro_lexicon'] = {
                'status': 'success',
                'total_macros': macro_count
            }
        except Exception as e:
            report['macro_lexicon'] = {
                'status': 'error',
                'message': str(e)
            }
            
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
