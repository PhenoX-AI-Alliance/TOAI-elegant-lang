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
        'core_lexicon': {'exists': False, 'total_entries': 0, 'categories': {}, 'compact_id_stats': {}},
        'macro_lexicon': {'exists': False, 'total_entries': 0, 'categories': {}, 'compact_id_stats': {}}
    }
    
    if os.path.exists(core_path):
        report['core_lexicon']['exists'] = True
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
                lexicon_map = core_data.get('lexicon', {})
                report['core_lexicon']['total_entries'] = len(lexicon_map)
                
                categories = {}
                compact_ids = []
                for sym, data in lexicon_map.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                        if 'compact_id' in data:
                            compact_ids.append(data['compact_id'])
                report['core_lexicon']['categories'] = categories
                report['core_lexicon']['compact_id_stats'] = {
                    'count': len(compact_ids),
                    'min': min(compact_ids) if compact_ids else None,
                    'max': max(compact_ids) if compact_ids else None
                }
        except Exception as e:
            report['core_lexicon']['error'] = str(e)
            
    if os.path.exists(macro_path):
        report['macro_lexicon']['exists'] = True
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                lexicon_map = macro_data.get('lexicon', macro_data)
                if isinstance(lexicon_map, dict):
                    report['macro_lexicon']['total_entries'] = len(lexicon_map)
                    categories = {}
                    for sym, data in lexicon_map.items():
                        if isinstance(data, dict):
                            cat = data.get('category', 'unknown')
                            categories[cat] = categories.get(cat, 0) + 1
                    report['macro_lexicon']['categories'] = categories
        except Exception as e:
            report['macro_lexicon']['error'] = str(e)
            
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report

if __name__ == '__main__':
    try:
        audit_lexicons()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
