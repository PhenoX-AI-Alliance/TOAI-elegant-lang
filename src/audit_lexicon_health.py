import sys
import os
import json
import traceback

def audit_lexicons():
    try:
        base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        lexicon_dir = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon')
        
        core_path = os.path.join(lexicon_dir, 'core_lexicon.json')
        macro_path = os.path.join(lexicon_dir, 'macro_lexicon.json')
        
        core_data = {}
        macro_data = {}
        
        if os.path.exists(core_path):
            with open(core_path, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
        else:
            print(f"Warning: {core_path} not found.")
            
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
        else:
            print(f"Warning: {macro_path} not found.")
            
        lexicon_dict = core_data.get('lexicon', {})
        
        category_counts = {}
        compact_ids = []
        
        for sym, data in lexicon_dict.items():
            if isinstance(data, dict):
                cat = data.get('category', 'unknown')
                category_counts[cat] = category_counts.get(cat, 0) + 1
                
                cid = data.get('compact_id')
                if cid is not None:
                    compact_ids.append(cid)
                    
        compact_stats = {}
        if compact_ids:
            compact_stats = {
                'min': min(compact_ids),
                'max': max(compact_ids),
                'count': len(compact_ids),
                'unique_count': len(set(compact_ids))
            }
            
        audit_result = {
            'timestamp': time.time(),
            'total_core_entries': len(lexicon_dict),
            'category_distribution': category_counts,
            'compact_id_stats': compact_stats,
            'macro_entries_count': len(macro_data) if isinstance(macro_data, dict) else 0
        }
        
        output_path = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(audit_result, f, ensure_ascii=False, indent=2)
            
        print(json.dumps(audit_result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    import time
    audit_lexicons()
