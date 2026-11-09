# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, 'TOAI-elegant-lang')
    if not os.path.exists(os.path.join(git_dir, '.git')):
        git_dir = repo_path
    
    try:
        cmd = ['git', '-C', git_dir, 'log', '-n', '20', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Could not retrieve git log: {str(e)}"]

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    target_paths = [
        os.path.join(repo_path, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
        os.path.join(repo_path, 'WHITEPAPER.md')
    ]
    for path in target_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:1000] # Return summary of whitepaper
            except Exception:
                pass
    return "Whitepaper not found."

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    logs = get_git_log()
    whitepaper_summary = scan_whitepaper()
    
    release_data = {
        "timestamp": datetime.now().isoformat(),
        "version_summary": "TOAI-elegant-lang Release Summary",
        "git_logs": logs,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    out_file = os.path.join(output_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated release summary at: {out_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)\n