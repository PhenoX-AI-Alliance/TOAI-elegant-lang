import sys
import os
import subprocess
import json
from datetime import datetime

def run_git_log():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        res = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception as e:
        return f"Git log unavailable: {e}"

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_path = os.path.join(workspace, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        with open(wp_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return "".join(lines[:20])
    return "Whitepaper not found."

def main():
    print("Building release summary...")
    logs = run_git_log()
    wp_summary = scan_whitepaper()
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_logs": logs,
        "whitepaper_excerpt": wp_summary
    }
    
    out_path = os.path.join(os.path.dirname(__file__), 'release_summary.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    print(f"Release summary successfully written to {out_path}")

if __name__ == '__main__':
    main()
