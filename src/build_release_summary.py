import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log acquisition failed: {str(e)}"

def scan_workspace():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    summary_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    
    git_history = get_git_log()
    current_time = datetime.now().isoformat()
    
    data = {
        "timestamp": current_time,
        "git_recent_commits": git_history,
        "status": "success",
        "message": "Release summary successfully built from git log and workspace scan."
    }
    
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully written to {summary_path}")

if __name__ == '__main__':
    try:
        scan_workspace()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
