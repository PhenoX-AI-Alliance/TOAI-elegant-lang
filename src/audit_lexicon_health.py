import os
import sys
import json
import traceback

def audit_lexicons():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon')
    
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
            lexicon_dict = core_data.get('lexicon', {})
            categories = {}
            compact_ids = []
            
            for sym, data in lexicon_dict.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
                        
            report['core_lexicon'] = {
                'total_entries': len(lexicon_dict),
                'categories': categories,
                'compact_id_count': len(compact_ids),
                'has_duplicates_compact_id': len(compact_ids) != len(set(compact_ids))
            }
        except Exception as e:
            report['core_lexicon']['error'] = str(e)
    else:
        report['core_lexicon']['error'] = 'core_lexicon.json not found'
        
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report['macro_lexicon'] = {
                'total_entries': len(macro_data) if isinstance(macro_data, dict) else 0
            }
        except Exception as e:
            report['macro_lexicon']['error'] = str(e)
    else:
        report['macro_lexicon']['error'] = 'macro_lexicon.json not found'
        
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    audit_lexicons()
