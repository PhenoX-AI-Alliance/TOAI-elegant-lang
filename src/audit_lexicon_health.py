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
    
    try:
        if os.path.exists(core_path):
            report['core_lexicon']['exists'] = True
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            lexicon_dict = core_data.get('lexicon', {})
            report['core_lexicon']['total_entries'] = len(lexicon_dict)
            
            categories = {}
            compact_ids = []
            for sym, data in lexicon_dict.items():
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
            
        if os.path.exists(macro_path):
            report['macro_lexicon']['exists'] = True
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            macro_dict = macro_data.get('lexicon', macro_data)
            if isinstance(macro_dict, dict):
                report['macro_lexicon']['total_entries'] = len(macro_dict)
                categories = {}
                for sym, data in macro_dict.items():
                    if isinstance(data, dict):
                        cat = data.get('category', 'macro')
                        categories[cat] = categories.get(cat, 0) + 1
                report['macro_lexicon']['categories'] = categories
                
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
