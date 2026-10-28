# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import json
import datetime
import urllib.request
import urllib.error

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
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_path, '.git')):
        print("Error: Git repository not found at target path.", file=sys.stderr)
        sys.exit(1)
        
    git_log = run_git_command(['log', '-n', '10', '--oneline'], repo_path)
    git_status = run_git_command(['status', '--short'], repo_path)
    
    summary_data = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "recent_commits": git_log.splitlines() if git_log else [],
        "git_status": git_status.splitlines() if git_status else []
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Release summary successfully written to {output_file}")
    except Exception as e:
        print(f"Failed to write summary file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()\n