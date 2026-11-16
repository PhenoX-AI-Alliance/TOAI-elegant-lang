import sys
import os
import traceback
import time
import json

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        'timestamp': time.time(),
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
            report['core_lexicon'] = {
                'total_symbols': len(lexicon_dict),
                'categories': categories,
                'compact_id_count': len(compact_ids),
                'compact_id_min': min(compact_ids) if compact_ids else None,
                'compact_id_max': max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            report['core_lexicon'] = {'error': str(e)}
    else:
        report['core_lexicon'] = {'error': 'core_lexicon.json not found'}
        
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            if isinstance(macro_data, dict):
                m_dict = macro_data.get('lexicon', macro_data)
                report['macro_lexicon'] = {
                    'total_macros': len(m_dict)
                }
            else:
                report['macro_lexicon'] = {'total_macros': len(macro_data)}
        except Exception as e:
            report['macro_lexicon'] = {'error': str(e)}
    else:
        report['macro_lexicon'] = {'error': 'macro_lexicon.json not found'}
        
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
