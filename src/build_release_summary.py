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
        return f"Error executing {{' '.join(cmd)}}: {{e.stderr.strip()}}"
    except Exception as e:
        return str(e)

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_dir):
        print(f"Repository directory not found: {{repo_dir}}")
        sys.exit(1)
        
    git_check = os.path.join(repo_dir, '.git')
    if not os.path.exists(git_check):
        print(f"Not a git repository: {{repo_dir}}")
        sys.exit(1)
        
    log_output = run_git_command(['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'], repo_dir)
    status_output = run_git_command(['git', 'status', '--short'], repo_dir)
    tag_output = run_git_command(['git', 'describe', '--tags', '--abbrev=0'], repo_dir)
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "latest_tag": tag_output if not tag_output.startswith("Error") else "v0.1.0",
        "recent_commits": log_output.splitlines() if not log_output.startswith("Error") else [],
        "git_status": status_output.splitlines() if not status_output.startswith("Error") else []
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built and saved to {{output_path}}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
