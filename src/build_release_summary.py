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
        print(f"Git command failed: {cmd}, Error: {e}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_dir):
        print(f"Repository directory does not exist: {repo_dir}")
        sys.exit(1)
        
    git_status = run_git_command(['git', 'status', '--porcelain'], repo_dir)
    git_log = run_git_command(['git', 'log', '-n', '10', '--oneline'], repo_dir)
    
    summary = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "repository": "TOAI-elegant-lang",
        "recent_commits": git_log.splitlines() if git_log else [],
        "status": "clean" if not git_status else "dirty",
        "status_details": git_status.splitlines() if git_status else []
    }
    
    output_path = os.path.join(repo_dir, 'release_summary.json')
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"Release summary successfully generated at: {output_path}")
    except Exception as e:
        print(f"Failed to write release summary: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
