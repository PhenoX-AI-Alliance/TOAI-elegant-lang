import sys
import os
import json
import traceback

def audit_lexicons():
    try:
        base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        lang_dir = os.path.join(base_dir, 'TOAI-elegant-lang')
        
        core_path = os.path.join(lang_dir, 'lexicon', 'core_lexicon.json')
        macro_path = os.path.join(lang_dir, 'lexicon', 'macro_lexicon.json')
        
        report = {
            'core_lexicon_status': 'missing',
            'macro_lexicon_status': 'missing',
            'core_stats': {},
            'macro_stats': {}
        }
        
        if os.path.exists(core_path):
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
                'total_symbols': len(lexicon_dict),
                'categories': categories,
                'compact_id_count': len(compact_ids),
                'min_compact_id': min(compact_ids) if compact_ids else None,
                'max_compact_id': max(compact_ids) if compact_ids else None
            }
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report['macro_lexicon_status'] = 'loaded'
            report['macro_stats'] = {
                'total_macros': len(macro_data) if isinstance(macro_data, dict) else 0
            }
            
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
