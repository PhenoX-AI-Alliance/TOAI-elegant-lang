import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def run_git_command(cmd, repo_path):
    try:
        res = subprocess.run(
            cmd,
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e.stderr}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        print(f"Repository path does not exist: {repo_path}")
        sys.exit(1)

    log_output = run_git_command(["git", "log", "-n", "10", "--pretty=format:%h - %an, %ar : %s"], repo_path)
    
    whitepaper_path = os.path.join(workspace_dir, 'WHITE_PAPER.md')
    whitepaper_content = ""
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            whitepaper_content = f.read()[:1000]

    summary = {
        "timestamp": datetime.now().isoformat(),
        "recent_commits": log_output.splitlines() if log_output else [],
        "whitepaper_snippet": whitepaper_content
    }

    output_summary_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    with open(output_summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=4)
    
    print(f"Release summary successfully generated at: {output_summary_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
