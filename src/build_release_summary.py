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
        print(e.stderr)
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.isdir(repo_dir):
        print(f"Error: Repository directory not found at {repo_dir}")
        sys.exit(1)
        
    git_dir = os.path.join(repo_dir, '.git')
    if not os.path.isdir(git_dir):
        print(f"Error: Not a git repository: {repo_dir}")
        sys.exit(1)
        
    print("Fetching git log...")
    git_log = run_git_command(['git', 'log', '-n', '20', '--oneline'], repo_dir)
    
    whitepaper_path = os.path.join(repo_dir, 'WHITE_PAPER.md')
    whitepaper_content = ""
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            whitepaper_content = f.read()[:1000]
            
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": git_log.splitlines() if git_log else [],
        "whitepaper_snippet": whitepaper_content
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
