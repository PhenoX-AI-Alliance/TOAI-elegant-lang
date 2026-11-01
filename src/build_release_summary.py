import sys
import os
import traceback
import subprocess
import json
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
        print(f"Git command error: {e}")
        return ""

def main():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(base_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_dir):
        print(f"Error: Repository directory not found at {repo_dir}")
        sys.exit(1)
        
    git_check = os.path.join(repo_dir, '.git')
    if not os.path.exists(git_check):
        print("Initializing git repository for release summary...")
        subprocess.run(['git', 'init'], cwd=repo_dir, capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'TOAI Builder'], cwd=repo_dir, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'builder@toai.local'], cwd=repo_dir, capture_output=True)
        subprocess.run(['git', 'add', '.'], cwd=repo_dir, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit for release summary'], cwd=repo_dir, capture_output=True)
        
    git_log = run_git_command(['git', 'log', '-n', '10', '--oneline'], repo_dir)
    latest_tag = run_git_command(['git', 'describe', '--tags', '--abbrev=0'], repo_dir)
    if not latest_tag:
        latest_tag = "v0.1.0-alpha"
        
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "version": latest_tag,
        "recent_commits": git_log.splitlines() if git_log else [],
        "status": "stable"
    }
    
    output_dir = os.path.join(base_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully built and saved to {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
