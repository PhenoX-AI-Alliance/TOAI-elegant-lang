# -*- coding: utf-8 -*-
import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log(max_count=10):
    repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_path = os.path.join(repo_dir, 'TOAI-elegant-lang')
    if not os.path.exists(os.path.join(git_path, '.git')):
        git_path = repo_dir
    try:
        cmd = ['git', '-C', git_path, 'log', f'-n', str(max_count), '--oneline']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')
    except Exception as e:
        print(f"Warning: Failed to fetch git log: {e}")
        return []

def scan_whitepaper():
    repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    possible_paths = [
        os.path.join(repo_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
        os.path.join(repo_dir, 'WHITEPAPER.md')
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:1000]
            except Exception as e:
                print(f"Warning: Failed to read whitepaper at {path}: {e}")
    return "Whitepaper not found."

def main():
    print("Starting release summary generation...")
    logs = get_git_log(15)
    whitepaper_snippet = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": logs,
        "whitepaper_snippet": whitepaper_snippet
    }
    
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
