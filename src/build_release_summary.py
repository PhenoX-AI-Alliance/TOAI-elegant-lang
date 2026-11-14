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
        print(f"Git command failed: {cmd}, error: {e}")
        return ""

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        print(f"Repository path does not exist: {repo_path}")
        sys.exit(1)
        
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        print("Target is not a git repository. Initializing...")
        subprocess.run(['git', 'init'], cwd=repo_path, check=True)
        subprocess.run(['git', 'config', 'user.name', 'TOAI Release Agent'], cwd=repo_path, check=True)
        subprocess.run(['git', 'config', 'user.email', 'toai@agent.local'], cwd=repo_path, check=True)
        subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True)
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial commit for release summary'], cwd=repo_path, check=True)
        
    log_output = run_git_command(['git', 'log', '-n', '20', '--pretty=format:%h - %an, %ar : %s'], repo_path)
    
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    whitepaper_content = "No whitepaper found."
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            whitepaper_content = f.read()[:2000] # Read first 2000 chars
            
    summary_data = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "recent_commits": log_output.splitlines() if log_output else [],
        "whitepaper_snippet": whitepaper_content
    }
    
    output_file = os.path.join(repo_path, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
