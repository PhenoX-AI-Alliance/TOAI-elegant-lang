import sys
import os
import traceback
import time
import json
import subprocess
import datetime

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
        print(f"Git command failed: {' '.join(cmd)}")
        print(e.stderr.strip())
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_dir):
        print(f"Repository directory not found: {repo_dir}")
        sys.exit(1)
        
    git_dir = os.path.join(repo_dir, '.git')
    if not os.path.exists(git_dir):
        print(f"Not a git repository: {repo_dir}")
        sys.exit(1)
        
    print("Fetching recent git commits...")
    log_output = run_git_command(['git', 'log', '-n', '20', '--pretty=format:%h - %an, %ar : %s'], repo_dir)
    
    whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
    whitepaper_summary = "Whitepaper not found."
    if os.path.exists(whitepaper_path):
        print("Reading WHITEPAPER.md...")
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            whitepaper_summary = "".join(lines[:15])
            
    summary_data = {
        "generated_at": datetime.datetime.now().isoformat(),
        "git_log": log_output.splitlines() if log_output else [],
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    print(f"Saving release summary to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print("Release summary successfully generated.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
