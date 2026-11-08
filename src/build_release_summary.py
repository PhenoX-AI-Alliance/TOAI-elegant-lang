import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def run_git_log():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        return "Git repository not found at target path."
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Git command failed: {e.stderr}"

def generate_summary():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_logs = run_git_log()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    summary_data = {
        "timestamp": timestamp,
        "ecosystem": "Gaia Ecosystem - TOAI Elegant Lang",
        "git_recent_logs": git_logs,
        "status": "Release summary generated successfully with altruistic intent."
    }
    
    out_file = os.path.join(output_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully written to {out_file}")

if __name__ == '__main__':
    try:
        generate_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
