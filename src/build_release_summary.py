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
    except Exception as e:
        print(f"Git command failed: {cmd}, error: {e}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        print("Repository not found or not initialized, initializing dummy git or handling gracefully.")
        os.makedirs(repo_dir, exist_ok=True)
        try:
            subprocess.run(['git', 'init'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.name', 'TOAI Agent'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.email', 'agent@toai.internal'], cwd=repo_dir, check=True)
            # Create an initial commit if none exists
            dummy_file = os.path.join(repo_dir, 'README.md')
            if not os.path.exists(dummy_file):
                with open(dummy_file, 'w') as f:
                    f.write("# TOAI-elegant-lang\n")
            subprocess.run(['git', 'add', 'README.md'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=repo_dir, check=True)
        except Exception as init_err:
            print(f"Failed to initialize git repo: {init_err}")

    git_log = run_git_command(['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'], repo_dir)
    git_status = run_git_command(['git', 'status', '--short'], repo_dir)
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "git_log": git_log.splitlines() if git_log else [],
        "git_status": git_status.splitlines() if git_status else [],
        "version": "1.0.0"
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built and saved to {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
