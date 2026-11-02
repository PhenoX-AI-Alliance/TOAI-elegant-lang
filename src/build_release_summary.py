import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    if not os.path.exists(os.path.join(repo_path, '.git')):
        return "Git repository not found or not initialized."
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--oneline']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error fetching git log: {e}"

def scan_whitepaper(repo_path):
    candidates = ['whitepaper.md', 'README.md', 'CONSTITUTION.md']
    summary = {}
    for c in candidates:
        path = os.path.join(repo_path, c)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    summary[c] = f.read()[:500]
            except Exception as e:
                summary[c] = f"Error reading file: {e}"
    return summary

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    git_logs = get_git_log(repo_path)
    whitepaper_data = scan_whitepaper(repo_path)
    
    release_info = {
        "timestamp": datetime.now().isoformat(),
        "git_log": git_logs,
        "whitepaper_summary": whitepaper_data,
        "version": "1.0.0-alpha"
    }
    
    out_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'release_summary.json')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(release_info, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully built at: {out_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
