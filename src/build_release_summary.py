#!/usr/bin/env python3
import sys
import os
import subprocess
import json
from datetime import datetime

def run_git_command(args, cwd):
    try:
        res = subprocess.run(
            ['git'] + args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception as e:
        return f"Error executing git: {e}"

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        print("Git repository not initialized in target path. Initializing...")
        try:
            os.makedirs(repo_dir, exist_ok=True)
            subprocess.run(['git', 'init'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.name', 'TOAI Executor'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.email', 'executor@toai.internal'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'add', '.'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit by TOAI release builder'], cwd=repo_dir, check=True)
        except Exception as init_err:
            print(f"Failed to initialize git repository: {init_err}")
    
    git_log = run_git_command(['log', '-n', '10', '--oneline'], repo_dir)
    latest_commit = run_git_command(['log', '-n', '1', '--format=%H - %an: %s (%cd)'], repo_dir)
    
    whitepaper_path = os.path.join(repo_dir, 'WHITESPAPER.md')
    whitepaper_summary = "Whitepaper not found."
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            whitepaper_summary = "".join(lines[:20])
    
    release_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "latest_commit": latest_commit,
        "recent_commits": git_log.splitlines() if git_log else [],
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_path = os.path.join(repo_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(release_data, out, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    main()
