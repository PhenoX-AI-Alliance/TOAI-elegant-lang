import sys
import os
import traceback
import time
import json
import subprocess

def run_command(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)
        if res.returncode != 0:
            return f"Error executing {{cmd}}: {{res.stderr.strip()}}"
        return res.stdout.strip()
    except Exception as e:
        return f"Exception executing {{cmd}}: {{str(e)}}"

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace, 'TOAI-elegant-lang')
    
    git_status = "Not a git repository or git not initialized."
    git_log = "No git log available."
    git_tags = "No tags available."
    
    if os.path.exists(os.path.join(repo_dir, '.git')):
        git_status = run_command(['git', 'status'], cwd=repo_dir)
        git_log = run_command(['git', 'log', '--oneline', '-50'], cwd=repo_dir)
        git_tags = run_command(['git', 'describe', '--tags', '--abbrev=0'], cwd=repo_dir)
    else:
        # Fallback to workspace root if TOAI-elegant-lang is not a separate git repo
        if os.path.exists(os.path.join(workspace, '.git')):
            git_status = run_command(['git', 'status'], cwd=workspace)
            git_log = run_command(['git', 'log', '--oneline', '-50'], cwd=workspace)
            git_tags = run_command(['git', 'describe', '--tags', '--abbrev=0'], cwd=workspace)

    summary_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "git_status": git_status,
        "git_tags": git_tags,
        "git_log": git_log
    }
    
    output_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {{output_path}}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
