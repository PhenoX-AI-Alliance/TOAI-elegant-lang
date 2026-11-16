# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
import subprocess
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
        print(f"Git command error: {e}", file=sys.stderr)
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_dir):
        print(f"Repository directory does not exist: {repo_dir}", file=sys.stderr)
        sys.exit(1)
        
    git_check = run_git_command(['rev-parse', '--is-inside-work-tree'], repo_dir)
    if git_check != 'true':
        print("Not a valid git repository", file=sys.stderr)
        sys.exit(1)
        
    git_log = run_git_command(['log', '-n', '10', '--oneline'], repo_dir)
    git_status = run_git_command(['status', '--short'], repo_dir)
    
    whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
    whitepaper_content = ""
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            whitepaper_content = f.read()[:1000] 
            
    summary_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "git_log": git_log.splitlines(),
        "git_status": git_status.splitlines(),
        "whitepaper_snippet": whitepaper_content
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated release summary at {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
