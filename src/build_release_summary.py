import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        res = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper(workspace_dir):
    notes = []
    try:
        for root, dirs, files in os.walk(workspace_dir):
            for file in files:
                if 'whitepaper' in file.lower() or 'summary' in file.lower() or 'release' in file.lower():
                    full_path = os.path.join(root, file)
                    notes.append(full_path)
    except Exception as e:
        notes.append(f"Scan error: {str(e)}")
    return notes

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    logs = get_git_log()
    papers = scan_whitepaper(workspace)
    
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "recent_commits": logs,
        "related_documents": papers
    }
    
    out_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"Successfully generated release summary at: {out_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
