import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def run_git_command(args, cwd):
    try:
        result = subprocess.run(
            ['git'] + args,
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
    
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir, exist_ok=True)
        try:
            subprocess.run(['git', 'init', repo_dir], check=True)
        except Exception as e:
            print(f"Failed to init git repo: {e}")

    git_log = run_git_command(['log', '-n', '10', '--oneline'], repo_dir)
    if not git_log:
        git_log = "No commit history found or not a git repository yet."

    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "recent_commits": git_log.splitlines(),
        "status": "release summary generated successfully"
    }

    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)

    print(f"Release summary successfully written to {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
