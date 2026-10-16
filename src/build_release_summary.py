# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def run_git_command(args):
    try:
        result = subprocess.run(
            ['git'] + args,
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
    print("Building release summary for TOAI-elegant-lang...")
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    original_cwd = os.getcwd()
    if os.path.exists(repo_path):
        os.chdir(repo_path)
    
    git_log = run_git_command(['log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'])
    git_status = run_git_command(['status', '--short'])
    
    os.chdir(original_cwd)
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "git_log": git_log.splitlines() if git_log else [],
        "git_status": git_status.splitlines() if git_status else [],
        "message": "Release summary generated successfully with altruistic intent."
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully written to {out_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
