import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def run_git_command(cmd, cwd):
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing {{cmd}}: {{e.stderr.strip()}}"

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace, 'TOAI-elegant-lang')
    
    if not os.path.isdir(os.path.join(repo_dir, '.git')):
        print(f"Error: {{repo_dir}} is not a valid git repository.")
        sys.exit(1)
        
    git_log = run_git_command(['git', 'log', '-n', '10', '--oneline'], repo_dir)
    git_status = run_git_command(['git', 'status', '--porcelain'], repo_dir)
    
    summary = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "recent_commits": git_log.splitlines() if git_log else [],
        "git_status": git_status.splitlines() if git_status else []
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {{output_path}}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
