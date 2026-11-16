#!/usr/bin/env python3
import sys
import os
import subprocess
import json
import datetime

def get_git_logs():
    try:
        cmd = ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)', '--date=short']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git logs: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return [line.strip() for line in lines[:20] if line.strip()]
    return ["Whitepaper not found."]

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    logs = get_git_logs()
    whitepaper_summary = scan_whitepaper(workspace_dir)

    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0",
        "recent_commits": logs,
        "whitepaper_excerpt": whitepaper_summary
    }

    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, 'release_summary.json')

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, indent=2, ensure_ascii=False)

    print(f"Release summary successfully generated at: {out_file}")

if __name__ == '__main__':
    main()
