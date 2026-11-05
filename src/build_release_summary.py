# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import datetime
import json

def get_git_logs(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n {max_count}', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log retrieval failed: {e}"

def scan_whitepaper(repo_path):
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                return f.read()[:1000]
        except Exception as e:
            return f"Whitepaper read error: {e}"
    return "No WHITEPAPER.md found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_path, '.git')):
        print("Git repository not initialized. Initializing for release tracking...")
        try:
            subprocess.run(['git', 'init', repo_path], check=True)
        except Exception as e:
            print(f"Failed to init git: {e}")
            
    git_logs = get_git_logs(repo_path)
    whitepaper_summary = scan_whitepaper(repo_path)
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": git_logs,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_json_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {output_json_path}")

if __name__ == '__main__':
    main()
