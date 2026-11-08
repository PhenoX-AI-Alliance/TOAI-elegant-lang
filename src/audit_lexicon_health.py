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
        'core_lexicon_status': 'not_found',
        'macro_lexicon_status': 'not_found',
        'core_stats': {},
        'macro_stats': {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            report['core_lexicon_status'] = 'loaded'
            lexicon_dict = core_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                if 'compact_id' in data:
                    compact_ids.append(data['compact_id'])
            report['core_stats'] = {
                'total_entries': len(lexicon_dict),
                'categories': categories,
                'compact_id_count': len(compact_ids)
            }
        except Exception as e:
            report['core_lexicon_status'] = f'error: {str(e)}'
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report['macro_lexicon_status'] = 'loaded'
            if isinstance(macro_data, dict):
                report['macro_stats'] = {
                    'total_entries': len(macro_data),
                    'keys': list(macro_data.keys())
                }
            elif isinstance(macro_data, list):
                report['macro_stats'] = {
                    'total_entries': len(macro_data)
                }
        except Exception as e:
            report['macro_lexicon_status'] = f'error: {str(e)}'
            
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
