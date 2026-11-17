import sys
import os
import traceback
import time
import json
import subprocess
import datetime

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
        print(f"Git command error {cmd}: {e}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        print("Error: TOAI-elegant-lang is not a valid git repository.")
        sys.exit(1)
        
    git_log = run_git_command(['git', 'log', '-n', '20', '--oneline'], repo_dir)
    git_status = run_git_command(['git', 'status', '--porcelain'], repo_dir)
    
    whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
    whitepaper_content = ""
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            whitepaper_content = f.read()[:2000]
            
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_log": git_log.splitlines(),
        "git_status": git_status.splitlines(),
        "whitepaper_excerpt": whitepaper_content
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
