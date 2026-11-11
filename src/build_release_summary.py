#!/usr/bin/env python3
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
        print(f"Repository directory not found: {repo_dir}", file=sys.stderr)
        sys.exit(1)
        
    git_check = run_git_command(['rev-parse', '--is-inside-work-tree'], repo_dir)
    if git_check != 'true':
        print("Target directory is not a git repository.", file=sys.stderr)
        sys.exit(1)
        
    latest_tag = run_git_command(['describe', '--tags', '--abbrev=0'], repo_dir)
    if not latest_tag:
        latest_tag = "HEAD~10"
        
    log_range = f"{latest_tag}..HEAD" if latest_tag != "HEAD~10" else "HEAD~10..HEAD"
    git_log = run_git_command(['log', log_range, '--oneline'], repo_dir)
    
    whitepaper_path = os.path.join(repo_dir, 'WHITE_PAPER.md')
    whitepaper_snippet = ""
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            whitepaper_snippet = "".join(lines[:20])
            
    summary_data = {
        "timestamp": datetime.datetime.utcnow().isoformat() + " Z",
        "latest_reference": latest_tag,
        "git_log": git_log.splitlines(),
        "whitepaper_overview": whitepaper_snippet
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
