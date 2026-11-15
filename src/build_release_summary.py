# -*- coding: utf-8 -*-
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
        print(f"Git command failed: {' '.join(args)}", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        return ""

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace, 'TOAI-elegant-lang')
    
    if not os.path.isdir(repo_dir):
        print(f"Error: Repository directory not found at {repo_dir}", file=sys.stderr)
        sys.exit(1)
        
    git_dir = os.path.join(repo_dir, '.git')
    if not os.path.isdir(git_dir):
        print(f"Error: Not a git repository: {repo_dir}", file=sys.stderr)
        sys.exit(1)
        
    print("Scanning git log for release summary...")
    log_output = run_git_command(['log', '-n', '20', '--pretty=format:%h - %an, %ar : %s'], repo_dir)
    
    whitepaper_path = os.path.join(repo_dir, 'WHITE_PAPER.md')
    whitepaper_content = ""
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            whitepaper_content = f.read()[:1000] # First 1000 chars for summary
            
    summary_data = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "recent_commits": log_output.splitlines() if log_output else [],
        "whitepaper_excerpt": whitepaper_content
    }
    
    output_path = os.path.join(repo_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
