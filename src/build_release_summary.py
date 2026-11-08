import sys
import os
import traceback
import subprocess
import json
import datetime

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
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_dir):
        print(f"Error: Repository path does not exist: {repo_dir}")
        sys.exit(1)
        
    git_check = run_git_command(['git', 'rev-parse', '--is-inside-work-tree'], repo_dir)
    if git_check != 'true':
        print("Error: Target directory is not a valid git repository.")
        sys.exit(1)
        
    commit_log = run_git_command(['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ar)'], repo_dir)
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": commit_log.splitlines() if commit_log else []
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated release summary at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)\n