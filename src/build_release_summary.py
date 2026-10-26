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
        print(f"Git command failed: {e}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        print("Git repository not found. Initializing...")
        try:
            subprocess.run(['git', 'init'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.name', 'TOAI Executor'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.email', 'executor@toai.internal'], cwd=repo_dir, check=True)
        except Exception as init_err:
            print(f"Failed to initialize git repository: {init_err}")
            sys.exit(1)
            
    git_log = run_git_command(['git', 'log', '-n', '10', '--oneline'], repo_dir)
    if not git_log:
        git_log = "No commit history available yet."
        
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": git_log.splitlines(),
        "status": "release_summary_generated"
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully written to {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error in release summary builder: {e}")
        sys.exit(1)
