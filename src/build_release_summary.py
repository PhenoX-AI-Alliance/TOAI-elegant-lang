# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import json
import datetime

def run_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    target_repo = os.path.join(repo_path, 'TOAI-elegant-lang')
    if not os.path.isdir(os.path.join(target_repo, '.git')):
        return "Git repository not found or not initialized."
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=target_repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running git log: {e.stderr}"

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    target_repo = os.path.join(repo_path, 'TOAI-elegant-lang')
    whitepaper_candidates = ['README.md', 'WHITEPAPER.md', 'CONSTITUTION.md']
    summary = {}
    for candidate in whitepaper_candidates:
        full_path = os.path.join(target_repo, candidate)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                summary[candidate] = content[:300] + ('...' if len(content) > 300 else '')
        else:
            summary[candidate] = "File not found."
    return summary

def main():
    print("=== TOAI Release Summary Builder ===")
    git_logs = run_git_log()
    whitepaper_data = scan_whitepaper()
    
    release_info = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_recent_commits": git_logs.splitlines(),
        "whitepaper_summaries": whitepaper_data
    }
    
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(release_info, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    main()
