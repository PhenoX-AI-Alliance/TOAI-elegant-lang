import sys
import os
import traceback
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
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace, 'TOAI-elegant-lang')
    
    if not os.path.isdir(repo_dir):
        print(f"Repository directory not found: {repo_dir}")
        sys.exit(1)
        
    git_dir = os.path.join(repo_dir, '.git')
    if not os.path.isdir(git_dir):
        print(f"Not a git repository: {repo_dir}")
        sys.exit(1)
        
    log_output = run_git_command(['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'], repo_dir)
    latest_tag = run_git_command(['git', 'describe', '--tags', '--abbrev=0'], repo_dir)
    if not latest_tag:
        latest_tag = "v0.1.0"
        
    summary_data = {
        "version": latest_tag,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "recent_commits": log_output.splitlines() if log_output else []
    }
    
    output_file = os.path.join(repo_dir, 'release_summary.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Release summary successfully written to {output_file}")
    except Exception as e:
        print(f"Failed to write release summary: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)