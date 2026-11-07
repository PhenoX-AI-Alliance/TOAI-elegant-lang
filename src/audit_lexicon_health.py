import sys
import os
import json
import traceback

def audit_lexicon():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lang_dir = os.path.join(base_dir, 'TOAI-elegant-lang')
    
    core_path = os.path.join(lang_dir, 'lexicon', 'core_lexicon.json')
    macro_path = os.path.join(lang_dir, 'lexicon', 'macro_lexicon.json')
    
    report = {
        'core_lexicon_status': 'missing',
        'macro_lexicon_status': 'missing',
        'core_categories': {},
        'core_compact_id_stats': {},
        'macro_categories': {}
    }
    
    if os.path.exists(core_path):
        try:
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            report['core_lexicon_status'] = 'loaded'
            lexicon_dict = core_data.get('lexicon', {})
            cat_counts = {}
            compact_ids = []
            for sym, data in lexicon_dict.items():
                if isinstance(data, dict):
                    cat = data.get('category', 'unknown')
                    cat_counts[cat] = cat_counts.get(cat, 0) + 1
                    if 'compact_id' in data:
                        compact_ids.append(data['compact_id'])
            report['core_categories'] = cat_counts
            report['core_compact_id_stats'] = {
                'total_items': len(lexicon_dict),
                'with_compact_id': len(compact_ids),
                'min_compact_id': min(compact_ids) if compact_ids else None,
                'max_compact_id': max(compact_ids) if compact_ids else None
            }
        except Exception as e:
            report['core_lexicon_status'] = f'error: {str(e)}'
            
    if os.path.exists(macro_path):
        try:
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report['macro_lexicon_status'] = 'loaded'
            macro_dict = macro_data.get('macros', macro_data)
            macro_cats = {}
            if isinstance(macro_dict, dict):
                for m_name, m_data in macro_dict.items():
                    if isinstance(m_data, dict):
                        cat = m_data.get('category', 'unknown')
                        macro_cats[cat] = macro_cats.get(cat, 0) + 1
            report['macro_categories'] = macro_cats
        except Exception as e:
            report['macro_lexicon_status'] = f'error: {str(e)}'
            
    output_path = os.path.join(lang_dir, 'lexicon', 'lexicon_audit_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try:
        audit_lexicon()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
