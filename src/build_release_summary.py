import sys
import os
import subprocess
import json
import time

def run_git_command(cmd, cwd):
    try:
        res = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return res.stdout.strip()
    except Exception as e:
        print(f"Git command error: {e}", file=sys.stderr)
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        print(f"Error: {repo_dir} is not a git repository.", file=sys.stderr)
        sys.exit(1)
        
    git_log = run_git_command(['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'], repo_dir)
    git_status = run_git_command(['git', 'status', '--porcelain'], repo_dir)
    
    summary = {
        "timestamp": time.time(),
        "git_log": git_log.splitlines() if git_log else [],
        "git_status": git_status.splitlines() if git_status else []
    }
    
    out_file = os.path.join(output_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated release summary at {out_file}")

if __name__ == '__main__':
    main()
