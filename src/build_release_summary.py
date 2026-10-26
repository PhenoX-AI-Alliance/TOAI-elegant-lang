#!/usr/bin/env python3
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
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {' '.join(args)}, error: {e.stderr.strip()}", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"Unexpected error running git: {e}", file=sys.stderr)
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        print("Error: Target directory is not a git repository.", file=sys.stderr)
        sys.exit(1)
        
    print("Scanning git log for release summary...")
    git_log = run_git_command(['log', '-n', '20', '--pretty=format:%h - %an, %ar : %s'], repo_dir)
    latest_tag = run_git_command(['describe', '--tags', '--abbrev=0'], repo_dir)
    if not latest_tag:
        latest_tag = "v0.1.0-alpha"
        
    summary_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "latest_tag": latest_tag,
        "recent_commits": git_log.splitlines() if git_log else []
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'release_summary.json')
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at: {output_path}")
    except Exception as e:
        print(f"Failed to write release summary: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)