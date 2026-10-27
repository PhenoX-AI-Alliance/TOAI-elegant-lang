import sys
import os
import subprocess
import json
from datetime import datetime

def run_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        return "Git repository not initialized."
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Git error: {e.stderr.strip()}"

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        with open(wp_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return "".join(lines[:20])
    return "Whitepaper not found."

def main():
    print("Building release summary...")
    git_logs = run_git_log()
    whitepaper_snippet = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_commits": git_logs.splitlines(),
        "whitepaper_overview": whitepaper_snippet
    }
    
    output_dir = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully written to {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error in release summary builder: {e}", file=sys.stderr)
        sys.exit(1)
