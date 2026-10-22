#!/usr/bin/env python3
import sys
import os
import subprocess
import datetime
import json

def get_git_log(max_count=10):
    repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_path = os.path.join(repo_dir, '.git')
    if not os.path.exists(git_path):
        return ["Git repository not initialized or found."]
    try:
        cmd = ['git', '-C', repo_dir, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper():
    repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_path = os.path.join(repo_dir, 'WHITE_PAPER.md')
    if not os.path.exists(wp_path):
        return "Whitepaper (WHITE_PAPER.md) not found."
    try:
        with open(wp_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return "".join(lines[:30]) # Return first 30 lines as overview
    except Exception as e:
        return f"Error reading whitepaper: {str(e)}"

def generate_summary():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    logs = get_git_log(15)
    whitepaper_preview = scan_whitepaper()
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0-alpha",
        "git_history": logs,
        "whitepaper_overview": whitepaper_preview
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    generate_summary()
