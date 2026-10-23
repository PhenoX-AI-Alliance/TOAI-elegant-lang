# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import json
from datetime import datetime

def run_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, 'TOAI-elegant-lang')
    if not os.path.exists(os.path.join(git_dir, '.git')):
        git_dir = repo_path
    
    try:
        cmd = ['git', '-C', git_dir, 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log error: {str(e)}"]

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    candidates = [
        os.path.join(repo_path, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
        os.path.join(repo_path, 'WHITEPAPER.md')
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    return [line.strip() for line in lines[:20] if line.strip()]
            except Exception:
                pass
    return ["Whitepaper not found or unreadable."]

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    logs = run_git_log()
    whitepaper_summary = scan_whitepaper()
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "version_overview": whitepaper_summary[:5],
        "recent_commits": logs
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    main()
