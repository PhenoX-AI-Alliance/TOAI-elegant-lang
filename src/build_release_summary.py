import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def run_git_command(cmd, cwd):
    try:
        res = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return res.stdout.strip()
    except Exception as e:
        print(f"Git command failed: {e}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.isdir(repo_dir):
        print(f"Repository directory does not exist: {repo_dir}")
        sys.exit(1)
        
    os.chdir(repo_dir)
    
    # Check if git repo
    git_check = run_git_command(['git', 'rev-parse', '--is-inside-work-tree'], repo_dir)
    if git_check != 'true':
        print("Not a valid git repository.")
        sys.exit(1)
        
    git_log = run_git_command(['git', 'log', '-n', '10', '--oneline'], repo_dir)
    git_status = run_git_command(['git', 'status', '--porcelain'], repo_dir)
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "recent_commits": git_log.splitlines() if git_log else [],
        "git_status": git_status.splitlines() if git_status else []
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
