import sys
import os
import subprocess
import json
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
    except Exception as e:
        print(f"Git command failed: {e}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.isdir(os.path.join(repo_dir, '.git')):
        print("Error: Target directory is not a git repository.")
        sys.exit(1)
        
    git_log = run_git_command(['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'], repo_dir)
    git_status = run_git_command(['git', 'status', '--short'], repo_dir)
    
    whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
    whitepaper_content = ""
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            whitepaper_content = f.read()[:1000] # Read first 1000 chars as summary
            
    summary_data = {
        "generated_at": datetime.now().isoformat(),
        "git_log": git_log.splitlines() if git_log else [],
        "git_status": git_status.splitlines() if git_status else [],
        "whitepaper_excerpt": whitepaper_content
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {output_path}")

if __name__ == '__main__':
    main()
