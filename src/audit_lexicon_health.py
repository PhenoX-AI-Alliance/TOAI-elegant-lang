import sys
import os
import json
import time
import traceback

def audit_lexicon():
    """
    Reads lexicon files and generates a health report including category distribution 
    and compact_id statistics.
    """
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        project_root = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        core_lex_path = os.path.join(project_root, 'lexicon', 'core_lexicon.json')
        macro_lex_path = os.path.join(project_root, 'lexicon', 'macro_lexicon.json')
        
        # Output results to TOAI_Generated as per environment rules
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        report_path = os.path.join(output_dir, 'lexicon_health_report.json')

        report = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "core_lexicon": {},
            "macro_lexicon": {},
            "summary": {"status": "partial"}
        }

        # 1. Audit Core Lexicon
        if os.path.exists(core_lex_path):
            with open(core_lex_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            lexicon = raw_data.get('lexicon', {})
            total_entries = len(lexicon)
            
            category_dist = {}
            compact_ids = []
            missing_cid = 0

            for sym, entry in lexicon.items():
                # Category stats
                cat = entry.get('category', 'unspecified')
                category_dist[cat] = category_dist.get(cat, 0) + 1
                
                # Compact ID stats
                cid = entry.get('compact_id')
                if cid is not None:
                    compact_ids.append(cid)
                else:
                    missing_cid += 1
            
            unique_cids = set(compact_ids)
            duplicates = len(compact_ids) - len(unique_cids)
            
            report["core_lexicon"] = {
                "file_path": core_lex_path,
                "total_symbols": total_entries,
                "category_distribution": category_dist,
                "compact_id_stats": {
                    "count": len(compact_ids),
                    "missing": missing_cid,
                    "unique_count": len(unique_cids),
                    "duplicates": duplicates,
                    "min": min(compact_ids) if compact_ids else None,
                    "max": max(compact_ids) if compact_ids else None
                }
            }
        else:
            report["core_lexicon"] = {"error": f"File not found: {core_lex_path}"}

        # 2. Audit Macro Lexicon
        if os.path.exists(macro_lex_path):
            with open(macro_lex_path, 'r', encoding='utf-8') as f:
                macro_data = json.load(f)
            
            macro_count = len(macro_data)
            macro_cats = {}
            for m_key, m_val in macro_data.items():
                if isinstance(m_val, dict):
                    m_cat = m_val.get('category', 'macro_unspecified')
                    macro_cats[m_cat] = macro_cats.get(m_cat, 0) + 1
            
            report["macro_lexicon"] = {
                "file_path": macro_lex_path,
                "total_macros": macro_count,
                "category_distribution": macro_cats
            }
        else:
            report["macro_lexicon"] = {"error": f"File not found: {macro_lex_path}"}

        report["summary"]["status"] = "success"

        # Write output
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        
        print(f"Health audit completed. Report saved to: {report_path}")

    except Exception as e:
        print(f"Error during lexicon audit: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    audit_lexicon()
