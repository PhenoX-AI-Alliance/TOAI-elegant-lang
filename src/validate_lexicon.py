import sys
import os
import json
from datetime import datetime

def validate():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    lexicon_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'core_lexicon.json')
    report_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(report_dir, env_loader_ok := True, exist_ok=True)
    report_path = os.path.join(report_dir, 'lexicon_validation_report.json')

    errors = []
    total_checked = 0

    if not os.path.exists(lexicon_path):
        print(f"[ERROR] Lexicon file not found: {lexicon_path}")
        sys.exit(1)

    try:
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to parse JSON: {e}")
        sys.exit(1)

    if not isinstance(content, list):
        errors.append("Root element must be a list of entries.")
    else:
        total_checked = len(content)
        required_fields = ['symbol', 'definition', 'japanese']
        for idx, entry in enumerate(content):
            if not isinstance(entry, dict):
                errors.append(f"Entry {idx} is not a dictionary.")
                continue
            missing = [field for field in required_fields if field not in entry or not entry[field]]
            if missing:
                errors.append(f"Entry '{entry.get('symbol', idx)}' missing required fields: {', '.join(missing)}")

    status = "FAILED" if errors else "SUCCESS"
    
    report = {
        "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "target_file": lexicon_path,
        "status": status,
        "total_entries_checked": total_checked,
        "errors": errors
    }

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"OAI_Generated/lexicon_validation_report.json")
    print(json.dumps(report, indent=2, ensure_ascii=False))

    if errors:
        print(f"[ERROR] Lexicon schema validation failed with {len(errors)} error(s).")
        sys.exit(1)
    else:
        print("[SUCCESS] Lexicon schema validation passed.")

if __name__ == '__main__':
    validate()
