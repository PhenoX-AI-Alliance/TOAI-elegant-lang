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
        'core_lexicon_status': 'missing',
        'macro_lexicon_status': 'missing',
        'core_categories': {},
        'macro_categories': {},
        'core_total_entries': 0,
        'macro_total_entries': 0
    }
    
    try:
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            report['core_lexicon_status'] = 'loaded'
            lexicon_dict = core_data.get('lexicon', {})
            report['core_total_entries'] = len(lexicon_dict)
            
            categories = {}
            for sym, data in lexicon_dict.items():
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
            report['core_categories'] = categories
        else:
            report['core_lexicon_status'] = 'not_found'
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            report['macro_lexicon_status'] = 'loaded'
            if isinstance(macro_data, dict):
                report['macro_total_entries'] = len(macro_data)
                macro_cats = {}
                for k, v in macro_data.items():
                    if isinstance(v, dict):
                        cat = v.get('category', 'unknown')
                        macro_cats[cat] = macro_cats.get(cat, 0) + 1
                report['macro_categories'] = macro_cats
            elif isinstance(macro_data, list):
                report['macro_total_entries'] = len(macro_data)
        else:
            report['macro_lexicon_status'] = 'not_found'
            
        output_report_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
        with open(output_report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"Error during lexicon audit: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
