import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    if not os.path.exists(os.path.join(repo_path, '.git')):
        return "Git repository not found."
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Failed to fetch git log: {e}"

def scan_whitepaper(repo_path):
    wp_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                return f.read()[:1000]
        except Exception as e:
            return f"Error reading WHITEPAPER.md: {e}"
    return "WHITEPAPER.md not found."

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    git_logs = get_git_log(repo_path)
    whitepaper_snippet = scan_whitepaper(repo_path)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_logs": git_logs,
        "whitepaper_snippet": whitepaper_snippet
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated release summary at {out_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
