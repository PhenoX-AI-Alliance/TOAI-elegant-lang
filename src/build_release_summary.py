import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepaper(workspace_path):
    whitepaper_candidates = [
        os.path.join(workspace_path, 'WHITEPAPER.md'),
        os.path.join(workspace_path, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
        os.path.join(workspace_path, 'CONSTITUTION.md')
    ]
    found_docs = {}
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    found_docs[os.path.basename(path)] = f.read()[:1000]
            except Exception as e:
                print(f"Warning: Could not read {path}: {e}")
    return found_docs

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    if not os.path.exists(repo_path):
        repo_path = workspace_dir
        
    print(f"Scanning repository at: {repo_path}")
    git_logs = get_git_log(repo_path)
    whitepapers = scan_whitepaper(workspace_dir)
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_recent_commits": git_logs,
        "whitepaper_snippets": whitepapers,
        "version": "1.0.0-alpha"
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at: {output_path}")
    except Exception as e:
        print(f"Error saving release summary: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
