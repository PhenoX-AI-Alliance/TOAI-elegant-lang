# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import json
import datetime

def get_git_logs():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log unavailable: {e}"]

def scan_whitepaper(workspace):
    whitepaper_candidates = ['README.md', 'CONSTITUTION.md', 'WHITE_PAPER.md']
    summaries = {}
    for candidate in whitepaper_candidates:
        path = os.path.join(workspace, candidate)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    summaries[candidate] = "".join(lines[:5]).strip()
            except Exception as e:
                summaries[candidate] = f"Error reading: {e}"
    return summaries

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    logs = get_git_logs()
    whitepapers = scan_whitepaper(workspace)
    
    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_recent_commits": logs,
        "whitepaper_summaries": whitepapers,
        "status": "success"
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    main()
