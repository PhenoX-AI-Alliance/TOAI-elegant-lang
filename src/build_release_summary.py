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
        print(f"Git command failed: {e}", file=sys.stderr)
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        print(f"Error: Repository path does not exist: {repo_path}", file=sys.stderr)
        sys.exit(1)
        
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        print(f"Warning: Not a git repository: {repo_path}. Initializing...", file=sys.stderr)
        subprocess.run(['git', 'init'], cwd=repo_path, check=True)
        subprocess.run(['git', 'config', 'user.name', 'TOAI Release Agent'], cwd=repo_path, check=True)
        subprocess.run(['git', 'config', 'user.email', 'toai@example.com'], cwd=repo_path, check=True)
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial commit'], cwd=repo_path, check=True)
        
    log_output = run_git_command(['git', 'log', '-n', '10', '--oneline'], repo_path)
    if not log_output:
        log_output = "No commit history found or empty repository."
        
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    whitepaper_content = "Whitepaper not found."
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            whitepaper_content = f.read()[:1000]
            
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "git_log": log_output.splitlines(),
        "whitepaper_excerpt": whitepaper_content
    }
    
    output_summary_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    with open(output_summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_summary_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
