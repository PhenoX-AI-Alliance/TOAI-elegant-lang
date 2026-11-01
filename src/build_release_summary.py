import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n {max_count}', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        print(f"Warning: Failed to fetch git log: {e}")
        return []

def scan_whitepaper(repo_path):
    wp_candidates = [
        os.path.join(repo_path, 'WHITEPAPER.md'),
        os.path.join(repo_path, 'docs', 'WHITEPAPER.md'),
        os.path.join(repo_path, 'README.md')
    ]
    for path in wp_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:2000] # Return first 2000 chars as summary
            except Exception as e:
                print(f"Warning: Failed to read {path}: {e}")
    return "No whitepaper found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print(f"Scanning repository at: {repo_path}")
    
    git_commits = []
    if os.path.exists(os.path.join(repo_path, '.git')):
        git_commits = get_git_log(repo_path)
    else:
        print("Notice: Git repository not initialized at target. Skipping git log.")
        
    whitepaper_summary = scan_whitepaper(repo_path)
    
    release_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0-alpha",
        "git_recent_commits": git_commits,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated release summary at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
