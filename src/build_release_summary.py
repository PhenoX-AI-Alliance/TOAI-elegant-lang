#!/usr/bin/env python3
import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        cmd = ["git", "log", "-n", "10", "--pretty=format:%h - %an: %s (%ad)", "--date=short"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=os.getcwd())
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_workspace():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_path = os.path.join(workspace, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_commits": get_git_log(),
        "whitepaper_exists": os.path.exists(whitepaper_path)
    }
    return summary

def main():
    summary = scan_workspace()
    output_dir = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Release summary successfully generated at: {out_file}")

if __name__ == '__main__':
    main()
