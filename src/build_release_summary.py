#!/usr/bin/env python3
import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_path = os.path.join(workspace_dir, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return "".join(lines[:20]) # First 20 lines as summary
        except Exception as e:
            return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    print("=== TOAI Release Summary Generator ===")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    git_logs = get_git_log()
    whitepaper_summary = scan_whitepaper(workspace_dir)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_commits": git_logs,
        "whitepaper_summary": whitepaper_summary
    }
    
    output_file = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)
