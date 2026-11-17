import os
import sys
import json
import traceback

def audit_lexicons():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    report = {
        'core_lexicon': {},
        'macro_lexicon': {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lex_dict = core_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            
            for sym, data in lex_dict.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    cid = data.get('compact_id')
                    if cid is not None:
                        compact_ids.append(cid)
                        
            report['core_lexicon'] = {
                'total_symbols': len(lex_dict),
                'categories': categories,
                'compact_id_count': len(compact_ids),
                'compact_id_min': min(compact_ids) if compact_ids else None,
                'compact_id_max': max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            report['core_lexicon'] = {'error': str(e)}
    else:
        report['core_lexicon'] = {'error': 'file not found'}
        
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            if isinstance(macro_data, dict):
                report['macro_lexicon'] = {
                    'total_macros': len(macro_data),
                    'keys': list(macro_data.keys())
                }
            elif isinstance(macro_data, list):
                report['macro_lexicon'] = {
                    'total_macros': len(macro_data)
                }
            else:
                report['macro_lexicon'] = {'total_macros': 0}
        except Exception as e:
            report['macro_lexicon'] = {'error': str(e)}
    else:
        report['macro_lexicon'] = {'error': 'file not found'}
        
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
