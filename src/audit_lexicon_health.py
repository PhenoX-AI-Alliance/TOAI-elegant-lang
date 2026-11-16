import sys
import os
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    base_lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(base_lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(base_lexicon_dir, 'macro_lexicon.json')
    
    audit_results = {
        'core_lexicon': {},
        'macro_lexicon': {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                if 'compact_id' in data:
                    compact_ids.append(data['compact_id'])
            audit_results['core_lexicon'] = {
                'total_entries': len(lexicon_dict),
                'category_distribution': categories,
                'compact_id_count': len(compact_ids)
            }
        except Exception as e:
            audit_results['core_lexicon'] = {'error': str(e)}
    else:
        audit_results['core_lexicon'] = {'error': 'file not found'}
        
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            audit_results['macro_lexicon'] = {
                'total_entries': len(macro_data) if isinstance(macro_data, dict) else 'non-dict'
            }
        except Exception as e:
            audit_results['macro_lexicon'] = {'error': str(e)}
    else:
        audit_results['macro_lexicon'] = {'error': 'file not found'}
        
    print(json.dumps(audit_results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
