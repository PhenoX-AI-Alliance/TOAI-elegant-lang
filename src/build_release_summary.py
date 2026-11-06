import sys
import os
import traceback
import time
import json
import subprocess
import datetime

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
        print(f"Git command failed: {e}", file=sys.stderr)
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_dir):
        print(f"Repository directory does not exist: {repo_dir}", file=sys.stderr)
        sys.exit(1)
        
    git_status = run_git_command(['rev-parse', '--is-inside-work-tree'], repo_dir)
    if git_status != 'true':
        print("Target directory is not a valid git repository.", file=sys.stderr)
        sys.exit(1)
        
    latest_tag = run_git_command(['describe', '--tags', '--abbrev=0'], repo_dir)
    if not latest_tag:
        latest_tag = "HEAD"
        
    log_range = f"{latest_tag}..HEAD" if latest_tag != "HEAD" else "HEAD"
    git_log = run_git_command(['log', log_range, '--pretty=format:- %s (%an)'], repo_dir)
    
    summary_data = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "latest_tag": latest_tag,
        "changelog": git_log if git_log else "No recent changes found."
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
