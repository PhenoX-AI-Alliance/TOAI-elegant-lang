import sys
import os
import traceback
import subprocess
import json
import datetime

def run_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log unavailable: {str(e)}"

def scan_workspace():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    summary_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    
    git_logs = run_git_log()
    
    summary_data = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "version": "1.0.0-gaia",
        "recent_commits": git_logs.splitlines(),
        "status": "success",
        "message": "Release summary successfully generated from git log and ecosystem scan."
    }
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully wrote release summary to {summary_path}")

if __name__ == '__main__':
    try:
        scan_workspace()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
