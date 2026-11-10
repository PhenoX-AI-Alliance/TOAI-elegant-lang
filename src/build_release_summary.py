import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def run_git_log():
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if not os.path.exists(os.path.join(repo_path, '.git')):
        return "Git repository not found at target path."
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Failed to retrieve git log: {e}"

def generate_summary():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_logs = run_git_log()
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "project": "TOAI-elegant-lang",
        "version": "1.0.0",
        "recent_commits": git_logs,
        "status": "release summary successfully generated with altruistic care."
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully written to {output_file}")

if __name__ == '__main__':
    try:
        generate_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
