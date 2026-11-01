import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=10):
    if not os.path.exists(os.path.join(repo_path, '.git')):
        return "Git repository not initialized."
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
        return f"Failed to retrieve git log: {str(e)}"

def scan_whitepaper(workspace_path):
    whitepaper_candidates = [
        os.path.join(workspace_path, 'WHITEPAPER.md'),
        os.path.join(workspace_path, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
        os.path.join(workspace_path, 'docs', 'WHITEPAPER.md')
    ]
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:1000]
            except Exception:
                pass
    return "Whitepaper not found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    git_logs = get_git_log(repo_path)
    whitepaper_snippet = scan_whitepaper(workspace_dir)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "workspace": workspace_dir,
        "git_logs": git_logs,
        "whitepaper_snippet": whitepaper_snippet
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully built at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
