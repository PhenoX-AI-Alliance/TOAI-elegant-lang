import sys
import os
import traceback
import json

def audit_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        'core_lexicon': {},
        'macro_lexicon': {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_map = core_data.get('lexicon', {})
                categories = {}
                for sym, data in lexicon_map.items():
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                result['core_lexicon'] = {
                    'total_symbols': len(lexicon_map),
                    'category_distribution': categories
                }
        except Exception as e:
            result['core_lexicon'] = {'error': str(e)}
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                result['macro_lexicon'] = {
                    'total_macros': len(macro_data) if isinstance(macro_data, dict) else 0
                }
        except Exception as e:
            result['macro_lexicon'] = {'error': str(e)}
            
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
