# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def run_git_command(cmd, cwd):
    try:
        res = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception as e:
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.isdir(repo_dir):
        print(f"Error: Repository directory not found at {repo_dir}")
        sys.exit(1)
        
    git_check = run_git_command(['git', 'rev-parse', '--is-inside-work-tree'], repo_dir)
    if git_check != 'true':
        print("Error: Not a valid git repository.")
        sys.exit(1)
        
    commit_log = run_git_command(['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'], repo_dir)
    latest_tag = run_git_command(['git', 'describe', '--tags', '--abbrev=0'], repo_dir)
    if not latest_tag:
        latest_tag = "v0.1.0-alpha"
        
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "latest_tag": latest_tag,
        "recent_commits": commit_log.splitlines() if commit_log else []
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
