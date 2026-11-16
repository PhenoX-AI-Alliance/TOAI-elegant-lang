# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def run_git_command(cmd, repo_path):
    try:
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {' '.join(cmd)}, error: {e.stderr.strip()}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)
        
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        print(f"Error: Not a git repository: {repo_path}")
        sys.exit(1)
        
    print(f"Scanning repository at: {repo_path}")
    
    latest_tag = run_git_command(["git", "describe", "--tags", "--abbrev=0"], repo_path)
    if not latest_tag:
        latest_tag = "HEAD (No tags found)"
        
    print(f"Latest Tag / Version: {latest_tag}")
    
    log_output = run_git_command(["git", "log", "-n", "10", "--pretty=format:%h - %an: %s (%ad)", "--date=short"], repo_path)
    
    whitepaper_path = os.path.join(repo_path, 'WHITE_PAPER.md')
    whitepaper_summary = "White paper not found."
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            whitepaper_summary = "".join(lines[:15]).strip()
            
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "latest_tag": latest_tag,
        "recent_commits": log_output.splitlines() if log_output else [],
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=4)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
