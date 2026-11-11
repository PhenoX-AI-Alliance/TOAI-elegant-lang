import sys
import os
import json
import traceback

def audit_lexicons():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        'core_audit': {},
        'macro_audit': {},
        'timestamp': time.time() if 'time' in globals() else 0
    }
    
    import time
    result['timestamp'] = time.time()
    
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
                    cid = data.get('compact_id')
                    if cid is not None:
                        compact_ids.append(cid)
            
            result['core_audit'] = {
                'total_symbols': len(lexicon_dict),
                'category_distribution': categories,
                'compact_id_count': len(compact_ids),
                'compact_id_min': min(compact_ids) if compact_ids else None,
                'compact_id_max': max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            result['core_audit'] = {'error': str(e)}
    else:
        result['core_audit'] = {'error': 'core_lexicon.json not found'}
        
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            result['macro_audit'] = {
                'total_macros': len(macro_data) if isinstance(macro_data, dict) else 0
            }
        except Exception as e:
            result['macro_audit'] = {'error': str(e)}
    else:
        result['macro_audit'] = {'error': 'macro_lexicon.json not found'}
        
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    audit_lexicons()
