import sys
import os
import json
import traceback

def audit_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'lexicon')
    
    core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
    macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
    
    result = {
        'core_lexicon_status': 'missing',
        'macro_lexicon_status': 'missing',
        'core_categories': {},
        'macro_categories': {},
        'core_compact_id_stats': {},
        'macro_compact_id_stats': {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon = core_data.get('lexicon', {})
            result['core_lexicon_status'] = 'loaded'
            
            categories = {}
            compact_ids = []
            for sym, data in lexicon.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    cid = data.get('compact_id')
                    if cid is not None:
                        compact_ids.append(cid)
            
            result['core_categories'] = categories
            if compact_ids:
                result['core_compact_id_stats'] = {
                    'count': len(compact_ids),
                    'min': min(compact_ids),
                    'max': max(compact_ids)
                }
        except Exception as e:
            result['core_lexicon_status'] = f'error: {str(e)}'
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            lexicon = macro_data.get('lexicon', macro_data)
            result['macro_lexicon_status'] = 'loaded'
            
            categories = {}
            compact_ids = []
            if isinstance(lexicon, dict):
                for sym, data in lexicon.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                        cid = data.get('compact_id')
                        if cid is not None:
                            compact_ids.append(cid)
            
            result['macro_categories'] = categories
            if compact_ids:
                result['macro_compact_id_stats'] = {
                    'count': len(compact_ids),
                    'min': min(compact_ids),
                    'max': max(compact_ids)
                }
        except Exception as e:
            result['macro_lexicon_status'] = f'error: {str(e)}'
            
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
