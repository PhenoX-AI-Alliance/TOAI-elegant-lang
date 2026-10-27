import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_logs():
    try:
        res = subprocess.run(['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'],
                             capture_output=True, text=True, check=True)
        return res.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_path = os.path.join(workspace, 'TOAI-elegant-lang', 'WHITE_PAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return ''.join(lines[:20])
        except Exception as e:
            return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    print("Building release summary...")
    logs = get_git_logs()
    wp_summary = scan_whitepaper()
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_commits": logs,
        "whitepaper_excerpt": wp_summary,
        "release_status": "Stable",
        "ecosystem": "Gaia Ecosystem - TOAI"
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_file = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at {out_file}")

if __name__ == '__main__':
    main()
