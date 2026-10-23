import sys
import os
import subprocess
import json
from datetime import datetime

def run_git_command(args, cwd):
    try:
        res = subprocess.run(
            ['git'] + args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception as e:
        print(f"Git command failed: {e}")
        return ""

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace, 'TOAI-elegant-lang')
    
    if not os.path.isdir(os.path.join(repo_dir, '.git')):
        print("Error: Not a git repository.")
        sys.exit(1)
        
    print("Scanning git log...")
    git_log = run_git_command(['log', '-n', '10', '--pretty=format:%h - %an: %s (%ar)'], repo_dir)
    latest_tag = run_git_command(['describe', '--tags', '--abbrev=0'], repo_dir)
    if not latest_tag:
        latest_tag = "v0.1.0"
        
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "latest_tag": latest_tag,
        "recent_commits": git_log.splitlines() if git_log else []
    }
    
    output_path = os.path.join(repo_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    main()
