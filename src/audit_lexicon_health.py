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
                
        if os.path.exists(macro_path):
            with open(macro_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
                
        lexicon_dict = core_data.get('lexicon', {})
        category_counts = {}
        compact_ids = []
        
        for sym, data in lexicon_dict.items():
            if isinstance(data, dict):
                cat = data.get('category', 'unknown')
                category_counts[cat] = category_counts.get(cat, 0) + 1
                if 'compact_id' in data:
                    compact_ids.append(data['compact_id'])
                    
        report = {
            "total_core_entries": len(lexicon_dict),
            "category_distribution": category_counts,
            "compact_id_stats": {
                "total": len(compact_ids),
                "unique": len(set(compact_ids))
            },
            "macro_entries_count": len(macro_data) if isinstance(macro_data, dict) else 0
        }
        
        output_path = os.path.join(base_dir, 'TOAI-elegant-lang', 'lexicon_audit_report.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(f"Audit completed successfully. Report saved to {output_path}")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    audit_lexicons()
