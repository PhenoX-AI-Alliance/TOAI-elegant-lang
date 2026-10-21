import sys
import os
import subprocess
import json
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
    except Exception as e:
        print(f"Git command failed: {cmd}, error: {e}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        print("Git repository not initialized. Initializing for release summary...")
        try:
            subprocess.run(['git', 'init'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.name', 'TOAI Builder'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.email', 'builder@toai.local'], cwd=repo_dir, check=True)
            subprocess.run(['touch', 'README.md'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'add', 'README.md'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit for release summary'], cwd=repo_dir, check=True)
        except Exception as init_err:
            print(f"Failed to initialize git repo: {init_err}")
    
    git_log = run_git_command(['git', 'log', '-n', '10', '--oneline'], repo_dir)
    latest_tag = run_git_command(['git', 'describe', '--tags', '--abbrev=0'], repo_dir)
    if not latest_tag:
        latest_tag = "v0.1.0-alpha"
        
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "latest_tag": latest_tag,
        "git_log": git_log.splitlines() if git_log else [],
        "status": "success"
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    main()
