import sys
import os
import json
from collections import Counter

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    audit_result = {
        'core_lexicon': {},
        'macro_lexicon': {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            categories = []
            compact_ids = []
            for sym, data in lexicon_dict.items():
                if isinstance(data, dict):
                    categories.append(data.get('category', 'unknown'))
                    compact_ids.append(data.get('compact_id', 'unknown'))
            audit_result['core_lexicon'] = {
                'total_symbols': len(lexicon_dict),
                'category_distribution': dict(Counter(categories)),
                'compact_id_stats': {
                    'unique_count': len(set(compact_ids)),
                    'total_count': len(compact_ids)
                }
            }
        except Exception as e:
            audit_result['core_lexicon'] = {'error': str(e)}
    else:
        audit_result['core_lexicon'] = {'error': 'core_lexicon.json not found'}
        
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            audit_result['macro_lexicon'] = {
                'total_macros': len(macro_data) if isinstance(macro_data, (dict, list)) else 0
            }
        except Exception as e:
            audit_result['macro_lexicon'] = {'error': str(e)}
    else:
        audit_result['macro_lexicon'] = {'error': 'macro_lexicon.json not found'}
        
    print(json.dumps(audit_result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
